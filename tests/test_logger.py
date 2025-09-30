"""Tests for logger configuration branches."""

from opengov_earlygerman.utils.logger import get_logger
from opengov_earlygerman import config as cfg


def test_get_logger_console_format(monkeypatch) -> None:
    # Force non-JSON branch
    monkeypatch.setattr(cfg.settings, "log_format", "console")
    logger = get_logger(__name__)
    # Basic assertion: logger is created and usable
    logger.info("test message")
