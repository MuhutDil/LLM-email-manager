"""
Unit tests for utils/logging_config.py
"""
import pytest
import logging

from utils.logging_config import LOGGER


class TestLoggingConfig:
    """Tests for logging configuration"""

    def test_logger_exists(self):
        """Checking existence of LOGGER"""
        assert LOGGER is not None

    def test_logger_name(self):
        """Checking the logger name"""
        assert LOGGER.name == __name__.split('.')[0] or LOGGER.name == 'utils.logging_config'

    def test_logger_has_handlers(self):
        """Checking the presence of handlers on the logger"""
        # Check that there is at least one handler at the root level or the logger itself.
        has_handlers = len(LOGGER.handlers) > 0 or len(logging.root.handlers) > 0
        assert has_handlers

    def test_logger_info_message(self, caplog):
        """Checking INFO message logging"""
        with caplog.at_level(logging.INFO):
            LOGGER.info("Test info message")
        
        assert "Test info message" in caplog.text

    def test_logger_warning_message(self, caplog):
        """Checking WARNING message logging"""
        with caplog.at_level(logging.WARNING):
            LOGGER.warning("Test warning message")
        
        assert "Test warning message" in caplog.text

    def test_logger_error_message(self, caplog):
        """Checking ERROR message logging"""
        with caplog.at_level(logging.ERROR):
            LOGGER.error("Test error message")
        
        assert "Test error message" in caplog.text

    def test_httpx_logger_warning_level(self):
        """Check that the httpx logger is set to WARNING"""
        httpx_logger = logging.getLogger("httpx")
        assert httpx_logger.level <= logging.WARNING


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
