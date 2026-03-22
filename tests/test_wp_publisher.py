import json
from unittest.mock import patch, MagicMock
from wp_publisher import upload_image, create_post, load_published, save_published

def test_upload_image():
    """이미지 업로드 시 WP Media API 호출 확인."""
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"id": 42, "source_url": "https://wp.com/img.png"}
    mock_resp.raise_for_status = MagicMock()

    with patch("wp_publisher.requests.post", return_value=mock_resp):
        with patch("builtins.open", MagicMock()):
            result = upload_image("/fake/img.png")
            assert result["id"] == 42

def test_create_post():
    """포스트 생성 시 WP Posts API 호출 확인."""
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {
        "id": 100,
        "link": "https://wp.com/2026/03/20/test-post/",
    }
    mock_resp.raise_for_status = MagicMock()

    with patch("wp_publisher.requests.post", return_value=mock_resp):
        result = create_post("제목", "<p>본문</p>")
        assert result["id"] == 100
        assert "link" in result

def test_load_save_published(tmp_path):
    """발행 기록 로드/저장."""
    filepath = str(tmp_path / "wp_published.json")

    data = load_published(filepath)
    assert data == {}

    data["TEST001"] = "https://wp.com/post/1"
    save_published(data, filepath)

    reloaded = load_published(filepath)
    assert reloaded["TEST001"] == "https://wp.com/post/1"
