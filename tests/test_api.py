import os
import sys
import io
import pytest
from PIL import Image

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from fast_api.main import app
from fast_api.yolo_service import run_yolo_inference

client = TestClient(app)


def _generate_test_image_bytes(width: int = 300, height: int = 300) -> bytes:
    """Generate in-memory RGB JPEG image bytes for test fixtures."""
    img = Image.new("RGB", (width, height), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_root_endpoint():
    """Verify that root endpoint returns service metadata and routes catalog."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["version"] == "1.0.0"
    assert "endpoints" in data
    assert "live_inference" in data["endpoints"]


def test_health_endpoint():
    """Verify health endpoint responds with system status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "database" in data
    assert data["version"] == "1.0.0"


def test_yolo_service_inference_direct():
    """Test the standalone YOLO service inference execution."""
    image_bytes = _generate_test_image_bytes(400, 400)
    result = run_yolo_inference(image_bytes, confidence_threshold=0.20, render_annotation=True)

    assert "engine" in result
    assert result["image_width"] == 400
    assert result["image_height"] == 400
    assert result["inference_time_ms"] >= 0
    assert isinstance(result["detections"], list)
    assert result["annotated_image_base64"] is not None


def test_live_detect_endpoint():
    """Test the live POST /api/v1/detect file upload endpoint."""
    image_bytes = _generate_test_image_bytes(500, 500)
    files = {"file": ("test_sample.jpg", image_bytes, "image/jpeg")}

    response = client.post("/api/v1/detect?confidence=0.25&include_preview=true", files=files)
    assert response.status_code == 200

    data = response.json()
    assert "engine" in data
    assert data["image_width"] == 500
    assert data["image_height"] == 500
    assert "detected_count" in data
    assert "inference_time_ms" in data
    assert isinstance(data["detections"], list)
    assert data["annotated_image_base64"] is not None


def test_live_detect_invalid_file_type():
    """Verify non-image uploads are rejected with 400."""
    text_bytes = b"Hello, this is a plain text file."
    files = {"file": ("document.txt", text_bytes, "text/plain")}

    response = client.post("/api/v1/detect", files=files)
    assert response.status_code == 400
    assert "Uploaded file must be an image" in response.json()["detail"]


def test_warehouse_detections_endpoint():
    """Verify querying extracted warehouse detections."""
    response = client.get("/api/v1/detections")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
