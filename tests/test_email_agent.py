"""
Unit tests for graphs/email_agent.py
"""
import pytest
from unittest.mock import Mock, patch

from graphs.email_agent import (
    forward_email,
    send_wrong_email_notification_to_sender,
    extract_notice_data,
    determine_email_action,
    call_agent_model_node,
    route_agent_graph_edge,
    tools,
    tool_node,
    email_agent_graph,
)
from langchain_core.messages import AIMessage, HumanMessage


class TestForwardEmailTool:
    """Tests the tool forward_email"""

    @patch('graphs.email_agent.LOGGER')
    @patch('graphs.email_agent.time.sleep', return_value=None)
    def test_forward_email_success(self, mock_sleep, mock_logger):
        """Checking if email forwarding was successful"""
        result = forward_email.invoke({
            "email_message": "Test message",
            "send_to_email": "test@example.com"
        })
        
        assert result is True
        mock_logger.info.assert_any_call("Forwarding the email to test@example.com...")
        mock_logger.info.assert_any_call("Email forwarded!")
        mock_sleep.assert_called_once()


class TestSendWrongEmailNotificationTool:
    """Tests the tool send_wrong_email_notification_to_sender"""

    @patch('graphs.email_agent.LOGGER')
    @patch('graphs.email_agent.time.sleep', return_value=None)
    def test_send_wrong_email_notification(self, mock_sleep, mock_logger):
        """Checking if an invalid email notification has been sent"""
        result = send_wrong_email_notification_to_sender.invoke({
            "sender_email": "sender@example.com",
            "correct_department": "billing@company.com"
        })
        
        assert result is True
        mock_logger.info.assert_any_call("Sending wrong email notification to sender@example.com...")
        mock_logger.info.assert_any_call("Email sent!")
        mock_sleep.assert_called_once()


class TestExtractNoticeDataTool:
    """Tests the tool extract_notice_data"""

    @patch('graphs.email_agent.NOTICE_EXTRACTION_GRAPH')
    @patch('graphs.email_agent.LOGGER')
    def test_extract_notice_data(self, mock_logger, mock_graph):
        """Checking the data extraction notice"""
        mock_result = {
            "notice_email_extract": Mock(
                entity_name="Test Entity",
                project_id=12345,
            )
        }
        mock_graph.invoke.return_value = mock_result
        
        result = extract_notice_data.invoke({
            "email": "Test email content",
            "escalation_criteria": "immediate danger"
        })
        
        assert result is not None
        mock_graph.invoke.assert_called_once()
        mock_logger.info.assert_any_call("Calling the email notice extraction graph...")


class TestDetermineEmailActionTool:
    """Tests the tool determine_email_action"""

    def test_determine_email_action_returns_string(self):
        """Checking that the tool returns a string"""
        result = determine_email_action.invoke({"email": "Test email"})
        
        assert isinstance(result, str)
        assert len(result) > 0


class TestCallAgentModelNode:
    """Tests for the call_agent_model_node"""

    @patch('graphs.email_agent.EMAIL_AGENT_MODEL')
    def test_call_agent_model_node(self, mock_model):
        """Checking the agent model call node"""
        mock_response = AIMessage(content="Test response")
        mock_model.invoke.return_value = mock_response
        
        state = {
            "messages": [HumanMessage(content="Test message")]
        }
        
        result = call_agent_model_node(state)
        
        assert "messages" in result
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], AIMessage)
        mock_model.invoke.assert_called_once()


class TestRouteAgentGraphEdge:
    """Tests for route_agent_graph_edge"""

    def test_route_agent_graph_with_tool_calls(self):
        """Checking routing in the presence of tool calls"""
        last_message = AIMessage(
            content="",
            tool_calls=[{"name": "test_tool", "args": {}, "id": "1"}]
        )
        state = {"messages": [last_message]}
        
        result = route_agent_graph_edge(state)
        
        assert result == "email_tools"

    def test_route_agent_graph_without_tool_calls(self):
        """Checking routing without tool calls"""
        from langgraph.graph import END
        
        last_message = AIMessage(content="Test response")
        state = {"messages": [last_message]}
        
        result = route_agent_graph_edge(state)
        
        assert result == END


class TestTools:
    """Tests for tools"""

    def test_tools_not_empty(self):
        """Checking that the list of tools is not empty"""
        assert len(tools) > 0

    def test_tools_contains_expected_tools(self):
        """Checking the availability of expected tools"""
        tool_names = [tool.name for tool in tools]
        
        assert "forward_email" in tool_names
        assert "send_wrong_email_notification_to_sender" in tool_names
        assert "extract_notice_data" in tool_names
        assert "determine_email_action" in tool_names


class TestEmailAgentGraph:
    """Tests for email_agent_graph"""

    def test_graph_compiled(self):
        """Checking that the graph is compiled"""
        assert email_agent_graph is not None
        assert hasattr(email_agent_graph, 'invoke')

    def test_tool_node_exists(self):
        """Checking tool_node exists"""
        assert tool_node is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
