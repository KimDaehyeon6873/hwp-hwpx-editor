"""Document 클래스 Fast Mode 테스트"""

import pytest
from pathlib import Path

from hwp_hwpx_editor import Document, DocumentType
from hwp_hwpx_parser import NoteData, ExtractResult, MemoData


TESTS_DATA_DIR = Path(__file__).parent / "data"


class TestDocumentFastMode:
    """Document 클래스 fast_mode 테스트"""

    @pytest.fixture
    def hwp5_notes_file(self):
        return TESTS_DATA_DIR / "sample_notes.hwp"

    @pytest.fixture
    def hwpx_notes_file(self):
        return TESTS_DATA_DIR / "sample_notes.hwpx"

    @pytest.fixture
    def basic_hwp_file(self):
        return TESTS_DATA_DIR / "각주미주.hwp"

    def test_fast_mode_hwp5_text_extraction(self, basic_hwp_file):
        if not basic_hwp_file.exists():
            pytest.skip("Test file not available")

        doc = Document(str(basic_hwp_file), fast_mode=True)
        text = doc.extract_text_fast()

        assert isinstance(text, str)
        assert len(text) > 0

    @pytest.mark.skipif(
        not (TESTS_DATA_DIR / "sample_notes.hwp").exists(),
        reason="Sample file not available",
    )
    def test_extract_text_with_notes_fast_hwp5(self, hwp5_notes_file):
        doc = Document(str(hwp5_notes_file), fast_mode=True)
        result = doc.extract_text_with_notes_fast()

        assert isinstance(result, ExtractResult)
        assert len(result.text) > 0
        assert len(result.footnotes) == 2
        assert len(result.endnotes) == 3
        assert len(result.hyperlinks) == 2

    @pytest.mark.skipif(
        not (TESTS_DATA_DIR / "sample_notes.hwpx").exists(),
        reason="Sample file not available",
    )
    def test_extract_text_with_notes_fast_hwpx(self, hwpx_notes_file):
        doc = Document(str(hwpx_notes_file), fast_mode=True)
        result = doc.extract_text_with_notes_fast()

        assert isinstance(result, ExtractResult)
        assert len(result.text) > 0
        assert len(result.footnotes) == 2
        assert len(result.endnotes) == 3
        assert len(result.hyperlinks) == 2

    @pytest.mark.skipif(
        not (TESTS_DATA_DIR / "sample_notes.hwp").exists(),
        reason="Sample file not available",
    )
    def test_get_footnotes_fast(self, hwp5_notes_file):
        doc = Document(str(hwp5_notes_file), fast_mode=True)
        footnotes = doc.get_footnotes_fast()

        assert len(footnotes) == 2
        assert all(isinstance(fn, NoteData) for fn in footnotes)
        assert all(fn.note_type == "footnote" for fn in footnotes)

    @pytest.mark.skipif(
        not (TESTS_DATA_DIR / "sample_notes.hwp").exists(),
        reason="Sample file not available",
    )
    def test_get_endnotes_fast(self, hwp5_notes_file):
        doc = Document(str(hwp5_notes_file), fast_mode=True)
        endnotes = doc.get_endnotes_fast()

        assert len(endnotes) == 3
        assert all(isinstance(en, NoteData) for en in endnotes)
        assert all(en.note_type == "endnote" for en in endnotes)

    @pytest.mark.skipif(
        not (TESTS_DATA_DIR / "sample_notes.hwp").exists(),
        reason="Sample file not available",
    )
    def test_get_hyperlinks_fast(self, hwp5_notes_file):
        doc = Document(str(hwp5_notes_file), fast_mode=True)
        hyperlinks = doc.get_hyperlinks_fast()

        assert len(hyperlinks) == 2
        assert all(isinstance(hl, tuple) for hl in hyperlinks)
        assert all(len(hl) == 2 for hl in hyperlinks)


class TestDocumentFastModeAutoDetect:
    """Document fast_mode 파일 타입 자동 감지 테스트"""

    def test_auto_detect_hwp(self):
        hwp_file = TESTS_DATA_DIR / "각주미주.hwp"
        if not hwp_file.exists():
            pytest.skip("Test file not available")

        doc = Document(str(hwp_file), fast_mode=True)
        assert doc.document_type == DocumentType.HWP

    @pytest.mark.skipif(
        not (TESTS_DATA_DIR / "sample_notes.hwpx").exists(),
        reason="Sample file not available",
    )
    def test_auto_detect_hwpx(self):
        hwpx_file = TESTS_DATA_DIR / "sample_notes.hwpx"
        doc = Document(str(hwpx_file), fast_mode=True)
        assert doc.document_type == DocumentType.HWPX


class TestDocumentFastModeEdgeCases:
    """Document fast_mode 엣지 케이스 테스트"""

    def test_blank_hwp_no_notes(self):
        blank_file = TESTS_DATA_DIR / "blank.hwp"
        if not blank_file.exists():
            pytest.skip("Test file not available")

        doc = Document(str(blank_file), fast_mode=True)
        result = doc.extract_text_with_notes_fast()

        assert result.footnotes == []
        assert result.endnotes == []
        assert result.hyperlinks == []

    def test_file_not_found_raises_on_extract(self):
        doc = Document("/nonexistent/path/file.hwp", fast_mode=True)
        with pytest.raises(FileNotFoundError):
            doc.extract_text_fast()

    def test_invalid_extension_raises(self):
        with pytest.raises(ValueError):
            Document("/some/path/file.txt", fast_mode=True)


class TestDocumentFastModeMemos:
    @pytest.fixture
    def sample_hwpx_file(self):
        return TESTS_DATA_DIR / "sample_notes.hwpx"

    @pytest.fixture
    def sample_hwp_file(self):
        return TESTS_DATA_DIR / "각주미주.hwp"

    @pytest.mark.skipif(
        not (TESTS_DATA_DIR / "sample_notes.hwpx").exists(),
        reason="Sample HWPX file not available",
    )
    def test_get_memos_fast_hwpx(self, sample_hwpx_file):
        doc = Document(str(sample_hwpx_file), fast_mode=True)
        memos = doc.get_memos_fast()

        assert isinstance(memos, list)

    def test_get_memos_fast_hwp(self):
        hwp_file = TESTS_DATA_DIR / "각주미주.hwp"
        if not hwp_file.exists():
            pytest.skip("Test file not available")

        doc = Document(str(hwp_file), fast_mode=True)
        memos = doc.get_memos_fast()

        assert isinstance(memos, list)
