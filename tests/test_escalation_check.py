"""
Unit tests for chains/escalation_check.py
"""
import pytest

from chains.escalation_check import EscalationCheck, escalation_prompt, ESCALATION_CHECK_CHAIN


class TestEscalationCheck:
    """Tests for EscalationCheck model"""

    def test_escalation_check_true(self):
        """Checking the creation of EscalationCheck with needs_escalation=True"""
        check = EscalationCheck(needs_escalation=True)
        assert check.needs_escalation is True
        assert isinstance(check.needs_escalation, bool)

    def test_escalation_check_false(self):
        """Checking the creation of EscalationCheck with needs_escalation=False"""
        check = EscalationCheck(needs_escalation=False)
        assert check.needs_escalation is False
        assert isinstance(check.needs_escalation, bool)

    def test_escalation_check_field_description(self):
        """Checking if a field description needs_escalation exists"""
        field_info = EscalationCheck.model_fields['needs_escalation']
        assert field_info.description is not None
        assert "escalation" in field_info.description.lower()


class TestEscalationPrompt:
    """Tests for escalation_prompt"""

    def test_prompt_has_messages(self):
        """Checking that the prompt contains messages"""
        assert hasattr(escalation_prompt, 'messages')
        assert len(escalation_prompt.messages) > 0

    def test_prompt_template_variables(self):
        """Checking for the presence of variables in a prompt template"""
        prompt_str = str(escalation_prompt)
        assert "escalation_criteria" in prompt_str or "message" in prompt_str.lower()
        assert "notice" in prompt_str.lower() or "escalation" in prompt_str.lower()


class TestEscalationCheckChain:
    """Tests for ESCALATION_CHECK_CHAIN"""

    def test_chain_structure(self):
        """Checking the chain structure"""
        assert ESCALATION_CHECK_CHAIN is not None
        # Check that the chain has an invoke method
        assert hasattr(ESCALATION_CHECK_CHAIN, 'invoke')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
