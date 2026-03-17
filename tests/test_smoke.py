"""Smoke test: 핵심 패키지 임포트 확인."""


def test_import_watch_tower():
    import watch_tower

    assert watch_tower is not None


def test_import_ultralytics():
    from ultralytics import YOLO

    assert YOLO is not None


def test_import_supervision():
    import supervision

    assert supervision is not None


def test_import_huggingface_hub():
    from huggingface_hub import hf_hub_download

    assert hf_hub_download is not None
