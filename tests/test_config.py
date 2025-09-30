"""Tests for configuration validators and defaults."""

from opengov_earlygerman.config import Settings


def test_parse_cors_origins_from_string() -> None:
    s = Settings(cors_origins="http://a.com, http://b.com")
    assert s.cors_origins == ["http://a.com", "http://b.com"]
