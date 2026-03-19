## 1. 모듈 구조 생성

- [x] 1.1 `src/watch_tower/zone/` 디렉토리 및 `__init__.py` 생성
- [x] 1.2 pydantic v2 사용 가능 여부 확인 (ultralytics 경유 버전 체크)

## 2. Pydantic 데이터 모델 (zone/models.py)

- [x] 2.1 ZoneType enum 정의 (danger, warning, entry)
- [x] 2.2 GeoJSONPolygon 모델 정의 (type, coordinates + 좌표 범위/꼭짓점 수/closing point 검증)
- [x] 2.3 ZoneDefinition 모델 정의 (전체 필드 + zone_id 검증 + 기본값)
- [x] 2.4 ZoneConfig 모델 정의 (zones 리스트 + zone_id 중복 검증)
- [x] 2.5 ZoneDefinition.to_polygon_zone(w, h) 메서드 구현 (정규화→픽셀 변환 + PolygonZone 생성)

## 3. YAML 파일 I/O (zone/config.py)

- [x] 3.1 load_zone_config(path) 구현 (YAML 로드 → ZoneConfig 파싱)
- [x] 3.2 save_zone_config(config, path) 구현 (ZoneConfig → YAML 저장, 디렉토리 자동 생성)

## 4. 공개 API (__init__.py)

- [x] 4.1 zone 모듈 공개 API 정의 (ZoneDefinition, ZoneConfig, ZoneType, GeoJSONPolygon, load_zone_config, save_zone_config)

## 5. 샘플 데이터

- [x] 5.1 DATA_ROOT/configs/zones/sample.yaml 작성 (danger 1개 + warning 1개)

## 6. Zone 설정 모듈 테스트 (tests/test_zone_config.py)

- [x] 6.1 유효한 ZoneDefinition 생성 테스트
- [x] 6.2 zone_id 빈 문자열 거부 테스트
- [x] 6.3 ZoneType 유효/무효 값 테스트
- [x] 6.4 GeoJSON 좌표 범위 초과 거부 테스트
- [x] 6.5 GeoJSON 꼭짓점 부족 거부 테스트
- [x] 6.6 GeoJSON closing point 자동 추가 테스트
- [x] 6.7 ZoneConfig zone_id 중복 거부 테스트
- [x] 6.8 to_polygon_zone 좌표 변환 정확성 테스트
- [x] 6.9 YAML 로드/저장 왕복(round-trip) 테스트
- [x] 6.10 존재하지 않는 파일 로드 시 에러 테스트

## 7. Zone Logic 단위 테스트 (tests/test_zone_logic.py)

- [x] 7.1 zone 내부 중앙 bbox → True 테스트
- [x] 7.2 zone 완전 외부 bbox → False 테스트
- [x] 7.3 상반신 안/발 밖 → BOTTOM_CENTER False 테스트
- [x] 7.4 상반신 밖/발 안 → BOTTOM_CENTER True 테스트
- [x] 7.5 BOTTOM_CENTER vs CENTER anchor 판정 차이 테스트
- [x] 7.6 경계선 안쪽/바깥 판정 테스트
- [x] 7.7 여러 사람 중 일부만 zone 안 테스트
- [x] 7.8 빈 detections 테스트
- [x] 7.9 오목 polygon 테스트
- [x] 7.10 정규화→픽셀 좌표 변환 (1920x1080, 3840x2160) 테스트

## 8. 검증

- [x] 8.1 `uv run pytest tests/test_zone_config.py tests/test_zone_logic.py -v` 전체 통과 확인
