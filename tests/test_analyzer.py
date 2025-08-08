"""Tests for ServerAnalyzer class."""

import os
from unittest.mock import MagicMock, patch

import pytest

from serverwatch_analyzer.analyzer import ServerAnalyzer


class TestServerAnalyzer:
    """Test cases for ServerAnalyzer."""

    def test_init_with_api_key(self):
        """Test initialization with provided API key."""
        with patch("serverwatch_analyzer.analyzer.OpenAI") as mock_openai:
            # pragma: allowlist secret
            analyzer = ServerAnalyzer(api_key="test-key")
            # pragma: allowlist secret
            mock_openai.assert_called_once_with(api_key="test-key")
            assert analyzer.model == "gpt-4.1-nano"

    def test_init_with_env_api_key(self):
        """Test initialization with API key from environment."""
        # pragma: allowlist secret
        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"}):
            with patch("serverwatch_analyzer.analyzer.OpenAI") as mock_openai:
                ServerAnalyzer()
                mock_openai.assert_called_once_with(api_key="env-key")

    def test_init_without_api_key_raises_error(self):
        """Test initialization without API key raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(
                ValueError, match="OpenAI API key must be provided"
            ):
                ServerAnalyzer()

    def test_init_with_custom_model(self):
        """Test initialization with custom model."""
        with patch("serverwatch_analyzer.analyzer.OpenAI"):
            analyzer = ServerAnalyzer(
                api_key="test-key", model="gpt-3.5-turbo"
            )
            assert analyzer.model == "gpt-3.5-turbo"

    def test_analyze_report_success(self, mock_openai_client: MagicMock):
        """Test successful report analysis."""
        with patch(
            "serverwatch_analyzer.analyzer.OpenAI",
            return_value=mock_openai_client,
        ):
            analyzer = ServerAnalyzer(api_key="test-key")
            result = analyzer.analyze_report("Test report content")

            assert result == "Test analysis result"
            mock_openai_client.chat.completions.create.assert_called_once()

            call_args = mock_openai_client.chat.completions.create.call_args
            assert call_args[1]["model"] == "gpt-4.1-nano"
            assert len(call_args[1]["messages"]) == 2
            assert (
                "Linux security analyst"
                in call_args[1]["messages"][1]["content"]
            )

    def test_analyze_report_empty_content_raises_error(self):
        """Test analysis with empty content raises ValueError."""
        with patch("serverwatch_analyzer.analyzer.OpenAI"):
            analyzer = ServerAnalyzer(api_key="test-key")

            with pytest.raises(
                ValueError, match="Report content cannot be empty"
            ):
                analyzer.analyze_report("")

            with pytest.raises(
                ValueError, match="Report content cannot be empty"
            ):
                analyzer.analyze_report("   ")

    def test_analyze_report_api_error(self, mock_openai_client: MagicMock):
        """Test handling of API errors during analysis."""
        mock_openai_client.chat.completions.create.side_effect = Exception(
            "API Error"
        )

        with patch(
            "serverwatch_analyzer.analyzer.OpenAI",
            return_value=mock_openai_client,
        ):
            analyzer = ServerAnalyzer(api_key="test-key")

            with pytest.raises(
                Exception, match="Error in GPT analysis: API Error"
            ):
                analyzer.analyze_report("Test content")

    def test_analyze_report_no_content_returned(
        self, mock_openai_client: MagicMock
    ):
        """Test handling when API returns no content."""
        mock_openai_client.chat.completions.create.return_value.choices[
            0
        ].message.content = None

        with patch(
            "serverwatch_analyzer.analyzer.OpenAI",
            return_value=mock_openai_client,
        ):
            analyzer = ServerAnalyzer(api_key="test-key")
            result = analyzer.analyze_report("Test content")

            assert result == "No analysis returned"

    def test_get_model(self):
        """Test getting current model."""
        with patch("serverwatch_analyzer.analyzer.OpenAI"):
            analyzer = ServerAnalyzer(
                api_key="test-key", model="gpt-3.5-turbo"
            )
            assert analyzer.get_model() == "gpt-3.5-turbo"

    def test_set_model(self):
        """Test setting model."""
        with patch("serverwatch_analyzer.analyzer.OpenAI"):
            analyzer = ServerAnalyzer(api_key="test-key")
            analyzer.set_model("gpt-3.5-turbo")
            assert analyzer.model == "gpt-3.5-turbo"

    def test_analyze_report_with_custom_model(
        self, mock_openai_client: MagicMock
    ):
        """Test analysis with custom model."""
        with patch(
            "serverwatch_analyzer.analyzer.OpenAI",
            return_value=mock_openai_client,
        ):
            analyzer = ServerAnalyzer(api_key="test-key", model="custom-model")
            analyzer.analyze_report("Test content")

            call_args = mock_openai_client.chat.completions.create.call_args
            assert call_args[1]["model"] == "custom-model"

    def test_analyze_report_prompt_includes_content(
        self, mock_openai_client: MagicMock
    ):
        """Test that the prompt includes the report content."""
        test_content = "Specific test content for analysis"

        with patch(
            "serverwatch_analyzer.analyzer.OpenAI",
            return_value=mock_openai_client,
        ):
            analyzer = ServerAnalyzer(api_key="test-key")
            analyzer.analyze_report(test_content)

            call_args = mock_openai_client.chat.completions.create.call_args
            user_message = call_args[1]["messages"][1]["content"]
            assert test_content in user_message

    def test_analyze_report_system_message(
        self, mock_openai_client: MagicMock
    ):
        """Test that system message is properly set."""
        with patch(
            "serverwatch_analyzer.analyzer.OpenAI",
            return_value=mock_openai_client,
        ):
            analyzer = ServerAnalyzer(api_key="test-key")
            analyzer.analyze_report("Test content")

            call_args = mock_openai_client.chat.completions.create.call_args
            system_message = call_args[1]["messages"][0]
            assert system_message["role"] == "system"
            assert "professional Linux admin" in system_message["content"]
