# Watch Tower

건설 현장 실시간 AI 안전 모니터링 시스템.
카메라 영상을 AI로 분석하여 보호구 미착용, 작업자 쓰러짐, 위험구역 침입, 구역 내 인원 수를 자동 감지하고 즉각 알림을 발송한다.

## 문서 구조

```
docs/
├── getting-started.md    # 설치 및 실행 가이드
├── architecture.md       # 시스템 아키텍처
├── concepts/             # 개념 문서 (요구사항, 설계 결정 등)
│   └── overview.md       # 프로젝트 개요 및 요구사항 정의서
├── research/             # 리서치 및 기술 조사
│   ├── ppe-detection.md
│   ├── fall-detection.md
│   ├── danger-zone-intrusion-research.md
│   ├── pretrained-models.md
│   ├── edge-device-jetson.md
│   ├── realtime-pipeline.md
│   ├── video-streaming-framework.md
│   └── comparison-recommendation.md
└── references/           # 외부 참조 자료, API 문서 등
```

### 문서 작성 규칙

- **concepts/**: 프로젝트 고유 개념, 요구사항, 설계 결정 문서
- **research/**: 기술 조사, 벤치마크, PoC 결과 문서
- **references/**: 외부 API, 라이브러리, 프로토콜 참조 문서
- 새 문서 생성 시 이 섹션의 트리도 함께 업데이트할 것
