## ADDED Requirements

### Requirement: PyTorch CUDA 동작
PyTorch가 CUDA GPU를 인식하고 사용할 수 있어야 한다 (SHALL).

#### Scenario: CUDA 사용 가능 확인
- **WHEN** `python -c "import torch; print(torch.cuda.is_available())"`을 실행하면
- **THEN** True가 출력되어야 한다

#### Scenario: GPU 디바이스 확인
- **WHEN** `python -c "import torch; print(torch.cuda.get_device_name(0))"`을 실행하면
- **THEN** "NVIDIA GeForce RTX 3080 Ti"가 출력되어야 한다

### Requirement: ultralytics GPU 추론
ultralytics YOLO 모델이 GPU에서 추론을 실행할 수 있어야 한다 (SHALL).

#### Scenario: YOLO GPU 추론 실행
- **WHEN** ultralytics YOLO 모델을 로드하고 device="cuda"로 추론을 실행하면
- **THEN** GPU에서 추론이 완료되고 결과가 반환되어야 한다

#### Scenario: CUDA 메모리 사용
- **WHEN** GPU 추론이 실행되는 동안
- **THEN** nvidia-smi에서 GPU 메모리 사용량이 증가해야 한다
