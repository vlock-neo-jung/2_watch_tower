# Zone 침입 감지 검증 계획 — 전체 개요

## 이 작업이 왜 필요한가

Watch Tower의 핵심 기능 중 하나가 **위험구역 침입 감지**다.
건설 현장에는 크레인 회전 반경, 개구부 주변, 중장비 작업 구역 등 사람이 들어가면 안 되는 영역이 있다.
이 기능은 카메라 영상에서 사람을 찾고, 미리 정해둔 위험구역 안에 들어왔는지 판단해서 알림을 보내는 것이다.

현재 Phase 2에서 "사람을 찾고 추적하는 것"은 검증이 진행 중이다(SODA 파인튜닝).
그 사이에 **위험구역 판정 로직 자체**를 미리 검증할 수 있다.
모델이 사람을 찾아주면, 그 다음 단계인 "이 사람이 위험구역 안에 있는가?"는 순수한 기하학 계산이기 때문이다.

## 핵심 아이디어: 레이어별 분리 평가

위험구역 침입 감지는 한 덩어리가 아니라 **4개 레이어**가 쌓여서 동작한다:

```
Layer 1: Detection — 영상에서 사람을 찾는다
Layer 2: Tracking  — 같은 사람에게 같은 ID를 부여한다
Layer 3: Zone Logic — 그 사람의 위치가 위험구역 안인지 계산한다
Layer 4: Temporal Logic — N프레임 연속으로 안에 있을 때만 이벤트로 판정한다
```

각 레이어에서 오류가 발생할 수 있다:
- Layer 1 오류: 사람을 못 찾음 → 침입을 놓침
- Layer 2 오류: ID가 바뀜 → 같은 사람을 새 사람으로 봄 → 중복 알림
- Layer 3 오류: 경계선 근처에서 안/밖 판정이 흔들림 → 깜빡이는 오탐
- Layer 4 오류: 임계값이 너무 높으면 빠른 침입을 놓침, 너무 낮으면 오탐 증가

**Layer 1, 2는 이미 Phase 2에서 검증 중**이다.
이 계획은 **Layer 3, 4를 독립적으로 검증**하고, 마지막에 전체를 합쳐서 end-to-end 평가하는 것이다.

## 평가 방법론: 왜 이렇게 하는가

위험구역 침입 감지의 정확도를 측정하는 **업계 표준이 존재하지 않는다**.
상용 제품(viAct, Voxel AI 등)도 측정 방법을 공개하지 않는다.
유일한 전용 벤치마크는 영국 정부의 i-LIDS(Imagery Library for Intelligent Detection Systems)인데, 접근이 제한적이다.

그래서 우리는:
1. **Zone Logic** → 합성 데이터로 단위 테스트 (모델 필요 없음)
2. **End-to-End** → i-LIDS의 프로토콜만 차용하여 자체 평가
   - 핵심: **event-level 평가** (프레임 단위가 아님)
   - "침입이 시작된 후 N초 이내에 시스템이 알람을 발생시켰는가?"

## 단계 구성

| 단계 | 내용 | 모델 필요 | 의존 관계 |
|------|------|-----------|----------|
| [Step 1](./01-zone-logic-unit-test.md) | Zone Logic 단위 테스트 | 불필요 | 없음 |
| [Step 2](./02-zone-config-schema.md) | Zone 설정 스키마 + 로드/검증 코드 | 불필요 | 없음 |
| [Step 3](./03-event-gt-preparation.md) | 어노테이션 도구 + GT 준비 | 불필요 | Step 2 |
| — | [도구 사양](./03-1-annotation-tool-spec.md) | — | — |
| [Step 4](./04-zone-detection-poc.md) | Zone 침입 감지 PoC 스크립트 | 기존 모델 | Step 1, 2 |
| [Step 5](./05-event-level-evaluation.md) | Event-level 정량 평가 | 기존 모델 | Step 3, 4 |
| [Step 6](./06-go-no-go-decision.md) | Go/No-Go 판단 | - | Step 5 |

## 실행 순서

어노테이션 도구(Step 3)는 Zone 편집 모드와 어노테이션 모드로 나뉜다.
Zone 편집 모드만 먼저 완성하면 Step 4와 병렬 진행이 가능하다.

```
Phase A: 기반 작업 (모델 불필요)
──────────────────────────────────────────────────
Step 1 (단위 테스트)  ──────────────────┐
                                        │
Step 2 (설정 스키마 + 코드)  ───┐       │
                                │       │
Step 3a (도구: Zone 편집 모드)  ─┘       │
  │                                     │
  │  Zone 설정 YAML 생성 가능            │
  │                                     │
Phase B: PoC + GT (기존 모델 사용)       │
──────────────────────────────────────────────────
  │                                     │
  ├── Step 4 (PoC 스크립트) ◄───────────┘
  │     결과 영상 + 이벤트 로그
  │
  └── Step 3b (도구: 어노테이션 모드)
        GT JSON 생성

Phase C: 평가
──────────────────────────────────────────────────
Step 5 (정량 평가) ◄── Step 4 이벤트 로그 + Step 3b GT
  │
Step 6 (Go/No-Go)
```

### 왜 이 순서인가

1. **Step 1, 2, 3a는 병렬 가능** — 모델 불필요, 독립적
2. **Step 3a(Zone 편집)를 먼저** — zone 설정 파일이 있어야 Step 4 PoC를 돌릴 수 있다
3. **Step 4와 Step 3b는 병렬 가능** — PoC 스크립트 개발과 GT 어노테이션 작업은 독립적
4. **Step 3b(어노테이션)는 Step 4 이후에 해도 된다** — PoC 결과 영상을 참고하면서 GT를 만들면 더 효율적 (단, 편향 주의)
5. **Step 5는 Step 3b + Step 4 모두 완료 후** — 시스템 이벤트 로그와 GT 모두 필요

### 도구 구현 순서 (Step 3 상세)

어노테이션 도구 자체의 구현도 단계를 나눈다:

```
Step 3a: Zone 편집 모드 (먼저)
─────────────────────────────
  3a-1. FastAPI 기본 셋업 (영상 파일 서빙, zone CRUD API)
  3a-2. React 프로젝트 초기화 (Vite + TypeScript)
  3a-3. VideoPlayer 컴포넌트 (HTML5 <video>, 재생/탐색)
  3a-4. ZoneEditor 컴포넌트 (Fabric.js polygon 그리기/편집)
  3a-5. ZonePanel 컴포넌트 (zone 목록, 추가/삭제)
  3a-6. 저장/불러오기 연동 (API ↔ YAML)
  → 산출물: zone 설정 YAML 생성 가능

Step 3b: 어노테이션 모드 (나중)
─────────────────────────────
  3b-1. 모드 전환 UI
  3b-2. EventTimeline 컴포넌트 (침입 시작/끝 마킹, 이벤트 목록)
  3b-3. 타임라인 시각화 (슬라이더 위 이벤트 구간 표시)
  3b-4. GT JSON 저장/불러오기
  → 산출물: GT JSON 생성 가능
```

## 기술 스택

| 레이어 | 선택 | 이유 |
|--------|------|------|
| Backend | FastAPI | 프로젝트 기존 계획 일치, Phase 5 대시보드 확장 |
| Frontend | React (Vite + TypeScript) | 컴포넌트 기반 확장, 대시보드 재사용 |
| Canvas | Fabric.js | polygon 편집 내장 지원 |
| 영상 재생 | HTML5 `<video>` | 브라우저 네이티브 |

상세 아키텍처와 디렉토리 구조는 [03-1-annotation-tool-spec.md](./03-1-annotation-tool-spec.md) 참조.

## 데이터 경로

모든 데이터는 기존 `DATA_ROOT` 패턴을 따른다:

```
DATA_ROOT (/home/neo/share/watch-tower_data/)
├── samples/          (기존) 샘플 영상
├── models/           (기존) 모델 가중치
├── outputs/          (기존) 추론 결과
├── experiments/      (기존) 실험 리포트
├── configs/zones/    zone 설정 YAML
└── zone_gt/          GT JSON
```
