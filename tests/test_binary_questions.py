"""
Unit tests for chains/binary_questions.py
"""
import pytest

from chains.binary_questions import BinaryAnswer, binary_question_prompt, BINARY_QUESTION_CHAIN


class TestBinaryAnswer:
    """Tests for the model BinaryAnswer"""

    def test_binary_answer_true(self):
        """Checking the creation of a BinaryAnswer with a value True"""
        answer = BinaryAnswer(is_true=True)
        assert answer.is_true is True
        assert isinstance(answer.is_true, bool)

    def test_binary_answer_false(self):
        """Checking the creation of a BinaryAnswer with a value False"""
        answer = BinaryAnswer(is_true=False)
        assert answer.is_true is False
        assert isinstance(answer.is_true, bool)

    def test_binary_answer_field_description(self):
        """Checking if the field description is_true"""
        field_info = BinaryAnswer.model_fields['is_true']
        assert field_info.description is not None
        assert "Whether the answer" in field_info.description


class TestBinaryQuestionPrompt:
    """Tests for prompt binary_question_prompt"""

    def test_prompt_has_messages(self):
        """Checking that the prompt contains messages"""
        assert hasattr(binary_question_prompt, 'messages')
        assert len(binary_question_prompt.messages) > 0

    def test_prompt_template_content(self):
        """Checking the contents of a prompt template"""
        prompt_str = str(binary_question_prompt)
        assert "True" in prompt_str or "False" in prompt_str
        assert "question" in prompt_str.lower()


class TestBinaryQuestionChain:
    """Tests for chain BINARY_QUESTION_CHAIN"""

    def test_chain_structure(self):
        """Checking the chain structure"""
        assert BINARY_QUESTION_CHAIN is not None
        # Check that the chain has an invoke method.
        assert hasattr(BINARY_QUESTION_CHAIN, 'invoke')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
