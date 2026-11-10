
"""Integration test for successful image prediction."""

from io import BytesIO

from PIL import Image


def test_successful_prediction(client):
    """Verify that a valid image passes through the prediction pipeline."""
    img_data = BytesIO()

    image = Image.new("RGB", (224, 224), color="white")
    image.save(img_data, format="JPEG")
    img_data.seek(0)

    response = client.post(
        "/prediction",
        data={"file": (img_data, "test.jpg")},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"File cannot be processed" not in response.data
    assert b"Prediction" in response.data
