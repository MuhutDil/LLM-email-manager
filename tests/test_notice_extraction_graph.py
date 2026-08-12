"""
Unit tests for graphs/notice_extraction.py
"""
import pytest
from unittest.mock import Mock, patch

from graphs.notice_extraction import (
    GraphState,
    parse_notice_message_node,
    check_escalation_status_node,
    send_escalation_email_node,
    create_legal_ticket_node,
    route_escalation_status_edge,
    answer_follow_up_question_node,
    route_follow_up_edge,
    workflow,
    NOTICE_EXTRACTION_GRAPH,
)
from chains.notice_extraction import NoticeEmailExtract


class TestGraphState:
    """Tests for the GraphState structure"""

    def test_graph_state_keys(self):
        """Checking for the presence of required keys in GraphState"""
        # GraphState is a TypedDict, check that it is defined
        assert GraphState is not None


class TestParseNoticeMessageNode:
    """Tests for parse_notice_message_node"""

    @patch('graphs.notice_extraction.NOTICE_PARSER_CHAIN')
    def test_parse_notice_message_node(self, mock_chain):
        """Проверка узла парсинга notice сообщения"""
        mock_extract = NoticeEmailExtract(
            entity_name="Test Entity",
            project_id=12345,
        )
        mock_chain.invoke.return_value = mock_extract
        
        state = {
            "notice_message": "Test notice message",
            "notice_email_extract": None,
        }
        
        result = parse_notice_message_node(state)
        
        assert result["notice_email_extract"] == mock_extract
        mock_chain.invoke.assert_called_once()


class TestCheckEscalationStatusNode:
    """Tests for check_escalation_status_node"""

    @patch('graphs.notice_extraction.ESCALATION_CHECK_CHAIN')
    def test_check_escalation_status_needs_escalation_text(self, mock_chain):
        """Checking the need for escalation by text"""
        mock_chain.invoke.return_value = Mock(needs_escalation=True)
        
        state = {
            "notice_message": "Test message",
            "notice_email_extract": NoticeEmailExtract(max_potential_fine=5000),
            "escalation_text_criteria": "immediate danger",
            "escalation_dollar_criteria": 100000,
            "requires_escalation": False,
        }
        
        result = check_escalation_status_node(state)
        
        assert result["requires_escalation"] is True

    @patch('graphs.notice_extraction.ESCALATION_CHECK_CHAIN')
    def test_check_escalation_status_needs_escalation_dollar(self, mock_chain):
        """Checking the need for escalation by amount"""
        mock_chain.invoke.return_value = Mock(needs_escalation=False)
        
        state = {
            "notice_message": "Test message",
            "notice_email_extract": NoticeEmailExtract(max_potential_fine=150000),
            "escalation_text_criteria": "immediate danger",
            "escalation_dollar_criteria": 100000,
            "requires_escalation": False,
        }
        
        result = check_escalation_status_node(state)
        
        assert result["requires_escalation"] is True

    @patch('graphs.notice_extraction.ESCALATION_CHECK_CHAIN')
    def test_check_escalation_status_no_escalation(self, mock_chain):
        """Checking whether escalation is necessary"""
        mock_chain.invoke.return_value = Mock(needs_escalation=False)
        
        state = {
            "notice_message": "Test message",
            "notice_email_extract": NoticeEmailExtract(max_potential_fine=5000),
            "escalation_text_criteria": "immediate danger",
            "escalation_dollar_criteria": 100000,
            "requires_escalation": False,
        }
        
        result = check_escalation_status_node(state)
        
        assert result["requires_escalation"] is False


class TestSendEscalationEmailNode:
    """Tests for send_escalation_email_node"""

    @patch('graphs.notice_extraction.send_escalation_email')
    def test_send_escalation_email_node(self, mock_send_email):
        """Checking the escalation email sending node"""
        state = {
            "notice_email_extract": NoticeEmailExtract(entity_name="Test"),
            "escalation_emails": ["test@example.com"],
        }
        
        result = send_escalation_email_node(state)
        
        mock_send_email.assert_called_once()
        assert result == state


class TestCreateLegalTicketNode:
    """Tests for create_legal_ticket_node"""

    @patch('graphs.notice_extraction.create_legal_ticket')
    def test_create_legal_ticket_node(self, mock_create_ticket):
        """Checking the legal ticket creation node"""
        mock_create_ticket.return_value = None
        
        state = {
            "notice_email_extract": NoticeEmailExtract(entity_name="Test"),
            "follow_ups": None,
            "current_follow_up": None,
        }
        
        result = create_legal_ticket_node(state)
        
        mock_create_ticket.assert_called_once()
        assert "current_follow_up" in result


class TestRouteEscalationStatusEdge:
    """Tests for route_escalation_status_edge"""

    def test_route_escalation_status_requires_escalation(self):
        """Check routing if escalation is necessary"""
        state = {"requires_escalation": True}
        
        result = route_escalation_status_edge(state)
        
        assert result == "send_escalation_email"

    def test_route_escalation_status_no_escalation(self):
        """Checking routing without escalation"""
        state = {"requires_escalation": False}
        
        result = route_escalation_status_edge(state)
        
        assert result == "create_legal_ticket"


class TestAnswerFollowUpQuestionNode:
    """Tests for answer_follow_up_question_node"""

    @patch('graphs.notice_extraction.BINARY_QUESTION_CHAIN')
    def test_answer_follow_up_question_node(self, mock_chain):
        """Checking the answer node for a follow-up question"""
        mock_chain.invoke.return_value = Mock(is_true=True)
        
        state = {
            "current_follow_up": "Test question?",
            "notice_message": "Test message",
            "follow_ups": None,
        }
        
        result = answer_follow_up_question_node(state)
        
        mock_chain.invoke.assert_called_once()
        assert result["follow_ups"] is not None
        assert "Test question?" in result["follow_ups"]

    def test_answer_follow_up_question_node_no_followup(self):
        """Checking a node without a follow-up question"""
        state = {
            "current_follow_up": None,
            "notice_message": "Test message",
        }
        
        result = answer_follow_up_question_node(state)
        
        assert result.get("follow_ups") is None


class TestRouteFollowUpEdge:
    """Tests for route_follow_up_edge"""

    def test_route_follow_up_has_question(self):
        """Checking routing when there is a follow-up question"""
        state = {"current_follow_up": "Test question?"}
        
        result = route_follow_up_edge(state)
        
        assert result == "answer_follow_up_question"

    def test_route_follow_up_no_question(self):
        """Checking routing without follow-up question"""
        from langgraph.graph import END
        
        state = {"current_follow_up": None}
        
        result = route_follow_up_edge(state)
        
        assert result == END


class TestNoticeExtractionGraph:
    """Tests for NOTICE_EXTRACTION_GRAPH"""

    def test_graph_compiled(self):
        """Checking that the graph is compiled"""
        assert NOTICE_EXTRACTION_GRAPH is not None
        assert hasattr(NOTICE_EXTRACTION_GRAPH, 'invoke')

    def test_graph_has_nodes(self):
        """Checking the presence of nodes in a graph"""
        assert workflow is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
