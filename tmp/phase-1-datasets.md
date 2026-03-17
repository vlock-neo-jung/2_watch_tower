# Watch Tower - 1차 데이터셋 확보 계획

## 1. 핵심 결론

- 건설 특화 공개 비디오 데이터셋은 부족하다
- 1차는 `건설 특화 이미지셋 + 공개 CCTV 비디오 벤치마크` 조합으로 진행한다
- 1차 핵심 확보 대상은 `PPE`, `사람 검출`, `추적/인원수/침입 검증용` 데이터셋이다

## 2. 바로 확보 추천 데이터셋

### 2.1 PPE

#### 1) Ultralytics Construction-PPE
- 링크: <https://docs.ultralytics.com/datasets/detect/construction-ppe/>
- 용도: `PPE 감지`
- 상태: 바로 사용 가능
- 특징:
  - train / val / test 분리
  - 11개 클래스
  - 건설 현장 PPE 검증에 직접 사용 가능
- 비고:
  - 라이선스: AGPL-3.0

#### 2) Mendeley PPE Detection Dataset (5-Class)
- 링크: <https://data.mendeley.com/datasets/8vf7z6v5sb>
- 용도: `PPE 감지`
- 상태: 바로 사용 가능
- 특징:
  - 다양한 시점
  - 가림, 그림자, 먼지 등 현장 조건 반영
- 비고:
  - 라이선스: CC BY 4.0

### 2.2 사람 검출

#### 3) SODA
- 링크: <https://linjiarui.net/en/portfolio/2022-02-22-SODA-site-object-detection-dataset-for-deep-learning-in-construction>
- 용도: `사람 검출`
- 상태: 다운로드 링크 확인됨
- 특징:
  - 건설 특화 대규모 이미지셋
  - worker 포함 15개 클래스
  - 다양한 각도, 조명, 날씨 조건 포함

### 2.3 추적 / 인원수 / 침입 검증

#### 4) MOT20
- 링크: <https://motchallenge.net/data/MOT20Det/>
- 용도:
  - `Tracking`
  - `구역 내 인원 탐지`
  - `위험구역 침입 로직`
- 상태: 바로 다운로드 가능
- 특징:
  - 공개 benchmark
  - crowded surveillance 환경
  - tracking 및 counting 검증에 적합
- 비고:
  - 건설 현장은 아니지만 1차 tracking 검증용으로 실용적

#### 5) SOMPT22
- 링크: <https://sompt22.github.io/>
- 용도:
  - `Tracking`
  - `구역 내 인원 탐지`
- 상태: 공개 다운로드 가능
- 특징:
  - 고정형 CCTV 기반
  - outdoor surveillance 관점
- 비고:
  - 비상업 연구용 제한

## 3. 2차 후보 데이터셋

### 3.1 쓰러짐

#### 6) OmniFall
- 링크: <https://huggingface.co/datasets/simplexsigil2/omnifall>
- 용도: `쓰러짐 감지`
- 상태: 공개 접근 가능
- 특징:
  - 다양한 공개 fall dataset 통합 benchmark
  - staged / in-the-wild / synthetic 구성
- 비고:
  - 건설 현장 특화는 아님

### 3.2 화재 / 연기

#### 7) ONFIRE 2025
- 링크: <https://mivia.unisa.it/onfire2025/>
- 용도: `화재 / 연기 감지`
- 상태: 공개 정보 확인, 데이터 접근은 별도 요청 가능성 있음
- 특징:
  - 고정 CCTV 기반 fire / smoke 비디오 benchmark
  - scenario 기반 평가 체계
- 비고:
  - 1차 핵심 범위는 아님

## 4. 보류 후보

### CSOD-24
- 검색 결과상 건설 비디오 데이터셋 후보
- worker with helmet / without helmet 포함
- 공개 접근성 재확인 필요

### CMOT
- 건설 multi-object tracking 데이터셋 후보
- GitHub 저장소 확인
- 실제 데이터 접근성과 활용성 추가 확인 필요

## 5. 1차 추천 조합

- `PPE`: `Construction-PPE` + `Mendeley PPE`
- `사람 검출`: `SODA`
- `추적 / 인원수 / 침입`: `MOT20` 또는 `SOMPT22`
- `쓰러짐`: `OmniFall`
- `화재`: 일단 보류, 필요 시 `ONFIRE`

## 6. 1차 핵심 확보 대상

1. `Construction-PPE`
2. `Mendeley PPE`
3. `SODA`
4. `MOT20` 또는 `SOMPT22`

## 7. 실제 다운로드 URL 및 명령어

### 7.1 바로 다운로드 가능한 데이터셋

#### Construction-PPE
- 직접 URL: <https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip>

```bash
mkdir -p datasets/raw
wget -O "datasets/raw/construction-ppe.zip" "https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip"
unzip "datasets/raw/construction-ppe.zip" -d "datasets/raw/construction-ppe"
```

#### MOT20
- 직접 URL: <https://motchallenge.net/data/MOT20Det.zip>

```bash
mkdir -p datasets/raw
wget -O "datasets/raw/MOT20Det.zip" "https://motchallenge.net/data/MOT20Det.zip"
unzip "datasets/raw/MOT20Det.zip" -d "datasets/raw/MOT20Det"
```

#### SOMPT22
- 다운로드 페이지: <https://sompt22.github.io/>
- Google Drive 폴더: <https://drive.google.com/drive/folders/1Z_gnFmX-EKUe4yLBQPa2pxXkyqYbxkhX?usp=sharing>

```bash
pip install gdown
gdown --folder "https://drive.google.com/drive/folders/1Z_gnFmX-EKUe4yLBQPa2pxXkyqYbxkhX?usp=sharing" -O "datasets/raw/SOMPT22"
```

### 7.2 브라우저 다운로드 권장 데이터셋

#### SODA
- 다운로드 페이지: <https://linjiarui.net/en/portfolio/2022-02-22-SODA-site-object-detection-dataset-for-deep-learning-in-construction>
- SharePoint 링크: <https://hkustconnect-my.sharepoint.com/:f:/g/personal/ycdeng_connect_ust_hk/EiQLht3OhstGnKXrjFXyRZYBIXFjUC43jUUNVBXfM_kkKg?e=jJ2Nhv>
- 백업 링크: <https://pan.baidu.com/s/1vuWIOdBnb-U5F_JOxcZoBw?pwd=9cnh>
- 비고:
  - SharePoint 폴더형 링크이므로 브라우저 다운로드 권장

#### Mendeley PPE Detection Dataset (5-Class)
- 페이지: <https://data.mendeley.com/datasets/8vf7z6v5sb>
- 비고:
  - direct file URL이 고정적이지 않을 수 있으므로 브라우저 다운로드 권장

## 8. 핵심 결론

- 1차는 `PPE`, `사람 검출`, `추적/침입/인원수` 검증용 데이터 확보가 우선이다
- 건설 특화 비디오가 부족하므로 공개 CCTV benchmark를 함께 사용한다
- 1차에서는 `Construction-PPE`, `Mendeley PPE`, `SODA`, `MOT20 또는 SOMPT22`를 먼저 확보한다
