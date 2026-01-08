"""
HWPX 표 및 텍스트 교체 기능 테스트
"""

import pytest
from pathlib import Path


class TestHWPXTableManager:
    """HWPXTableManager 테스트"""

    @pytest.fixture
    def sample_hwpx_path(self):
        return Path("tests/data/Table.hwpx")

    def test_get_all_tables(self, sample_hwpx_path):
        from hwp_hwpx_editor import HWPEditor, HWPXTableManager

        if not sample_hwpx_path.exists():
            pytest.skip("Test file not found")

        editor = HWPEditor()
        doc = editor(str(sample_hwpx_path))

        manager = HWPXTableManager(doc._java_object)
        tables = manager.get_all_tables()

        assert len(tables) > 0
        doc.close()

    def test_extract_table_text(self, sample_hwpx_path):
        from hwp_hwpx_editor import HWPEditor, HWPXTableManager

        if not sample_hwpx_path.exists():
            pytest.skip("Test file not found")

        editor = HWPEditor()
        doc = editor(str(sample_hwpx_path))

        manager = HWPXTableManager(doc._java_object)
        tables = manager.get_all_tables(include_nested=False)

        if tables:
            text = manager.extract_table_text(tables[0])
            assert isinstance(text, list)
            assert len(text) > 0
            assert isinstance(text[0], list)

        doc.close()

    def test_get_table_size(self, sample_hwpx_path):
        from hwp_hwpx_editor import HWPEditor, HWPXTableManager

        if not sample_hwpx_path.exists():
            pytest.skip("Test file not found")

        editor = HWPEditor()
        doc = editor(str(sample_hwpx_path))

        manager = HWPXTableManager(doc._java_object)
        tables = manager.get_all_tables(include_nested=False)

        if tables:
            rows, cols = manager.get_table_size(tables[0])
            assert rows > 0
            assert cols > 0

        doc.close()


class TestHWPXTextReplacer:
    """HWPXTextReplacer 테스트"""

    @pytest.fixture
    def sample_hwpx_path(self):
        return Path("tests/data/sample1.hwpx")

    def test_replace_all(self, sample_hwpx_path):
        from hwp_hwpx_editor import HWPEditor, HWPXTextReplacer

        if not sample_hwpx_path.exists():
            pytest.skip("Test file not found")

        editor = HWPEditor()
        doc = editor(str(sample_hwpx_path))

        replacer = HWPXTextReplacer(doc._java_object)
        count = replacer.replace_all(str.upper)

        assert count >= 0
        doc.close()


class TestDocumentTextReplacement:
    """Document 텍스트 교체 메서드 테스트"""

    @pytest.fixture
    def sample_hwpx_path(self):
        return Path("tests/data/sample1.hwpx")

    def test_replace_all_texts(self, sample_hwpx_path):
        from hwp_hwpx_editor import HWPEditor

        if not sample_hwpx_path.exists():
            pytest.skip("Test file not found")

        editor = HWPEditor()
        doc = editor(str(sample_hwpx_path))

        count = doc.replace_all_texts(lambda t: t.upper())

        assert count >= 0
        doc.close()

    def test_replace_table_texts(self, sample_hwpx_path):
        from hwp_hwpx_editor import HWPEditor

        if not sample_hwpx_path.exists():
            pytest.skip("Test file not found")

        editor = HWPEditor()
        doc = editor(str(sample_hwpx_path))

        count = doc.replace_table_texts(lambda t: f"[TABLE]{t}")

        assert count >= 0
        doc.close()

    def test_get_hwpx_table_manager(self, sample_hwpx_path):
        from hwp_hwpx_editor import HWPEditor, HWPXTableManager

        if not sample_hwpx_path.exists():
            pytest.skip("Test file not found")

        editor = HWPEditor()
        doc = editor(str(sample_hwpx_path))

        manager = doc.get_hwpx_table_manager()

        assert isinstance(manager, HWPXTableManager)
        doc.close()

    def test_replace_by_location(self, sample_hwpx_path):
        from hwp_hwpx_editor import HWPEditor

        if not sample_hwpx_path.exists():
            pytest.skip("Test file not found")

        editor = HWPEditor()
        doc = editor(str(sample_hwpx_path))

        count = doc.replace_all_texts(lambda t: t.lower(), locations=["body", "table"])

        assert count >= 0
        doc.close()
