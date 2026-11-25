# Into the Radius 2 Quest 한글패치

> **설치는 [ZECOLE VR 런처](https://github.com/zecole-vr/zecole-launcher)로 하세요.**  
> 런처 하나로 이 한글패치를 설치·업데이트·원본 복구할 수 있습니다. → **[ZECOLE_Launcher.exe 받기](https://github.com/zecole-vr/zecole-launcher/releases/latest/download/ZECOLE_Launcher.exe)** (설치 없이 바로 실행)

**Meta Quest · Standalone**용 비공식 한글패치입니다.

- 패치 버전: **1.2.5**
- 지원 게임: **1.2.5 (483352)**
- Android 설치 도구 버전: **1.0.0**

## 다운로드

게임은 두 설치 방법 모두 **Quest 단독판**입니다. 사용할 기기에 맞는 파일을 받으세요. 로그인 없이 내려받을 수 있습니다.

| 설치에 사용할 기기 | 설치 파일 | 상세 안내 |
| --- | --- | --- |
| Windows PC | [ITR2_Quest_v1.2.5.exe](https://github.com/zecole-vr/IntoTheRadius2-Quest-KoreanPatch/releases/download/v1.2.5/ITR2_Quest_v1.2.5.exe) | [Windows 설치·복구](설치방법.txt) |
| Android 휴대폰 | [ITR2_Quest_Android_v1.2.5.zip](https://github.com/zecole-vr/IntoTheRadius2-Quest-KoreanPatch/releases/download/v1.2.5/ITR2_Quest_Android_v1.2.5.zip) | [휴대폰 설치·복구](설치방법_Android.txt) |

각 파일의 SHA-256 체크섬은 [같은 릴리스](https://github.com/zecole-vr/IntoTheRadius2-Quest-KoreanPatch/releases/tag/v1.2.5)의 `.sha256` 파일에서 확인할 수 있습니다. GitHub의 **Source code ZIP은 설치본이 아닙니다.**

## 번역 출처 및 제작

[refracta/itr2-ko PCVR 한글패치](https://github.com/refracta/itr2-ko) 제작자의 동의를 받아 번역 문자열을 사용하여 Quest 버전으로 제작했습니다. 도움에 감사드립니다.

Quest 버전 제작: **VR 유튜브 크리에이터 제콜 (ZECOLE)**  
유튜브: [youtube.com/@zecole](https://www.youtube.com/@zecole)

## Windows PC로 설치

Windows 10/11 64비트 PC, Microsoft Edge WebView2 Runtime, 지원 버전의 게임이 설치된 Quest, USB 데이터 케이블을 준비해 주세요. PC에는 최소 12GiB, Quest에는 최소 5GB의 여유 공간이 필요합니다.

1. [릴리스](https://github.com/zecole-vr/IntoTheRadius2-Quest-KoreanPatch/releases)에 첨부된 **ITR2_Quest_v1.2.5.exe**를 내려받아 실행합니다. 압축 해제는 필요 없습니다. GitHub의 Source code ZIP은 설치본이 아닙니다.
2. Quest의 개발자 모드를 켜고 게임을 완전히 종료합니다.
3. Quest를 PC에 USB로 연결하고 헤드셋에서 **USB 디버깅을 허용**합니다.
4. **한글패치 설치 / 업데이트** 버튼을 누릅니다.
5. 완료 안내 후 게임을 실행합니다. 한국어를 따로 선택할 필요는 없습니다.

Python이나 SideQuest를 별도로 설치할 필요는 없습니다. ADB가 없으면 약관 동의 후 자동 다운로드하며 이때 인터넷 연결이 필요합니다. WebView2가 없다면 [Microsoft 공식 페이지](https://developer.microsoft.com/microsoft-edge/webview2/)에서 Runtime을 설치해 주세요.

설치 중에는 USB 케이블을 분리하거나 게임을 실행하지 마세요. 일부 문구는 영어로 표시될 수 있습니다.

런처를 실행하거나 **다시 확인**을 누르면 GitHub의 최신 정식 버전을 확인합니다. 새 버전이 있으면 **최신 설치본 받기** 버튼으로 다운로드 페이지를 열고, 새 EXE를 내려받아 실행해 주세요. 기존 EXE의 자동 다운로드·교체 기능은 없습니다.

## Windows PC에서 제거 · 원본 복구

1. 게임을 완전히 종료하고 Quest를 PC에 USB로 연결합니다.
2. USB 디버깅을 허용한 뒤 설치에 사용한 EXE를 실행합니다.
3. **제거 · 원본 복구** 버튼을 누릅니다.
4. 완료 안내 후 게임을 실행합니다.

게임 파일을 원본으로 복구하며 세이브 진행 상황은 되돌리지 않습니다. 지원 버전과 유효한 원본 백업이 필요합니다.

백업 및 설치 기록: **%LOCALAPPDATA%\ZECOLE\ITR2QuestPatch\userdata**  
%LOCALAPPDATA%는 현재 Windows 사용자의 AppData\Local 폴더입니다. EXE를 옮기거나 다시 내려받아도 기록과 백업은 유지됩니다. **설치·복구 안내 → 백업 폴더 열기**에서 확인할 수 있습니다.

기존 ZIP 설치본의 userdata 백업은 자동 이전되지 않으므로 보관해 주세요. 기존 ZIP으로 설치한 패치를 복구해야 한다면 해당 ZIP의 복구 도구와 백업을 사용해 주세요.

## Android 휴대폰으로 설치 · 복구

PC 없이 Android 휴대폰과 Quest를 USB 데이터 케이블로 직접 연결하여 설치합니다. USB OTG/호스트 기능을 지원하는 휴대폰과 별도 앱 [Bugjaeger](https://play.google.com/store/apps/details?id=eu.sisik.hackendebug)가 필요합니다. iPhone은 지원하지 않습니다.

Quest 여유 공간은 원본 백업이 없으면 **9GB 이상**, 유효한 백업이 있으면 **5GB 이상** 필요하며 휴대폰에는 30MB 이상을 권장합니다. 다운로드·앱 준비에 인터넷이 필요하고, 파일 전송 후 패치 작업은 오프라인으로 가능합니다. Python, PC용 ADB, Java를 따로 설치하지 않습니다.

1. 휴대폰에 Android용 ZIP과 Bugjaeger를 받습니다.
2. Quest의 게임을 완전히 종료하고 개발자 모드를 켭니다. 휴대폰과 Quest를 연결한 뒤 휴대폰의 USB 접근 및 Quest의 USB 디버깅 요청을 허용합니다.
3. Bugjaeger로 ZIP을 Quest의 `/sdcard/Download/`에 전송합니다.
4. [휴대폰용 상세 설치 안내](설치방법_Android.txt)의 명령을 순서대로 복사해 압축 해제와 파일 검사를 진행합니다.
5. `install` 명령 실행 후 `log`에서 `RESULT=INSTALLED` 또는 `RESULT=ALREADY_INSTALLED`와 `END install`을 확인합니다. **STARTED는 작업 시작 표시이며 완료가 아닙니다.**
6. 완료 후 게임을 실행합니다. 한국어를 따로 선택할 필요는 없습니다.

복구할 때는 같은 안내의 `restore` 명령을 실행하고, 로그에서 `RESULT=RESTORED` 또는 `RESULT=ALREADY_ORIGINAL`과 `END restore`를 확인합니다. 게임 파일을 원본으로 복구하며 세이브 진행 상황은 되돌리지 않습니다.

원본 백업과 모바일 설치 기록은 **Quest의 게임 데이터 폴더**에 보관됩니다. ZIP을 옮기거나 다시 받아도 유지되지만 게임을 삭제하면 함께 사라질 수 있으므로 백업을 임의로 지우지 마세요. 정확한 경로와 중단 시 점검 방법은 상세 안내에 있습니다.

Windows의 설치 기록은 자동 이전되지 않습니다. 같은 1.2.5 패치와 유효한 원본 백업이 Quest에 있다면 모바일 `install`로 파일을 검증하고 모바일 기록을 만든 뒤 `restore`를 사용할 수 있습니다. 휴대폰용에는 자동 업데이트 기능이 없으며, 새 버전이 나오면 해당 ZIP과 안내를 다시 받아 주세요.

## 게임 업데이트 안내

**게임 버전이 바뀌면 해당 버전용 한글패치가 업데이트되기 전까지 이용할 수 없습니다.** 게임 업데이트 후에는 이전 버전의 패치나 복구 도구를 적용하지 마세요.

## 폰트 저작권

사용 폰트: **Noto Sans KR**  
Copyright 2014–2021 Adobe. Reserved Font Name: “Source”.  
라이선스: **SIL Open Font License 1.1 (OFL)**.

폰트와 수정본의 저작권 고지 및 라이선스 전문은 [licenses/NotoSansKR-OFL.txt](licenses/NotoSansKR-OFL.txt)에 포함되어 있습니다. EXE에도 포함되어 있으며 **설치·복구 안내 → 출처 · 라이선스 보기**로 열 수 있습니다. Android ZIP에도 `NotoSansKR-OFL.txt`를 동봉했습니다. 런처의 Windows 시스템 글꼴 파일은 재배포하지 않습니다.

기타 구성 요소의 고지는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)를 참고해 주세요.

## 이번 버전

- Quest 단독판 **1.2.5 (483352)**에 대응합니다.
- 기존 한글 번역과 적 음성 자막을 포함합니다.
- Android 휴대폰에서 USB로 설치·복구하는 배포판을 추가했습니다.
- Windows와 휴대폰용 설치·복구 안내를 구분했습니다.

문의: [버그 제보 / 수정 요청](https://github.com/zecole-vr/IntoTheRadius2-Quest-KoreanPatch/issues/new)
