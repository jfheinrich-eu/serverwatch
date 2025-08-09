"""Report Generator for converting markdown to HTML and handling email."""

import logging
import os
import smtplib
from email.message import EmailMessage
from email.utils import formatdate
from pathlib import Path
from typing import Optional

try:
    import markdown
except ImportError:
    markdown = None  # type: ignore


class ReportGenerator:
    """Generates HTML reports and handles email sending."""

    def __init__(
        self, smtp_server: str = "localhost", smtp_port: int = 25
    ) -> None:
        """Initialize the ReportGenerator.

        Args:
            smtp_server: SMTP server hostname.
            smtp_port: SMTP server port.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown content to HTML.

        Args:
            markdown_content: The markdown content to convert.

        Returns:
            HTML representation of the markdown.

        Raises:
            ImportError: If markdown package is not installed.
        """
        if markdown is None:
            raise ImportError(
                "markdown package is required for HTML conversion"
            )

        if not markdown_content.strip():
            return "<html><body><p>No content provided</p></body></html>"

        return markdown.markdown(markdown_content)

    def save_html_report(self, html_content: str, output_path: str) -> None:
        """Save HTML content to a file.

        Args:
            html_content: The HTML content to save.
            output_path: Path where to save the HTML file.

        Raises:
            OSError: If the file cannot be written.
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

    def append_analysis_to_report(
        self,
        report_path: str,
        analysis: str,
        section_title: str = "GPT-4 Analysis & Recommendations",
    ) -> None:
        """Append analysis section to an existing report.

        Args:
            report_path: Path to the report file.
            analysis: The analysis content to append.
            section_title: Title for the analysis section.

        Raises:
            OSError: If the file cannot be accessed.
        """
        report_file = Path(report_path)

        with open(report_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n## {section_title}\n")
            f.write(analysis)

    def send_email(
        self,
        recipient: str,
        subject: str,
        html_content: str,
        attachment_path: Optional[str] = None,
    ) -> None:
        """Send an email with HTML content and optional attachment.

        Args:
            recipient: Email address of the recipient.
            subject: Email subject line.
            html_content: HTML content for the email body.
            attachment_path: Optional path to file to attach.

        Raises:
            smtplib.SMTPException: If email sending fails.
            FileNotFoundError: If attachment file doesn't exist.
        """
        msg = EmailMessage()
        msg["From"] = os.getenv("EMAIL_FROM", "serverwatch@localhost")
        msg["To"] = recipient
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)

        msg.set_content(html_content, subtype="html")

        if attachment_path and Path(attachment_path).exists():
            with open(attachment_path, "rb") as f:
                file_data = f.read()
                msg.add_attachment(
                    file_data,
                    maintype="application",
                    subtype="octet-stream",
                    filename=Path(attachment_path).name,
                )

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.send_message(msg)

    def process_report(
        self,
        markdown_path: str,
        html_path: str,
        analysis: str,
        recipient: str,
        hostname: str,
        date_str: str,
    ) -> None:
        """Process a complete report: add analysis, convert to HTML, and send.

        Args:
            markdown_path: Path to the markdown report file.
            html_path: Path where to save the HTML report.
            analysis: Analysis content to append.
            recipient: Email recipient.
            hostname: Server hostname for email subject.
            date_str: Date string for email subject.

        Raises:
            Exception: If any step of the process fails.
        """
        # Append analysis to markdown
        self.append_analysis_to_report(markdown_path, analysis)

        # Read full markdown content
        with open(markdown_path, "r", encoding="utf-8") as f:
            full_md = f.read()

        # Convert to HTML
        html_content = self.markdown_to_html(full_md)

        # Save HTML file
        self.save_html_report(html_content, html_path)

        # Send email (this would typically be handled by mutt in the original)
        subject = f"[{hostname}]: Daily Server Report {date_str}"
        try:
            self.send_email(recipient, subject, html_content, markdown_path)
        except Exception as e:
            # Log error but don't fail the entire process
            logging.warning(f"Email sending failed: {e}")
