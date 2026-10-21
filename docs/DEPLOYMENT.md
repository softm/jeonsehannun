# 배포

정적 파일은 상대 경로를 사용해 `/jeonsehannun/` 경로와 로컬 루트에서 동일하게 동작합니다.

## 실행 및 검증
```
npm run check
npm test
npm start
```

런타임 외부 라이브러리·외부 API 키 없음. 브라우저 테스트는 배포 후 저장·복원까지 별도 검증합니다.

## 독립 프로젝트 Pages
`.github/workflows/pages.yml`은 main push 시 문법·모델 테스트 및 공개 배포 파일 패키징을 수행합니다.
독립 Pages가 활성화된 경우 공식 Pages Actions로 배포합니다. 아직 활성화되지 않았으면 경고 후 배포를 건너뛰며, 테스트 성공을 독립 Pages 배포 성공으로 간주하지 않습니다.
설정: https://github.com/softm/jeonsehannun/settings/pages → Source: GitHub Actions.

## 기존 사용자 Pages를 통한 게시
독립 저장소의 Pages 활성화 권한을 현재 실행 도구에서 사용할 수 없는 경우, 기존 `softm/softm.github.io`의 `jeonsehannun/` 하위에 이 저장소의 테스트를 통과한 정적 파일만 복사·게시합니다. 다른 프로젝트와 기존 사이트 파일은 변경하지 않습니다.
이 경우 운영 URL은 https://softm.github.io/jeonsehannun/ 이며, 소스 저장소의 독립 Pages 활성화와는 구별해야 합니다. 게시된 소스 커밋은 하위 디렉터리의 `release.json`에 기록합니다.

원본 계약서나 개인 기록은 배포 대상이 아닙니다. 배포에는 아래 파일만 포함합니다.
`index.html`, `styles.css`, `app.js`, `model.js`, `store.js`, `data.js`, `data-status.html`, `privacy.html`, `.nojekyll`.

## 데이터 보관
IndexedDB는 서버 동기화가 아닙니다. 같은 출처의 다른 앱과 저장소 보안 경계를 공유합니다. 제품 정식 출시 전 독립 출처, 인증, 사용자별 서버 저장소 및 접근통제 설계·보안 검증이 필요합니다.
