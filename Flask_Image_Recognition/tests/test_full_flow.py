# test_full_flow.py
"""
Assignment 3 -  Tests with Test Doubles
Covers one happy path and one sad path
"""
from io import BytesIO

def test_prediction_happy_path_with_stubs(client, monkeypatch):
    """
    Happy Path:
    - Stub out heavy model functions via the app namespace
    - Simulate a valid image upload and verify end-to-end behavior
    """
    # Define stubs
    def fake_preprocess_img(stream):
        return "FAKE_TENSOR"

    def fake_predict_result(data):
        assert data == "FAKE_TENSOR"
        return 7  # deterministic class

    # Patch the names used by app.py (since it imported them directly)
    import app
    monkeypatch.setattr(app, "preprocess_img", fake_preprocess_img)
    monkeypatch.setattr(app, "predict_result", fake_predict_result)

    # Simulate uploading an image
    fake_image = BytesIO(b"pretend_this_is_image_bytes")
    fake_image.name = "sample.jpg"

    resp = client.post(
        "/prediction",
        data={"file": (fake_image, fake_image.name)},
        content_type="multipart/form-data",
    )

    assert resp.status_code == 200
    assert b"Prediction" in resp.data or b"7" in resp.data


def test_prediction_sad_path_exception_from_preprocess(client, monkeypatch):
    """
    Sad Path:
    - Force preprocess_img to raise an exception
    - Verify graceful error handling
    """
    def broken_preprocess(_stream):
        raise ValueError("Simulated preprocessing failure")

    import app
    monkeypatch.setattr(app, "preprocess_img", broken_preprocess)

    fake_image = BytesIO(b"fake_bytes")
    fake_image.name = "broken.jpg"

    resp = client.post(
        "/prediction",
        data={"file": (fake_image, fake_image.name)},
        content_type="multipart/form-data",
    )

    assert resp.status_code == 200
    assert b"File cannot be processed." in resp.data
