#!/usr/bin/env python3
"""ITR2 Quest Korean patch installer. Python 3.10+, standard library only.

Installer code: MIT (licenses/INSTALLER-MIT.txt).
Translation strings used with permission; see THIRD_PARTY_NOTICES.md.
No APK installation, account access, or save restoration.
"""
from __future__ import annotations
import argparse
import contextlib
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import uuid
import zlib
import time
import tempfile
import urllib.request
import zipfile
import webbrowser

ROOT = Path(sys.executable if getattr(sys, 'frozen', False) else __file__).resolve().parent
CHUNK = 8 * 1024 * 1024
ADB_URL = 'https://dl.google.com/android/repository/platform-tools_r37.0.0-win.zip'
ADB_ZIP_HASH = '4fe305812db074cea32903a489d061eb4454cbc90a49e8fea677f4b7af764918'
ADB_TERMS = 'https://developer.android.com/studio/terms'

class PatchError(Exception):
    pass

def unpack_adb(archive, destination):
    """Only extract the pinned official archive inside a new private staging directory."""
    if sha256(archive) != ADB_ZIP_HASH:
        raise PatchError('ADB 다운로드 체크섬이 다릅니다. 실행하지 않고 중단합니다.')
    destination = Path(destination).resolve()
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            parts = member.filename.split('/')
            if parts[0] != 'platform-tools' or any(x in ('.', '..') or ':' in x or '\\' in x for x in parts):
                raise PatchError('ADB 압축 파일에 잘못된 경로가 있습니다.')
            target = (destination / member.filename).resolve()
            if not target.is_relative_to(destination):
                raise PatchError('ADB 압축 해제 경로 오류')
        z.extractall(destination)
    tool = destination / 'platform-tools'
    for name in ('adb.exe', 'AdbWinApi.dll', 'AdbWinUsbApi.dll', 'NOTICE.txt'):
        if not (tool / name).is_file():
            raise PatchError('ADB 필수 파일이 빠졌습니다: ' + name)
    return tool

def prepare_adb(root=ROOT):
    home = Path(root) / '.tools'
    installed = home / 'platform-tools-37.0.0'
    receipt = installed / 'download-receipt.json'
    if receipt.is_file():
        record = json.loads(receipt.read_text(encoding='utf-8'))
        if record.get('archive_sha256') == ADB_ZIP_HASH and record.get('license_accepted') is True:
            hashes = record.get('files', {})
            required = {'adb.exe', 'AdbWinApi.dll', 'AdbWinUsbApi.dll', 'NOTICE.txt'}
            if required.issubset(hashes) and all(
                    Path(name).name == name and (installed / name).is_file()
                    and sha256(installed / name) == expected for name, expected in hashes.items()):
                return str(installed / 'adb.exe')
        raise PatchError('자동 준비한 ADB가 손상되었습니다. .tools 폴더를 별도 보관한 뒤 다시 실행하세요.')
    say('연결 도구 ADB를 처음 한 번 Google 공식 서버에서 다운로드합니다.')
    say('별도 설치나 관리자 권한은 필요하지 않으며 인터넷 연결이 필요합니다.')
    say('Google Android SDK 약관: ' + ADB_TERMS)
    say('Y: 약관에 동의하고 다운로드 / V: 약관을 브라우저에서 보기 / N: 취소')
    while True:
        try:
            answer = input('선택 [Y/V/N]: ').strip().lower()
        except EOFError:
            raise PatchError('ADB 약관 확인이 필요합니다. 설치.bat에서 직접 실행하세요.')
        if answer == 'v':
            webbrowser.open(ADB_TERMS)
        elif answer == 'y':
            break
        else:
            raise PatchError('ADB 다운로드를 취소했습니다. 기기는 변경하지 않았습니다.')
    home.mkdir(parents=True, exist_ok=True)
    with operation_lock(home):
        if installed.exists():
            raise PatchError('.tools에 기존 ADB 폴더가 있습니다. 덮어쓰지 않습니다.')
        staging = Path(tempfile.mkdtemp(prefix='download-', dir=home)).resolve()
        try:
            archive = staging / 'platform-tools.zip'
            request = urllib.request.Request(ADB_URL, headers={'User-Agent': 'ITR2QuestKorean-RC1'})
            say('ADB 다운로드 중...')
            with urllib.request.urlopen(request, timeout=30) as response, archive.open('xb') as f:
                if not response.geturl().startswith('https://dl.google.com/'):
                    raise PatchError('공식 서버가 아닌 다운로드 주소로 연결되었습니다.')
                total = 0
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    total += len(block)
                    if total > 64 * 1024 * 1024:
                        raise PatchError('ADB 다운로드 크기가 예상 범위를 벗어났습니다.')
                    f.write(block)
                    say(f'ADB 다운로드: {total // 1024} KB')
            tool = unpack_adb(archive, staging)
            record = {'url': ADB_URL, 'archive_sha256': ADB_ZIP_HASH, 'license_accepted': True,
                      'terms_url': ADB_TERMS, 'accepted_at': datetime.datetime.now().isoformat(),
                      'files': {f.name: sha256(f) for f in tool.iterdir() if f.is_file()}}
            (tool / 'download-receipt.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
            tool.rename(installed)
            say('ADB 준비 완료. 다음 실행부터 다시 다운로드하지 않습니다.')
        finally:
            if staging.is_relative_to(home.resolve()) and staging.name.startswith('download-'):
                shutil.rmtree(staging)
    return str(installed / 'adb.exe')

def say(message):
    print(message, flush=True)

def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(CHUNK), b''):
            h.update(block)
    return h.hexdigest()

def load_release(root=ROOT):
    root = Path(root)
    m = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    if m.get('format') != 1:
        raise PatchError('지원하지 않는 배포본 형식입니다.')
    for name, key in [('recipe.json', 'recipe_sha256'), ('payload.bin', 'payload_sha256')]:
        if sha256(root / 'data' / name) != m[key]:
            raise PatchError(f'{name} 무결성 오류. 배포 ZIP을 다시 풀어 주세요.')
    recipe = json.loads((root / 'data/recipe.json').read_text(encoding='utf-8'))
    if recipe.get('format') != 1:
        raise PatchError('지원하지 않는 변환 정보입니다.')
    total = 0
    payload_size = (root / 'data/payload.bin').stat().st_size
    for op in recipe['operations']:
        if len(op) not in (3, 5) or op[0] not in ('copy', 'data', 'zero', 'zlib'):
            raise PatchError('변환 정보가 손상되었습니다.')
        kind, offset, length = op[:3]
        if not isinstance(offset, int) or not isinstance(length, int) or offset < 0 or length < 0:
            raise PatchError('잘못된 변환 범위입니다.')
        if kind == 'copy' and offset + length > m['main_bytes']:
            raise PatchError('원본 범위를 벗어난 변환입니다.')
        if kind == 'data' and offset + length > payload_size:
            raise PatchError('패치 데이터 범위를 벗어났습니다.')
        if kind == 'zlib' and (len(op) != 5 or not 0 < op[3] <= 1024 * 1024 or offset + op[3] > m['main_bytes']):
            raise PatchError('잘못된 폰트 처리 범위입니다.')
        total += length
    if total != m['main_bytes']:
        raise PatchError('예상 결과 크기가 다릅니다.')
    return m, recipe

def build(source, output, root=ROOT):
    """Reconstruct the exact user-tested OBB. Wrong originals fail before any output is created."""
    m, recipe = load_release(root)
    source, output = Path(source).resolve(), Path(output).resolve()
    if source == output:
        raise PatchError('원본과 결과 경로는 달라야 합니다.')
    say('원본 main OBB 체크섬 확인 중...')
    if source.stat().st_size != m['main_bytes'] or sha256(source) != m['source_sha256']:
        raise PatchError('지원하는 1.2.3 / 478362 원본이 아닙니다. 수정하거나 설치하지 않았습니다.')
    if output.exists():
        if sha256(output) == m['target_sha256']:
            say('이미 검증된 결과 파일이 있습니다.')
            return output
        raise PatchError('결과 경로에 다른 파일이 있습니다. 덮어쓰지 않습니다.')
    output.parent.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(output.parent).free < m['main_bytes'] + 512 * 1024 * 1024:
        raise PatchError('결과 파일을 만들 PC 여유 공간이 부족합니다. 최소 5GB를 확보하세요.')
    temp = output.with_name(output.name + '.building-' + uuid.uuid4().hex[:8])
    digest, written, last_notice = hashlib.sha256(), 0, 0
    try:
        with source.open('rb') as src, (Path(root) / 'data/payload.bin').open('rb') as payload, temp.open('xb') as dst:
            def write(block):
                nonlocal written, last_notice
                dst.write(block)
                digest.update(block)
                written += len(block)
                if written - last_notice >= 512 * 1024 * 1024:
                    say(f'패치 생성 {written * 100 // m["main_bytes"]}%')
                    last_notice = written
            for op in recipe['operations']:
                kind, offset, count = op[:3]
                if kind == 'zlib':
                    src.seek(offset)
                    block = zlib.compress(src.read(op[3]), 9)
                    if len(block) != count or hashlib.sha256(block).hexdigest() != op[4]:
                        raise PatchError('원본 폰트 재생성 결과가 다릅니다. Python/zlib 호환성을 확인하세요. 기기는 변경하지 않았습니다.')
                    write(block)
                elif kind == 'zero':
                    while count:
                        size = min(count, CHUNK)
                        write(bytes(size))
                        count -= size
                else:
                    f = src if kind == 'copy' else payload
                    f.seek(offset)
                    while count:
                        block = f.read(min(count, CHUNK))
                        if not block:
                            raise PatchError('입력 파일이 중간에 끝났습니다.')
                        write(block)
                        count -= len(block)
            dst.flush()
            os.fsync(dst.fileno())
        if written != m['main_bytes'] or digest.hexdigest() != m['target_sha256']:
            raise PatchError('생성 결과가 검증된 1.2.3 시험본과 다릅니다. 설치를 중단했습니다.')
        # A concurrent process must not replace an existing user file.
        if output.exists():
            raise PatchError('결과 경로에 파일이 생겨 덮어쓰기를 중단했습니다.')
        temp.rename(output)
        say('완료: 결과 SHA-256이 새 버전 PC 검증본과 일치합니다.')
        return output
    finally:
        if temp.exists():
            temp.unlink()

class Adb:
    def __init__(self, executable, serial=None):
        self.executable = str(executable)
        self.serial = serial

    def run(self, *args, timeout=180, check=True):
        cmd = [self.executable] + (['-s', self.serial] if self.serial else []) + list(args)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, encoding='utf-8', errors='replace')
        started = time.monotonic()
        try:
            while True:
                remaining = timeout - (time.monotonic() - started)
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(cmd, timeout)
                try:
                    output, _ = p.communicate(timeout=min(15, remaining))
                    break
                except subprocess.TimeoutExpired:
                    say(f'파일 검사/전송 진행 중... {int(time.monotonic() - started)}초')
        except BaseException:
            p.kill()
            p.communicate()
            raise
        if check and p.returncode:
            raise PatchError('ADB 작업 실패: ' + output.strip())
        return output.strip(), p.returncode

    def shell(self, *args, **kwargs):
        return self.run('shell', ' '.join(shlex.quote(str(x)) for x in args), **kwargs)

    def exists(self, path):
        return self.shell('test', '-e', path, check=False)[1] == 0

    def hash(self, path, missing_ok=False):
        if missing_ok and not self.exists(path):
            return None
        out, _ = self.shell('sha256sum', path, timeout=180)
        if not re.match(r'^[0-9a-fA-F]{64}\s', out):
            raise PatchError('기기 파일의 체크섬을 읽지 못했습니다: ' + path)
        return out.split()[0].lower()

def connect(args):
    if args.adb and not Path(args.adb).is_file():
        raise PatchError('--adb로 지정한 실행 파일을 찾을 수 없습니다.')
    candidates = [args.adb, shutil.which('adb')]
    if os.environ.get('APPDATA'):
        candidates.append(str(Path(os.environ['APPDATA']) / 'SideQuest/platform-tools/adb.exe'))
    if os.environ.get('LOCALAPPDATA'):
        candidates.append(str(Path(os.environ['LOCALAPPDATA']) / 'Android/Sdk/platform-tools/adb.exe'))
    executable = next((x for x in candidates if x and Path(x).is_file()), None)
    if not executable:
        executable = prepare_adb()
    adb = Adb(executable)
    out, _ = adb.run('devices')
    all_devices = [line.split() for line in out.splitlines() if line.strip() and not line.startswith(('List ', '*'))]
    devices = [x[0] for x in all_devices if len(x) >= 2 and x[1] == 'device']
    if args.serial:
        if args.serial not in devices:
            raise PatchError('지정한 기기가 연결/허용되어 있지 않습니다. USB 디버깅을 허용하세요.')
        adb.serial = args.serial
    elif len(devices) == 1:
        adb.serial = devices[0]
    else:
        raise PatchError('연결된 허용 기기가 없거나 여러 대입니다. 한 대만 연결하거나 --serial을 지정하세요.')
    if not re.fullmatch(r'[A-Za-z0-9_.:-]+', adb.serial):
        raise PatchError('지원하지 않는 기기 식별자입니다.')
    return adb

def paths(m):
    directory = '/sdcard/Android/obb/' + m['package']
    main = directory + '/' + m['main_name']
    return main, main + '.questko-original', directory + '/' + m['patch_name']

def version_check(adb, m):
    text, _ = adb.shell('dumpsys', 'package', m['package'])
    match = re.search(r'\bversionCode=(\d+)', text)
    if not match or int(match.group(1)) != m['version_code']:
        raise PatchError('대상 게임은 Quest 1.2.3 / 478362만 지원합니다. 다른 버전은 변경하지 않습니다.')

def stopped(adb, m):
    out, _ = adb.shell('pidof', m['package'], check=False)
    if out.strip():
        raise PatchError('게임이 실행 중입니다. 게임을 종료한 뒤 다시 실행하세요. 강제 종료하지 않았습니다.')

def status(adb, m):
    version_check(adb, m)
    main, backup, patch = paths(m)
    say('기기 원본/패치 체크섬을 확인합니다...')
    h = adb.hash(main, missing_ok=True)
    label = {m['source_sha256']: '원본 상태', m['target_sha256']: '검증된 한글 수정본 설치 상태', None: 'main OBB 없음'}.get(h, '지원하지 않는 파일 또는 다른 수정본')
    b = adb.hash(backup, missing_ok=True)
    p = adb.hash(patch, missing_ok=True)
    report = {'game': '1.2.3 / 478362', 'state': label, 'main_sha256': h,
              'device_original_backup_valid': b == m['source_sha256'],
              'patch_obb_original': p == m['patch_sha256']}
    say(json.dumps(report, ensure_ascii=False, indent=2))
    return report

@contextlib.contextmanager
def operation_lock(work):
    work.mkdir(parents=True, exist_ok=True)
    lock = work / 'operation.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise PatchError('다른 작업이 진행 중이거나 이전 비정상 종료의 operation.lock이 남았습니다. README 복구 절차를 확인하세요.')
    with os.fdopen(fd, 'w') as f:
        f.write(str(os.getpid()))
    try:
        yield
    finally:
        lock.unlink(missing_ok=True)

def pull_verified(adb, remote, local, expected):
    local = Path(local)
    if local.exists():
        if sha256(local) != expected:
            raise PatchError('기존 PC 백업이 예상 원본과 다릅니다. 덮어쓰지 않습니다: ' + str(local))
        return
    local.parent.mkdir(parents=True, exist_ok=True)
    temp = local.with_name(local.name + '.pull-' + uuid.uuid4().hex[:8])
    try:
        say('원본 백업: ' + local.name)
        adb.run('pull', remote, str(temp), timeout=900)
        if sha256(temp) != expected:
            raise PatchError('PC 원본 백업 체크섬이 다릅니다.')
        temp.rename(local)
    finally:
        temp.unlink(missing_ok=True)

def commit_install(adb, m, pending):
    """Two-phase device commit. Preserve an original, never commit unknown input."""
    main, backup, _ = paths(m)
    if adb.hash(main) != m['source_sha256']:
        raise PatchError('설치 도중 게임 파일이 바뀌었습니다. 교체하지 않습니다.')
    if adb.hash(pending) != m['target_sha256']:
        raise PatchError('기기로 전송한 파일의 체크섬이 다릅니다.')
    old_backup = adb.hash(backup, missing_ok=True)
    if old_backup not in (None, m['source_sha256']):
        raise PatchError('기기의 기존 원본 백업이 다릅니다. 덮어쓰지 않습니다.')
    if old_backup is None:
        adb.shell('mv', main, backup)
    try:
        adb.shell('mv', pending, main)
        if adb.hash(main) != m['target_sha256']:
            raise PatchError('설치 후 체크섬이 다릅니다.')
    except (Exception, KeyboardInterrupt):
        try:
            if adb.exists(main):
                adb.shell('mv', main, main + '.questko-failed-' + uuid.uuid4().hex[:8])
            adb.shell('mv', backup, main)
            if adb.hash(main) != m['source_sha256']:
                raise PatchError('복구 체크섬 실패')
            say('설치 실패 후 원본으로 자동 복구했습니다.')
        except Exception as rollback_error:
            say('자동 복구를 끝내지 못했습니다. 원본 백업 경로: ' + backup)
            say('USB 재연결 후 restore를 실행하세요. 상세: ' + str(rollback_error))
        raise

def install(adb, m, work, root=ROOT):
    version_check(adb, m)
    main, backup, patch = paths(m)
    say('설치 전 체크섬 확인 중...')
    current = adb.hash(main, missing_ok=True)
    if current == m['target_sha256']:
        if adb.hash(backup, missing_ok=True) != m['source_sha256']:
            raise PatchError('한글 수정본은 있지만 기기 원본 백업을 확인하지 못했습니다. PC 백업을 보존하고 status를 확인하세요.')
        say('동일한 수정본이 이미 설치되어 있습니다. 기기를 변경하지 않았습니다.')
        return
    if current != m['source_sha256']:
        raise PatchError('지원하는 원본 main OBB가 아닙니다. status/restore로 상태를 확인하세요.')
    stopped(adb, m)
    if adb.hash(patch) != m['patch_sha256']:
        raise PatchError('patch OBB가 원본과 다릅니다. 설치하지 않습니다.')
    if adb.hash(backup, missing_ok=True) not in (None, m['source_sha256']):
        raise PatchError('다른 원본 백업이 있습니다. 설치하지 않습니다.')
    if shutil.disk_usage(work).free < 12 * 1024**3:
        raise PatchError('작업 폴더가 있는 PC 드라이브에 최소 12GiB 여유 공간이 필요합니다.')
    df, _ = adb.shell('df', '-k', '/sdcard')
    try:
        available = int(df.splitlines()[-1].split()[3]) * 1024
    except (ValueError, IndexError):
        raise PatchError('기기 여유 공간을 확인하지 못했습니다.')
    if available < m['main_bytes'] + 512 * 1024**2:
        raise PatchError('퀘스트에 최소 5GB 여유 공간을 확보하세요.')
    originals = work / 'originals'
    pull_verified(adb, main, originals / m['main_name'], m['source_sha256'])
    pull_verified(adb, patch, originals / m['patch_name'], m['patch_sha256'])
    saved = f'/sdcard/Android/data/{m["package"]}/files/UnrealGame/IntoTheRadius2/IntoTheRadius2/Saved'
    if adb.exists(saved):
        folder = work / ('saves-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:4])
        folder.mkdir()
        say('세이브·설정을 PC로 백업합니다...')
        adb.run('pull', saved, str(folder / 'Saved'), timeout=300)
    output = build(originals / m['main_name'], work / 'generated' / m['main_name'], root)
    stopped(adb, m)
    pending = main + '.questko-upload-' + uuid.uuid4().hex[:8]
    say('검증된 결과를 기기로 전송합니다...')
    try:
        adb.run('push', str(output), pending, timeout=900)
        version_check(adb, m)
        stopped(adb, m)
        commit_install(adb, m, pending)
    finally:
        try:
            if adb.exists(pending):
                adb.shell('rm', pending)
        except Exception:
            say('연결 중단으로 임시 파일이 남을 수 있습니다: ' + pending)
    receipt = {'release': m['release'], 'installed_at': datetime.datetime.now().isoformat(),
               'original_sha256': m['source_sha256'], 'installed_sha256': m['target_sha256'],
               'device_backup': backup}
    (work / 'installation.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    say('설치 완료. APK와 세이브는 변경하지 않았습니다. 헤드셋에서 게임을 실행하세요.')

def restore(adb, m, work):
    version_check(adb, m)
    stopped(adb, m)
    main, backup, patch = paths(m)
    current = adb.hash(main, missing_ok=True)
    if current == m['source_sha256']:
        say('이미 원본 상태입니다. 변경하지 않았습니다.')
        return
    if current not in (None, m['target_sha256']):
        raise PatchError('알 수 없는 파일 또는 업데이트된 파일입니다. 자동 복구로 덮어쓰지 않습니다.')
    if adb.hash(patch) != m['patch_sha256']:
        raise PatchError('patch OBB가 변경되어 자동 복구를 중단합니다.')
    if adb.hash(backup, missing_ok=True) != m['source_sha256']:
        # A verified PC backup can recover a missing device backup.
        local = work / 'originals' / m['main_name']
        if not local.is_file() or sha256(local) != m['source_sha256']:
            raise PatchError('유효한 원본 백업이 없습니다. 다른 버전 파일로 대체하지 마세요.')
        if adb.exists(backup):
            raise PatchError('기기에 알 수 없는 백업 파일이 있습니다. 덮어쓰지 않습니다.')
        pending = backup + '.upload-' + uuid.uuid4().hex[:8]
        adb.run('push', str(local), pending, timeout=900)
        if adb.hash(pending) != m['source_sha256']:
            raise PatchError('복구용 전송 체크섬 오류: ' + pending)
        adb.shell('mv', pending, backup)
    retired = main + '.questko-retired-' + uuid.uuid4().hex[:8]
    if current is not None:
        adb.shell('mv', main, retired)
    try:
        adb.shell('mv', backup, main)
        if adb.hash(main) != m['source_sha256']:
            raise PatchError('복구 후 체크섬이 다릅니다.')
    except (Exception, KeyboardInterrupt):
        if current is not None and not adb.exists(main):
            adb.shell('mv', retired, main)
        raise
    say('원본 복구 완료. 세이브·설정·플레이 진행은 되돌리지 않았습니다.')
    if current is not None:
        say('제거한 패치 파일은 보관되어 있습니다: ' + retired)

def main(argv=None):
    if sys.version_info < (3, 10):
        raise PatchError('Python 3.10 이상이 필요합니다.')
    parser = argparse.ArgumentParser(description='ITR2 Quest 1.2.3 한글패치 — 공개 전 검토본')
    parser.add_argument('command', nargs='?', default='install', choices=['status', 'install', 'restore', 'build', 'verify', 'prepare'])
    parser.add_argument('--adb', help='adb.exe 경로')
    parser.add_argument('--serial', help='대상 ADB 기기')
    parser.add_argument('--work-dir', type=Path, help='백업/생성 작업 폴더. 기본값: 설치 도구 아래 userdata')
    parser.add_argument('--source', type=Path, help='build: 원본 main OBB')
    parser.add_argument('--output', type=Path, help='build: 생성할 main OBB')
    args = parser.parse_args(argv)
    m, _ = load_release()
    say('Into the Radius 2 Quest 한글패치 | 제작: 제콜 | 번역 문자열: refracta/itr2-ko (사용 동의 완료)')
    if args.command == 'prepare':
        say('연결 도구: ' + prepare_adb())
        return 0
    if args.command == 'verify':
        say('패치 데이터/변환 정보 체크섬 정상. 외부 DLL·Python 추가 패키지가 필요 없습니다.')
        return 0
    if args.command == 'build':
        if not args.source or not args.output:
            parser.error('build에는 --source와 --output이 필요합니다.')
        build(args.source, args.output)
        return 0
    adb = connect(args)
    if args.command == 'status':
        status(adb, m)
        return 0
    serial_folder = re.sub(r'[^A-Za-z0-9_.-]', '_', adb.serial)
    work = (args.work_dir or ROOT / 'userdata' / serial_folder / str(m['version_code'])).resolve()
    with operation_lock(work):
        if args.command == 'install':
            install(adb, m, work)
        else:
            restore(adb, m, work)
    return 0

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    try:
        raise SystemExit(main())
    except (PatchError, OSError, subprocess.TimeoutExpired, ValueError, KeyError) as exc:
        print('오류: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
    except KeyboardInterrupt:
        print('중단되었습니다. 파일 교체 도중 연결이 끊겼다면 status/restore를 확인하세요.', file=sys.stderr)
        raise SystemExit(130)
