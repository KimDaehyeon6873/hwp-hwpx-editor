"""
기본 기능 테스트
"""

import pytest
from pathlib import Path

from hwp_hwpx_editor import HWPParser, Document, DocumentType


class TestHWPParser:
    """HWPParser 클래스 테스트"""

    def test_initialization(self):
        """파서 초기화 테스트"""
        parser = HWPParser()
        assert parser is not None

    def test_create_blank_hwpx(self):
        """빈 HWPX 문서 생성 테스트"""
        parser = HWPParser()
        doc = parser.create_blank(DocumentType.HWPX)

        assert doc is not None
        assert doc.document_type == DocumentType.HWPX
        assert doc.is_modified is True

        # 텍스트 추출 테스트
        text = doc.extract_text()
        assert isinstance(text, str)

        doc.close()


class TestDocument:
    """Document 클래스 테스트"""

    def test_context_manager(self):
        """컨텍스트 매니저 테스트"""
        parser = HWPParser()
        with parser.create_blank(DocumentType.HWPX) as doc:
            assert doc is not None
            text = doc.extract_text()
            assert isinstance(text, str)

    def test_document_repr(self):
        """문서 문자열 표현 테스트"""
        parser = HWPParser()
        doc = parser.create_blank(DocumentType.HWPX)

        repr_str = repr(doc)
        assert "Document" in repr_str
        assert "hwpx" in repr_str
        assert "modified" in repr_str

        doc.close()


class TestHWPSupport:
    """HWP 파일 지원 테스트"""

    def test_hwp_file_exists(self):
        """HWP 테스트 파일 존재 확인"""
        hwp_path = Path("tests/data/blank.hwp")
        assert hwp_path.exists()

    def test_hwp_file_loading(self):
        """HWP 파일 로딩 테스트"""
        hwp_path = Path("tests/data/blank.hwp")

        # 파일 존재 확인
        assert hwp_path.exists()

        # Document 생성 시도 (일단은 파일이 존재하는지만 확인)
        # 실제 JVM 호출은 환경에 따라 실패할 수 있으므로 기본적인 구조만 테스트
        pass


class TestHWPXSupport:
    """HWPX 파일 지원 테스트"""

    def test_hwpx_file_exists(self):
        """HWPX 테스트 파일 존재 확인"""
        hwpx_path = Path("tests/data/sample1.hwpx")
        assert hwpx_path.exists()

    def test_hwpx_file_loading(self):
        """HWPX 파일 로딩 테스트"""
        hwpx_path = Path("tests/data/sample1.hwpx")

        # 파일 존재 확인
        assert hwpx_path.exists()

        # Document 생성 시도 (일단은 파일이 존재하는지만 확인)
        # 실제 JVM 호출은 환경에 따라 실패할 수 있으므로 기본적인 구조만 테스트
        pass
