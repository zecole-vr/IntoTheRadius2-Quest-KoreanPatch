# Into the Radius 2 Quest 한글패치

**Meta Quest · Standalone**용 비공식 한글패치입니다.

- 패치 버전: **1.2.4-rc.2 — 공개 전 검토본**
- 지원 게임: **1.2.4 (480012)**
- 설치 파일: **ITR2_Quest_v1.2.4-rc.2.exe**

현재 설치본은 비공개 저장소의 릴리스에 첨부된 EXE입니다. 저장소 접근 권한이 있는 사용자만 이용할 수 있습니다.

## 번역 출처 및 제작

[refracta/itr2-ko PCVR 한글패치](https://github.com/refracta/itr2-ko) 제작자의 동의를 받아 번역 문자열을 사용하여 Quest 버전으로 제작했습니다. 도움에 감사드립니다.

Quest 버전 제작: **VR 유튜브 크리에이터 제콜 (ZECOLE)**  
유튜브: [youtube.com/@zecole](https://www.youtube.com/@zecole)

## 설치 방법

Windows 10/11 64비트 PC, Microsoft Edge WebView2 Runtime, 지원 버전의 게임이 설치된 Quest, USB 데이터 케이블을 준비해 주세요. PC에는 최소 12GiB, Quest에는 최소 5GB의 여유 공간이 필요합니다.

1. [릴리스](https://github.com/zecole-vr/IntoTheRadius2-Quest-KoreanPatch/releases)에 첨부된 **ITR2_Quest_v1.2.4-rc.2.exe**를 내려받아 실행합니다. 압축 해제는 필요 없습니다. GitHub의 Source code ZIP은 설치본이 아닙니다.
2. Quest의 개발자 모드를 켜고 게임을 완전히 종료합니다.
3. Quest를 PC에 USB로 연결하고 헤드셋에서 **USB 디버깅을 허용**합니다.
4. **한글패치 설치 / 업데이트** 버튼을 누릅니다.
5. 완료 안내 후 게임을 실행합니다. 한국어를 따로 선택할 필요는 없습니다.

Python이나 SideQuest를 별도로 설치할 필요는 없습니다. ADB가 없으면 약관 동의 후 자동 다운로드하며 이때 인터넷 연결이 필요합니다. WebView2가 없다면 [Microsoft 공식 페이지](https://developer.microsoft.com/microsoft-edge/webview2/)에서 Runtime을 설치해 주세요.

설치 중에는 USB 케이블을 분리하거나 게임을 실행하지 마세요. 일부 문구는 영어로 표시될 수 있습니다.

현재 저장소와 릴리스는 공개 전 상태이므로 온라인 최신 버전 확인이 실패할 수 있습니다. 이는 기기 연결 상태나 설치 여부와 별개입니다.

## 제거 · 원본 복구

1. 게임을 완전히 종료하고 Quest를 PC에 USB로 연결합니다.
2. USB 디버깅을 허용한 뒤 설치에 사용한 EXE를 실행합니다.
3. **제거 · 원본 복구** 버튼을 누릅니다.
4. 완료 안내 후 게임을 실행합니다.

게임 파일을 원본으로 복구하며 세이브 진행 상황은 되돌리지 않습니다. 지원 버전과 유효한 원본 백업이 필요합니다.

백업 및 설치 기록: **%LOCALAPPDATA%\ZECOLE\ITR2QuestPatch\userdata**  
%LOCALAPPDATA%는 현재 Windows 사용자의 AppData\Local 폴더입니다. EXE를 옮기거나 다시 내려받아도 기록과 백업은 유지됩니다. **설치·복구 안내 → 백업 폴더 열기**에서 확인할 수 있습니다.

기존 ZIP 설치본의 userdata 백업은 자동 이전되지 않으므로 보관해 주세요. 기존 ZIP으로 설치한 패치를 복구해야 한다면 해당 ZIP의 복구 도구와 백업을 사용해 주세요.

## 게임 업데이트 안내

**게임 버전이 바뀌면 해당 버전용 한글패치가 업데이트되기 전까지 이용할 수 없습니다.** 게임 업데이트 후에는 이전 버전의 패치나 복구 도구를 적용하지 마세요.

## 폰트 저작권

사용 폰트: **Noto Sans KR**  
Copyright 2014–2021 Adobe. Reserved Font Name: “Source”.  
라이선스: **SIL Open Font License 1.1 (OFL)**.

폰트와 수정본의 저작권 고지 및 라이선스 전문은 [licenses/NotoSansKR-OFL.txt](licenses/NotoSansKR-OFL.txt)에 포함되어 있습니다. EXE에도 포함되어 있으며 **설치·복구 안내 → 출처 · 라이선스 보기**로 열 수 있습니다. 런처의 Windows 시스템 글꼴 파일은 재배포하지 않습니다.

기타 구성 요소의 고지는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)를 참고해 주세요.

## 이번 버전

- ZIP 압축 해제 없이 실행하는 단일 EXE 설치 프로그램을 제공합니다.
- 적 음성 자막을 추가하고 일부 대사를 수정했습니다.
- 설치·제거 안내와 백업 경로 표시를 정리했습니다.

새 EXE의 실제 Quest 설치·업데이트·제거 및 최종 자막 플레이 검증이 남아 있는 검토본입니다. [검증 상태](VALIDATION.md)

문의: [버그 제보 / 수정 요청](https://github.com/zecole-vr/IntoTheRadius2-Quest-KoreanPatch/issues/new)
