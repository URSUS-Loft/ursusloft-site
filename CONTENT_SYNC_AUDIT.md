# 콘텐츠 동기화 감사 보고서

감사 일자: 2026-07-16  
범위: `C:\dev\scene_director_mvp`의 읽기 전용 소스 조사와 홈페이지의 Privacy, Support, EULA 표시 본문 비교

## 1. 조사 방법과 원본 파일

`C:\dev\scene_director_mvp`는 `pubspec.yaml`의 `flutter` 설정, `lib/` 구조, Flutter 의존성을 가진 실제 Flutter 프로젝트임을 확인했다. 이 감사 중 앱 저장소의 파일은 수정하지 않았고, 앱 저장소의 기존 미추적 `introduction/` 항목도 변경하지 않았다.

앱의 실제 영어 법률 문구와 표시 경로는 다음과 같다.

- `C:\dev\scene_director_mvp\lib\about_legal_localizations.dart`
  - 영어 `privacyPolicyBody`, `eulaBody`, `usageNoticeBody`, 퍼블리셔 표기 원문을 보관한다.
- `C:\dev\scene_director_mvp\lib\main.dart`
  - Settings → About / Legal 화면에서 위 문자열을 `Text` 위젯으로 표시한다. 앱 버전(`0.9.0`), 제작자(`BEAR Works`), 퍼블리셔(`URSUS Loft`), Help, Final Prompt, New Prompt, 자동 저장 및 프리셋 UI의 실제 동작도 여기에 있다.
- `C:\dev\scene_director_mvp\lib\session_storage.dart`
  - 마지막 세션을 `%APPDATA%\Scene Director\last_session.json`에 저장·복원한다.
- `C:\dev\scene_director_mvp\lib\preset_storage.dart`
  - 프리셋을 `%APPDATA%\Scene Director\presets.json`에 저장·불러오기·삭제한다.
- `C:\dev\scene_director_mvp\pubspec.yaml`
  - 패키지 버전 `0.9.0+1`을 확인했다.

홈페이지에서는 다음의 사용자 표시 본문을 비교했다.

- `privacy/scene-director.html`
- `support/scene-director.html`
- `legal/scene-director-eula.html`

앱의 Dart·문서·텍스트·JSON/ARB/Markdown/HTML 후보를 `Privacy`, `EULA`, `Legal`, `Support`, `Help`, 회사 표기, 이메일·URL, 저장·세션·프리셋·참조 이미지 관련 키워드로 읽기 전용 검색했다. 공식 지원 이메일과 앱 화면에서 사용하는 외부 URL은 발견하지 못했다.

## 2. 앱 Privacy Policy의 실제 상태

앱의 실제 영어 Privacy Policy는 `about_legal_localizations.dart`의 `en.privacyPolicyBody`이며 Settings → About / Legal에서 그대로 표시된다. 요지는 다음과 같다.

- 운영·배포 주체는 `URSUS Loft`, 제작자 브랜드는 `BEAR Works`이다.
- 사용자 계정과 개발자 서버를 운영하지 않는다.
- 참고 이미지, 프롬프트, 프리셋, 세션 데이터, 프로젝트 설정을 URSUS Loft, BEAR Works 또는 다른 외부 서버로 전송하지 않는다.
- 참고 이미지는 로컬 미리보기와 프롬프트 정리를 위해 사용자 기기에서 선택한다.
- 마지막 세션과 프리셋은 `%APPDATA%\Scene Director`에 저장된다.
- 저장 파일은 텍스트·설정·참고 이미지 역할을 저장하지만, 참고 이미지 파일·파일명·파일 경로는 저장하지 않는다.
- 로컬 파일을 지우면 저장된 세션 또는 프리셋 설정이 삭제된다. Windows 제거/앱 삭제 시 AppData 파일의 완전한 제거는 보장하지 않는다.
- Microsoft Store, Windows, 사용자가 선택한 외부 AI 서비스는 각자 정책으로 데이터를 처리하며, URSUS Loft/BEAR Works는 이를 통제하지 않는다.

구현도 이 설명을 뒷받침한다. `buildSessionData()`에는 텍스트·설정·`referenceImageRoles`만 포함되고 `referenceImagePaths`는 포함되지 않는다. 이미지 파일은 `file_picker`로 단일 선택하여 메모리의 `referenceImagePaths`에만 유지하고, 세션 파일에는 쓰지 않는다.

시행일, 개인정보 담당 연락처, 분석·오류 로그·보안 방식·아동 개인정보의 구체 정책은 앱의 실제 영문 본문에 없다.

## 3. 홈페이지 Privacy Policy와의 차이

홈페이지 Privacy Policy는 앱 원문을 반영하지 않는 초안이다.

| 비교 항목 | 앱의 실제 문구/구현 | 홈페이지 표시 본문 | 판단 |
| --- | --- | --- | --- |
| 운영 주체 | URSUS Loft 운영·배포, BEAR Works 제작자 브랜드 | 운영 주체 미기재 | 홈페이지 누락 |
| 수집·외부 전송 | 계정·개발자 서버 없음, 지정 데이터의 외부 전송 없음 | 명시 없음 | 홈페이지의 핵심 누락 |
| 참고 이미지 | 로컬 선택·미리보기·정리, 파일/이름/경로 미저장 | 역할·프롬프트 정리만 언급 | 저장 제외 사항 누락 |
| 프롬프트·설정 | 로컬 JSON에 텍스트·설정·역할 저장 | “may be stored locally”, 최종 문서에서 확정 예정 | 실제 구현과 불일치하는 불확정 표현 |
| 저장 위치·보관 | `%APPDATA%\Scene Director`, 로컬 파일 삭제 시 설정 삭제, uninstall 완전 삭제 미보장 | “Details … will be confirmed” | 홈페이지 누락 |
| Microsoft/외부 서비스 | 각자 정책 적용, URSUS Loft/BEAR Works 비통제 | 별도 서비스라는 일반 설명 | 일부 일치, 통제 범위 누락 |
| 로그·분석/보안/아동 | 앱 문구에 구체 선언 없음 | 모두 추후 확정 또는 일반 문장 | 홈페이지가 앱보다 더 많은 정책을 암시하나 근거 없음 |
| 연락처·시행일 | 없음 | “before release” | 둘 다 확정 정보 없음 |
| 변경 정책 | 없음 | 업데이트 가능·중요 변경 반영 | 앱 원문에 없는 홈페이지 단독 문구 |

## 4. 앱 EULA의 실제 상태

앱의 실제 표시 제목은 `Terms of Use`이며, 영문 전문은 `en.eulaBody`다. 별도 파일형 EULA나 시행일·버전이 있는 긴 계약서는 발견하지 못했다. 실제 문구는 다음 범위로 제한된다.

- URSUS Loft가 Scene Director를 제공·배포하고 BEAR Works가 제작자 브랜드임을 밝힌다.
- 앱은 로컬 프롬프트 작성과 참고 자료 정리 도구이며 이미지 생성 서비스가 아니라고 설명한다.
- 외부 AI 서비스·모델·가용성·정책·생성 결과는 앱의 통제 밖이라고 밝힌다.
- 사용자는 참고 이미지, 캐릭터, 로고, 상표, 프롬프트의 권리·허가를 확인할 책임이 있다.
- 외부 AI 서비스 이용에는 해당 서비스의 약관·개인정보처리방침이 적용된다.
- Microsoft Store가 처리하는 배포·구매·라이선스·환불은 해당 Store 약관·정책이 적용된다.

앱 원문에는 계약 당사자의 정식 법인명, 라이선스 허여 범위, 상업적 사용, 복제·재배포·양도·리버스 엔지니어링, 소유권 조항, 업데이트, 보증 부인, 책임 제한, 종료, 관할법, 연락처, 시행일을 정한 구체 조항이 없다.

## 5. 홈페이지 EULA와의 차이

홈페이지 EULA는 13개 제목을 갖췄지만 모든 핵심 조항이 “final agreement will …”이라는 자리표시자다. 앱에 표시되는 실제 Terms of Use 전문을 인용·요약하지 않는다.

- 앱에 있는 외부 AI 서비스의 비통제, 사용자의 권리·허가 책임, Microsoft Store의 배포·구매·라이선스·환불 정책 적용이 홈페이지에서 누락됐다.
- 홈페이지의 License grant, Permitted use, Restrictions, Ownership, Updates, warranty, liability, termination, governing law 제목은 앱에는 없는 내용이므로 현재 웹에서 사실로 확정할 수 없다.
- 홈페이지가 “released application에서 제시되는 final agreement”라고 말하지만 현재 앱은 이미 `Terms of Use` 본문을 표시한다. 최종 법률 계약이 아니라는 점을 안내하는 목적은 이해되나, 앱 표시 문서와 동기화된 공식 문서로는 사용할 수 없다.

## 6. 앱 Support/Help의 실제 상태

앱에는 별도 외부 Support 문서는 없지만 실제 Help 모달과 메뉴가 있다.

- 상단 메뉴: `New Prompt`, `Save Preset`, `Load Preset`, `Delete Preset`, Settings.
- 하단 상태: `Auto saved`, `Last saved: just now`.
- 사이드바: `Project Type`, `Character`, `Multi-Character`, `Camera`, `Pose`, `Face`, `Costume`, `Environment`, `Rendering`, `Additional Instructions`.
- Help 모달: `Reference Images`, 위 섹션들, `Final Prompt (English)`, `Composition Preview`.
- Reference Images Help: 앱이 이미지를 업로드하거나 자동 분석하지 않으며, 외부 AI 도구에 같은 참조 이미지를 표시된 순서대로 첨부해야 하고, 각 이미지에 명확한 역할을 지정해야 한다. 빈 슬롯과 `Role Required` 이미지는 Final Prompt/Compact Prompt에서 제외된다.
- Final Prompt Help: 현재 설정으로 만든 상세 영문 프롬프트이고, 같은 참조 이미지를 같은 순서로 외부 AI 이미지 생성 도구에 복사한다. Final Prompt는 영어 전용이며 Compact Prompt보다 상세하고, 앱은 최종 이미지를 직접 생성하지 않는다.
- 세션은 상태 변경 때 자동 저장되고 앱 시작 시 복원된다. `New Prompt`는 현재 작업공간을 기본값으로 초기화하되 저장된 프리셋은 삭제하지 않는다.
- 프리셋은 이름으로 저장하며 같은 이름이면 갱신된다. 불러오기 후 마지막 세션도 저장하고, 삭제 기능도 있다.
- `pubspec.yaml`과 UI의 제품 상태상 확인된 지원 플랫폼은 Windows이다.

## 7. 홈페이지 Support와의 차이

| 비교 항목 | 앱 실제 상태 | 홈페이지 Support | 판단 |
| --- | --- | --- | --- |
| 기본 작업 순서 | 프로젝트 유형 → 참조 이미지/역할 → 설정 → Final Prompt/Compact Prompt → 외부 도구 | 거의 같은 순서 | 대체로 일치 |
| 메뉴 이름 | `New Prompt`, `Save Preset`, `Load Preset`, `Delete Preset`, `Settings` | 메뉴 이름 없음 | 홈페이지 누락 |
| 참조 이미지 역할·순서 | 역할 선택, 빈/Role Required 제외, 외부 도구의 정확한 같은 순서 요구 | 역할·순서는 언급 | Role Required/제외 규칙 누락 |
| Final Prompt | 상세 영문, Compact Prompt보다 상세, 영어 전용 | “assembled final prompt”만 언급 | 핵심 특성 누락 |
| 프리셋·세션 | 실제 자동 저장·복원·저장/불러오기/삭제 구현 | “will be described in final release documentation” | 실제 기능과 직접 충돌하는 미구현/불확정 표현 |
| 초기화 | New Prompt는 현재 작업공간 기본값 복원, 프리셋 보존 | 없음 | 홈페이지 누락 |
| 플랫폼 | Windows | 없음 | 홈페이지 누락 |
| 외부 생성 서비스 | 앱은 생성·자동 업로드·자동 분석하지 않음 | 생성하지 않고 사용자가 별도로 선택한다고 설명 | 대체로 일치, 자동 분석 부재 누락 |

## 8. 홈페이지에만 존재하는 임의 또는 근거 없는 문구

다음은 앱의 실제 영문 원문에서 근거를 찾지 못했거나, 앱 원문보다 앞서 확정 여부를 암시하는 홈페이지 문구다.

- Privacy의 “final release documentation will provide/confirm …” 계열 문장(저장 세부사항, 보안, 아동 개인정보).
- Privacy의 “Material updates will be reflected on this page.”
- EULA의 모든 “final agreement will …” 계약 조항과 법률 문서 구조.
- EULA의 “Final legal review is required before release.”
- Support의 “Saving behavior and available options will be described in the final release documentation.”

이 문구들은 향후 계획 안내로는 가능하지만 앱의 공식 표시 문서와 일치하는 Privacy/EULA/Support 본문으로 취급할 수 없다.

## 9. 앱에만 존재하고 홈페이지에서 누락된 문구

- “Scene Director does not operate user accounts or developer servers.”
- 지정 데이터(참조 이미지, 프롬프트, 프리셋, 세션 데이터, 프로젝트 설정)를 어떤 외부 서버에도 전송하지 않는다는 명시.
- `%APPDATA%\Scene Director`의 `last_session.json`, `presets.json` 저장 사실과 이미지 파일·파일명·경로 미저장.
- 로컬 파일 삭제와 uninstall 후 AppData 잔존 가능성.
- 실제 앱 버전 `0.9.0`(패키지 `0.9.0+1`), `Created in Korea`, 저작권 표기.
- 외부 AI 결과·서비스 정책·가용성은 앱 통제 밖이라는 EULA 문구, 사용자의 권리·허가 확인 책임, Microsoft Store 환불·라이선스 정책 적용.
- Final Prompt의 영어 전용/Compact Prompt보다 상세함, 빈·Role Required 슬롯 제외.
- 자동 세션 저장·복원, 프리셋 저장·불러오기·삭제, New Prompt의 프리셋 보존.

## 10. 서로 직접 충돌하는 문구

엄격한 의미에서 “A라고 단정” 대 “not A라고 단정”의 직접 반대 문구는 발견하지 못했다. 다만 사용자에게 실제 기능을 잘못 전달하는 중대한 불일치가 있다.

1. 홈페이지 Support는 프리셋·세션 기능을 추후 문서에서 설명할 기능처럼 표현하지만, 앱은 자동 저장·복원과 Save/Load/Delete Preset을 이미 제공한다.
2. 홈페이지 Privacy는 로컬 저장 세부사항을 추후 확정한다고 하지만 앱은 저장 위치, 저장 항목, 저장하지 않는 항목을 이미 구체적으로 밝히고 구현한다.
3. 홈페이지 EULA는 최종 계약이 향후 제시될 것처럼 보이지만, 앱은 현재 사용자에게 Terms of Use를 이미 표시한다. 웹의 계약 조항은 앱에 없는 내용이라 동기화되어 있지 않다.

## 11. 시행일, 회사명, 이메일, URL의 불일치

- 회사명: 앱은 `URSUS Loft`를 운영·배포 주체로, `BEAR Works`를 creator brand로 명시한다. 홈페이지 Privacy/EULA 본문은 이 표기를 누락한다. Support는 회사명과 모순되지는 않지만 본문에서 주체를 명시하지 않는다.
- 홈페이지 제품 페이지에만 `Created by BEAR Works` / `Published by URSUS Loft`가 있으나, 법률 문서에는 앱과 같은 문구가 없다.
- 시행일: 앱과 홈페이지 모두 확정 시행일이 없다.
- 이메일: 앱과 홈페이지 모두 공식 지원 이메일이 없다. 홈페이지의 “available before release”는 주소가 아니다.
- URL: 앱 화면에서 사용하는 공식 지원·개인정보·법률 URL은 발견하지 못했다. 홈페이지 외부 링크도 없다.
- 버전: 앱 UI `0.9.0`, 패키지 `0.9.0+1`; 홈페이지 문서에는 버전 식별자가 없다.

## 12. 공식 원본 제안

현재 사용자에게 실제 표시되는 Privacy/Terms 문구의 즉시 원본은 `lib/about_legal_localizations.dart`의 영어 `privacyPolicyBody` 및 `eulaBody`로 삼는 것이 적절하다. `lib/main.dart`는 그 문자열이 실제 화면에 조립·표시되는 근거다.

다만 이 앱 원문은 완성된 장문 법률 계약이 아니라 현재의 간결한 안내문이다. 출시 전 정식 Privacy Policy/EULA가 필요하다면 다음 순서를 권장한다.

1. 법률·운영 사실을 확정한다.
2. 확정된 영문 원문을 앱의 `about_legal_localizations.dart`에 먼저 반영하고 모든 번역을 동기화한다.
3. 같은 승인 원문을 홈페이지에 반영한다.
4. 시행일·연락처·공식 URL을 두 매체에 같은 값으로 추가한다.

## 13. 동기화가 필요한 파일 목록

이번 감사 단계에서는 아래 파일을 수정하지 않았다. 다음 동기화 단계의 대상이다.

- 홈페이지: `privacy/scene-director.html`
- 홈페이지: `support/scene-director.html`
- 홈페이지: `legal/scene-director-eula.html`
- 앱 공식 원문: `C:\dev\scene_director_mvp\lib\about_legal_localizations.dart`
- 앱 표시·지원 설명 근거: `C:\dev\scene_director_mvp\lib\main.dart`
- 앱 저장 관련 사실 근거: `C:\dev\scene_director_mvp\lib\session_storage.dart`, `C:\dev\scene_director_mvp\lib\preset_storage.dart`

앱의 법률 문서 자체도 정식 계약으로 배포할 계획이라면, 위 원문 파일의 Privacy/EULA를 먼저 확정·보강할 필요가 있다. 현재 웹사이트만을 앱 화면과 일치시키는 목적이라면 앱의 현행 영어 원문을 기준으로 웹의 세 문서를 동기화하는 것이 우선이다.

## 동기화 완료 기록 (2026-07-16)

- 홈페이지 Privacy 본문은 `C:\dev\scene_director_mvp\lib\about_legal_localizations.dart`의 영어 `privacyPolicyBody` 문장을 문단 구조만 바꾸어 동일하게 반영했다.
- 홈페이지 Terms of Use 본문은 같은 파일의 영어 `eulaBody` 문장을 문단 구조만 바꾸어 동일하게 반영했다. 기존 URL `legal/scene-director-eula.html`은 호환성을 위해 유지하고, 화면 제목·메타데이터·링크 표기는 Terms of Use로 바꿨다.
- Support에는 `lib/main.dart`, `lib/session_storage.dart`, `lib/preset_storage.dart`에서 확인한 Project Type, Reference Images/roles/order, Final Prompt·Compact Prompt, New Prompt, 자동 마지막 세션 저장·복원, 프리셋 저장·불러오기·삭제, Windows, 실제 저장 경로를 반영했다.
- 앱에서 확인되지 않은 공식 지원 이메일과 최종 Microsoft Store URL은 추가하지 않았다. GitHub Pages 실제 게시 상태, Spaceship DNS, 최종 Open Graph 이미지는 여전히 별도 확인이 필요하다.
- 동기화의 원본은 `C:\dev\scene_director_mvp\lib\about_legal_localizations.dart`, 기능 근거는 `C:\dev\scene_director_mvp\lib\main.dart`, `lib\session_storage.dart`, `lib\preset_storage.dart`다.

## 개발·운영 주체 정정 기록 (2026-07-16)

- Scene Director의 개발·운영·배포·퍼블리싱 주체는 `URSUS Loft`로 통일했다.
- `BEAR Works`는 별도 회사, 개발사, 퍼블리셔 또는 개인정보 처리 주체가 아닌 creator credit으로만 표기한다.
- 앱의 Privacy Policy와 Terms of Use 원문 및 지원 언어 번역은 `C:\dev\scene_director_mvp\lib\about_legal_localizations.dart`에서 수정했다. About / Legal 화면의 표시 순서는 `C:\dev\scene_director_mvp\lib\main.dart`에서 URSUS Loft의 개발·퍼블리싱 표기를 먼저, BEAR Works creator credit을 다음으로 표시하도록 수정했다.
- 홈페이지의 동기화 원본은 `privacy\scene-director.html`, `legal\scene-director-eula.html`이며, 제품 페이지의 제한된 creator credit 표기는 `products\scene-director.html`과 `assets\css\styles.css`에서 수정했다.
