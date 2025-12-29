"""
Acceptance Test AT-01: Successful image classification


select a valid PNG/JPG image from their computer
submits the form on the prediction page (/prediction).

"""

from io import BytesIO

import numpy as np
from PIL import Image


def test_acceptance_valid_image_prediction(client, monkeypatch):
    """AT-01 implementation: valid image goes through full prediction flow."""

    # Arrange: mock the TensorFlow model so the test is fast and deterministic
    class MockModel:
        def predict(self, x):
            # Make sure preprocessing produced a single image batch
            assert x.shape[0] == 1
            # Return a fixed probability vector (top-1 is index 2, for example)
            return np.array([[0.0, 0.0, 1.0] + [0.0] * 7])

    import model as model_module
    monkeypatch.setattr(model_module, "model", MockModel())

    # Create a simple in-memory image (no dependency on test image files)
    img = Image.new("RGB", (224, 224), color=(128, 128, 128))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Act: submit the form to /prediction with a valid file
    response = client.post(
        "/prediction",
        data={"file": (buffer, "test.png")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    # Assert: full acceptance criteria
    assert response.status_code == 200
    assert "text/html" in response.headers.get("Content-Type", "")

    body = response.data.lower()
    # page should show some kind of prediction/result text
    assert b"prediction" in body or b"result" in body
    # should NOT show typical error messages
    assert b"no file" not in body
    assert b"invalid file" not in body
    assert b"file is required" not in body
