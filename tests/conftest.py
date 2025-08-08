"""Shared test fixtures and utilities."""

from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    client = Mock()
    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message.content = "Test analysis result"
    client.chat.completions.create.return_value = response
    return client


@pytest.fixture
def sample_report_content():
    """Sample report content for testing."""
    return """
## Service Status
### nginx
Active: active (running)

## Log Analysis
### /var/log/nginx/error.log
2024-01-01 12:00:00 [error] connection refused

## Disk Usage
/dev/sda1    10G  8.1G  1.9G  81% /
"""


@pytest.fixture
def sample_html_content():
    """Sample HTML content for testing."""
    return """
<h2>Service Status</h2>
<h3>nginx</h3>
<p>Active: active (running)</p>
"""
