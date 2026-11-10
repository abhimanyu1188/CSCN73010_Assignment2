
# test_acceptance_happy.py
"""Acceptance tests for successful image uploads."""

from io import BytesIO

from PIL import Image


def create_test_image(width, height, color="white"):
    """Create a valid JPEG image in memory."""
    img_data = BytesIO()

    image = Image.new("RGB", (width, height), color=color)
    image.save(img_data, format="JPEG")

    img_data.seek(0)
    return img_data


def assert_successful_prediction(client, img_data, filename):
    """Upload an image and verify successful prediction."""
    response = client.post(
        "/prediction",
        data={"file": (img_data, filename)},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"File cannot be processed" not in response.data
    assert b"Prediction" in response.data


def test_acceptance_successful_upload(client):
    """Test successful upload of a valid JPEG image."""
    img_data = create_test_image(224, 224)

    assert_successful_prediction(
        client,
        img_data,
        "test_image.jpg"
    )


def test_acceptance_valid_large_image(client):
    """Test successful upload of a large valid JPEG image."""
    img_data = create_test_image(2000, 2000)

    assert_successful_prediction(
        client,
        img_data,
        "large_image.jpg"
    )


def test_acceptance_valid_image_size_upload(client):
    """Test successful upload of a high-resolution image."""
    img_data = create_test_image(1920, 1080, color="blue")

    assert_successful_prediction(
        client,
        img_data,
        "high_resolution_image.jpg"
    )
