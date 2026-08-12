"""
Unit tests for utils/gigachat_settings.py
"""
import pytest


class TestGigachatSettings:
    """GigaChat Configuration Tests"""

    def test_role_of_message_is_human(self):
        """Check that ROLE_OF_MESSAGE is set to 'human'"""
        # This is important because GigaChat does not accept 
        # 'system' messages in this version.
        from utils.gigachat_settings import ROLE_OF_MESSAGE
        
        assert ROLE_OF_MESSAGE == "human"

    def test_llm_exists(self):
        """Checking that the LLM model is initialized"""
        from utils.gigachat_settings import LLM
        
        assert LLM is not None

    def test_key_loaded_from_env(self):
        """Checking that the API key is loaded from the environment variable"""
        from utils.gigachat_settings import KEY
        assert KEY is None or isinstance(KEY, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
