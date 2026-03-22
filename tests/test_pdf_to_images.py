from unittest.mock import patch, MagicMock
from pdf_to_images import download_doc, convert_pdf_to_images

def test_download_doc_pdf(tmp_path):
    """PDF URL이면 다운로드 후 경로를 반환."""
    url = "https://example.com/test.pdf"
    fake_content = b"%PDF-1.4 fake content"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = fake_content

    with patch("pdf_to_images.requests.get", return_value=mock_response):
        path = download_doc(url, str(tmp_path))
        assert path is not None
        assert path.endswith(".pdf")

def test_download_doc_empty_url(tmp_path):
    """빈 URL이면 None 반환."""
    path = download_doc("", str(tmp_path))
    assert path is None

def test_download_doc_hwp(tmp_path):
    """HWP URL이면 None 반환 (변환 불가)."""
    url = "https://example.com/test.hwp"
    path = download_doc(url, str(tmp_path))
    assert path is None

def test_convert_pdf_to_images():
    """pdf2image 호출을 mock하여 이미지 리스트 반환 확인."""
    fake_images = [MagicMock(), MagicMock()]
    for img in fake_images:
        img.save = MagicMock()

    with patch("pdf2image.convert_from_path", return_value=fake_images):
        result = convert_pdf_to_images("/fake/path.pdf", "/fake/output")
        assert len(result) == 2
