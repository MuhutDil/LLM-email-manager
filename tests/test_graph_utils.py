"""
Unit tests for utils/graph_utils.py
"""
import pytest
from unittest.mock import patch

from chains.notice_extraction import NoticeEmailExtract
from utils.graph_utils import send_escalation_email, create_legal_ticket


class TestSendEscalationEmail:
    """Tests for the function send_escalation_email"""

    @patch('utils.graph_utils.LOGGER')
    @patch('utils.graph_utils.time.sleep', return_value=None)
    def test_send_escalation_email_single(self, mock_sleep, mock_logger):
        """Testing the sending escalation email"""
        notice = NoticeEmailExtract(entity_name="Test Entity")
        emails = ["test@example.com"]
        
        send_escalation_email(notice, emails)
        
        mock_logger.info.assert_any_call("Sending escalation emails...")
        mock_logger.info.assert_any_call(f"Escalation email sent to test@example.com")
        assert mock_sleep.call_count == 1

    @patch('utils.graph_utils.LOGGER')
    @patch('utils.graph_utils.time.sleep', return_value=None)
    def test_send_escalation_email_multiple(self, mock_sleep, mock_logger):
        """Testing sending multiple escalation emails"""
        notice = NoticeEmailExtract(entity_name="Test Entity")
        emails = ["test1@example.com", "test2@example.com", "test3@example.com"]
        
        send_escalation_email(notice, emails)
        
        assert mock_sleep.call_count == 3
        assert mock_logger.info.call_count == 4  # 1 initial + 3 per email

    @patch('utils.graph_utils.LOGGER')
    @patch('utils.graph_utils.time.sleep', return_value=None)
    def test_send_escalation_email_empty_list(self, mock_sleep, mock_logger):
        """Testing sending with an empty email list"""
        notice = NoticeEmailExtract(entity_name="Test Entity")
        emails = []
        
        send_escalation_email(notice, emails)
        
        mock_logger.info.assert_called_with("Sending escalation emails...")
        mock_sleep.assert_not_called()


class TestCreateLegalTicket:
    """Tests for the function create_legal_ticket"""

    @patch('utils.graph_utils.LOGGER')
    @patch('utils.graph_utils.time.sleep', return_value=None)
    @patch('utils.graph_utils.random.choice', return_value=None)
    def test_create_legal_ticket_no_followup(self, mock_choice, mock_sleep, mock_logger):
        """Checking ticket creation without follow-up"""
        notice = NoticeEmailExtract(
            entity_name="Test Entity",
            project_id=12345,
        )
        
        result = create_legal_ticket(None, notice)
        
        assert result is None
        mock_logger.info.assert_any_call("Creating legal ticket for notice...")
        mock_logger.info.assert_any_call("Legal ticket created!")
        mock_sleep.assert_called_once()

    @patch('utils.graph_utils.LOGGER')
    @patch('utils.graph_utils.time.sleep', return_value=None)
    @patch('utils.graph_utils.random.choice')
    def test_create_legal_ticket_with_followup(self, mock_choice, mock_sleep, mock_logger):
        """Checking the creation of a ticket with a follow-up question"""
        follow_up_question = "Does this message mention Texas?"
        mock_choice.return_value = follow_up_question
        
        notice = NoticeEmailExtract(
            entity_name="Test Entity",
            project_id=12345,
        )
        
        result = create_legal_ticket(None, notice)
        
        assert result == follow_up_question
        mock_logger.info.assert_any_call("Follow-up is required before creating this ticket")

    @patch('utils.graph_utils.LOGGER')
    @patch('utils.graph_utils.time.sleep', return_value=None)
    @patch('utils.graph_utils.random.choice', return_value=None)
    def test_create_legal_ticket_with_existing_followups(self, mock_choice, mock_sleep, mock_logger):
        """Checking ticket creation with existing follow-up"""
        existing_follow_ups = {
            "Does this message mention the states of Texas, Georgia, or New Jersey?": True
        }
        
        notice = NoticeEmailExtract(
            entity_name="Test Entity",
            project_id=12345,
        )
        
        result = create_legal_ticket(existing_follow_ups, notice)
        
        # The result must be None or a string (another follow-up question)
        assert result is None or isinstance(result, str)

    @patch('utils.graph_utils.LOGGER')
    @patch('utils.graph_utils.time.sleep', return_value=None)
    def test_create_legal_ticket_logs_info(self, mock_sleep, mock_logger):
        """Checking logging function create_legal_ticket"""
        notice = NoticeEmailExtract(entity_name="Test Entity")
        
        with patch('utils.graph_utils.random.choice', return_value=None):
            create_legal_ticket(None, notice)
        
        mock_logger.info.assert_any_call("Creating legal ticket for notice...")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
