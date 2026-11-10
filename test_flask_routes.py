
"""Tests for Flask homepage and invalid image uploads."""

from io import BytesIO


def test_homepage(client):
    """Verify that the homepage loads successfully."""
    response = client.get("/")

    assert response.status_code == 200
    assert b"<html" in response.data.lower()


def test_invalid_image_upload(client):
    """Verify that a non-image file is rejected."""
    invalid_file = BytesIO(b"This is not a valid image.")

    response = client.post(
        "/prediction",
        data={"file": (invalid_file, "invalid.jpg")},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"File cannot be processed" in response.data
