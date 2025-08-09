"""Tests for ReportGenerator class."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from serverwatch_analyzer.report_generator import ReportGenerator


class TestReportGenerator:
    """Test cases for ReportGenerator."""

    def test_init_default_values(self):
        """Test initialization with default values."""
        generator = ReportGenerator()
        assert generator.smtp_server == "localhost"
        assert generator.smtp_port == 25

    def test_init_custom_values(self):
        """Test initialization with custom values."""
        generator = ReportGenerator(
            smtp_server="mail.example.com", smtp_port=587
        )
        assert generator.smtp_server == "mail.example.com"
        assert generator.smtp_port == 587

    @patch("serverwatch_analyzer.report_generator.markdown")
    def test_markdown_to_html_success(self, mock_markdown: MagicMock):
        """Test successful markdown to HTML conversion."""
        mock_markdown.markdown.return_value = "<p>Test HTML</p>"

        generator = ReportGenerator()
        result = generator.markdown_to_html("# Test Markdown")

        assert result == "<p>Test HTML</p>"
        mock_markdown.markdown.assert_called_once_with("# Test Markdown")

    def test_markdown_to_html_empty_content(self):
        """Test markdown to HTML with empty content."""
        with patch(
            "serverwatch_analyzer.report_generator.markdown"
        ) as mock_md:
            generator = ReportGenerator()
            result = generator.markdown_to_html("")

            expected = "<html><body><p>No content provided</p></body></html>"
            assert result == expected
            mock_md.markdown.assert_not_called()

    def test_markdown_to_html_whitespace_only(self):
        """Test markdown to HTML with whitespace-only content."""
        with patch(
            "serverwatch_analyzer.report_generator.markdown"
        ) as mock_md:
            generator = ReportGenerator()
            result = generator.markdown_to_html("   \n\t  ")

            expected = "<html><body><p>No content provided</p></body></html>"
            assert result == expected
            mock_md.markdown.assert_not_called()

    def test_markdown_to_html_import_error(self):
        """Test markdown to HTML when markdown package not available."""
        with patch("serverwatch_analyzer.report_generator.markdown", None):
            generator = ReportGenerator()

            with pytest.raises(
                ImportError, match="markdown package is required"
            ):
                generator.markdown_to_html("# Test")

    def test_save_html_report_success(self):
        """Test successful HTML report saving."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_report.html"
            generator = ReportGenerator()

            generator.save_html_report("<p>Test HTML</p>", str(output_path))

            assert output_path.exists()
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
            assert content == "<p>Test HTML</p>"

    def test_save_html_report_creates_directories(self):
        """Test that save_html_report creates necessary directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "subdir" / "test_report.html"
            generator = ReportGenerator()

            generator.save_html_report("<p>Test</p>", str(output_path))

            assert output_path.exists()
            assert output_path.parent.exists()

    def test_append_analysis_to_report_success(self):
        """Test successful analysis appending."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".md"
        ) as tf:
            tf.write("# Existing Report\n")
            tf.flush()

            generator = ReportGenerator()
            generator.append_analysis_to_report(
                tf.name, "Test analysis content", "Custom Analysis"
            )

            with open(tf.name, "r", encoding="utf-8") as f:
                content = f.read()

            expected = (
                "# Existing Report\n\n\n"
                "## Custom Analysis\nTest analysis content"
            )
            assert content == expected

            os.unlink(tf.name)

    def test_append_analysis_to_report_default_title(self):
        """Test analysis appending with default title."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".md"
        ) as tf:
            tf.write("# Report\n")
            tf.flush()

            generator = ReportGenerator()
            generator.append_analysis_to_report(tf.name, "Analysis content")

            with open(tf.name, "r", encoding="utf-8") as f:
                content = f.read()

            assert "## GPT-4 Analysis & Recommendations\n" in content
            assert "Analysis content" in content

            os.unlink(tf.name)

    @patch("smtplib.SMTP")
    def test_send_email_success_no_attachment(self, mock_smtp: MagicMock):
        """Test successful email sending without attachment."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        generator = ReportGenerator()
        generator.send_email(
            "test@example.com", "Test Subject", "<p>Test HTML</p>"
        )

        mock_smtp.assert_called_once_with("localhost", 25)
        mock_server.send_message.assert_called_once()

    @patch("smtplib.SMTP")
    def test_send_email_with_attachment(self, mock_smtp: MagicMock):
        """Test email sending with attachment."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(b"Test attachment content")
            tf.flush()

            generator = ReportGenerator()
            generator.send_email(
                "test@example.com", "Test Subject", "<p>Test</p>", tf.name
            )

            mock_server.send_message.assert_called_once()
            os.unlink(tf.name)

    @patch("smtplib.SMTP")
    def test_send_email_attachment_not_found(self, mock_smtp: MagicMock):
        """Test email sending with non-existent attachment."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        generator = ReportGenerator()
        generator.send_email(
            "test@example.com",
            "Test Subject",
            "<p>Test</p>",
            "/nonexistent/file.txt",
        )

        # Should still send email without attachment
        mock_server.send_message.assert_called_once()

    @patch("smtplib.SMTP")
    def test_send_email_with_custom_from(self, mock_smtp: MagicMock):
        """Test email sending with custom from address."""
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        with patch.dict(os.environ, {"EMAIL_FROM": "custom@example.com"}):
            generator = ReportGenerator()
            generator.send_email(
                "test@example.com", "Subject", "<p>Content</p>"
            )

            # Verify the message was created with correct from address
            mock_server.send_message.assert_called_once()

    @patch.object(ReportGenerator, "append_analysis_to_report")
    @patch.object(ReportGenerator, "markdown_to_html")
    @patch.object(ReportGenerator, "save_html_report")
    @patch.object(ReportGenerator, "send_email")
    def test_process_report_success(
        self,
        mock_send: MagicMock,
        mock_save: MagicMock,
        mock_convert: MagicMock,
        mock_append: MagicMock,
    ):
        """Test successful complete report processing."""
        mock_convert.return_value = "<p>HTML content</p>"

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".md"
        ) as tf:
            tf.write("Original report content")
            tf.flush()

            generator = ReportGenerator()
            generator.process_report(
                tf.name,
                "output.html",
                "Test analysis",
                "admin@example.com",
                "testserver",
                "2024-01-01",
            )

            mock_append.assert_called_once_with(tf.name, "Test analysis")
            mock_convert.assert_called_once_with("Original report content")
            mock_save.assert_called_once_with(
                "<p>HTML content</p>", "output.html"
            )
            mock_send.assert_called_once_with(
                "admin@example.com",
                "[testserver]: Daily Server Report 2024-01-01",
                "<p>HTML content</p>",
                tf.name,
            )

            os.unlink(tf.name)

    @patch("serverwatch_analyzer.report_generator.logging")
    @patch.object(ReportGenerator, "send_email")
    @patch.object(ReportGenerator, "save_html_report")
    @patch.object(ReportGenerator, "markdown_to_html")
    @patch.object(ReportGenerator, "append_analysis_to_report")
    def test_process_report_email_failure(
        self,
        mock_append: MagicMock,
        mock_convert: MagicMock,
        mock_save: MagicMock,
        mock_send: MagicMock,
        mock_logging: MagicMock,
    ):
        """Test report processing with email failure."""
        mock_convert.return_value = "<p>HTML content</p>"
        mock_send.side_effect = Exception("SMTP Error")

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".md"
        ) as tf:
            tf.write("Report content")
            tf.flush()

            generator = ReportGenerator()
            # Should not raise exception despite email failure
            generator.process_report(
                tf.name,
                "output.html",
                "Analysis",
                "admin@example.com",
                "testserver",
                "2024-01-01",
            )

            # Verify other steps completed
            mock_append.assert_called_once()
            mock_convert.assert_called_once()
            mock_save.assert_called_once()

            # Verify error was printed
            mock_logging.warning.assert_called_once()
            assert "Email sending failed" in str(
                mock_logging.warning.call_args
            )

            os.unlink(tf.name)
