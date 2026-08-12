"""
Unit tests for chains/notice_extraction.py
"""
import pytest
from datetime import date

from chains.notice_extraction import (
    NoticeEmailExtract,
    info_parse_prompt,
    NOTICE_PARSER_CHAIN,
)


class TestNoticeEmailExtract:
    """Tests for NoticeEmailExtract model"""

    def test_create_empty_notice(self):
        """Checking if NoticeEmailExtract is empty"""
        notice = NoticeEmailExtract()
        assert notice.entity_name is None
        assert notice.project_id is None
        assert notice.max_potential_fine is None

    def test_create_full_notice(self):
        """Checking if NoticeEmailExtract is full"""
        notice = NoticeEmailExtract(
            date_of_notice_str="2024-06-15",
            entity_name="OSHA",
            entity_phone="(555) 123-4567",
            entity_email="compliance@osha.gov",
            project_id=111232345,
            site_location="123 Main Street, Dallas, TX",
            violation_type="Safety violations",
            required_changes="Install guardrails",
            compliance_deadline_str="2024-07-10",
            max_potential_fine=25000.0,
        )
        assert notice.entity_name == "OSHA"
        assert notice.project_id == 111232345
        assert notice.max_potential_fine == 25000.0

    def test_date_conversion_valid(self):
        """Checking the conversion of a valid date"""
        notice = NoticeEmailExtract(date_of_notice_str="2024-06-15")
        assert notice.date_of_notice == date(2024, 6, 15)

    def test_date_conversion_invalid(self):
        """Checking for invalid date conversion"""
        notice = NoticeEmailExtract(date_of_notice_str="invalid-date")
        assert notice.date_of_notice is None

    def test_date_conversion_none(self):
        """Checking the conversion of None dates"""
        notice = NoticeEmailExtract(date_of_notice_str=None)
        assert notice.date_of_notice is None

    def test_compliance_deadline_conversion(self):
        """Checking the deadline date conversion"""
        notice = NoticeEmailExtract(compliance_deadline_str="2024-07-10")
        assert notice.compliance_deadline == date(2024, 7, 10)

    def test_project_id_integer(self):
        """Checking that project_id is an integer"""
        notice = NoticeEmailExtract(project_id=12345)
        assert isinstance(notice.project_id, int)

    def test_max_potential_fine_float(self):
        """Checking that max_potential_fine is a float"""
        notice = NoticeEmailExtract(max_potential_fine=10000.50)
        assert isinstance(notice.max_potential_fine, float)

    def test_entity_email_validation(self):
        """Checking the email field entity_email"""
        notice = NoticeEmailExtract(entity_email="test@example.com")
        assert notice.entity_email == "test@example.com"


class TestInfoParsePrompt:
    """Tests for info_parse_prompt"""

    def test_prompt_has_messages(self):
        """Checking that the prompt contains messages"""
        assert hasattr(info_parse_prompt, 'messages')
        assert len(info_parse_prompt.messages) > 0

    def test_prompt_template_content(self):
        """Checking the contents of a prompt template"""
        prompt_str = str(info_parse_prompt)
        assert "message" in prompt_str.lower()
        assert "parse" in prompt_str.lower() or "extract" in prompt_str.lower()


class TestNoticeParserChain:
    """Tests for NOTICE_PARSER_CHAIN"""

    def test_chain_structure(self):
        """Checking the chain structure"""
        assert NOTICE_PARSER_CHAIN is not None
        assert hasattr(NOTICE_PARSER_CHAIN, 'invoke')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
