"""Server Report Analyzer using OpenAI GPT."""

import os
from typing import Optional

from openai import OpenAI

# Default analysis prompt template
DEFAULT_ANALYSIS_PROMPT = """
You are a Linux security analyst. Analyze the following server report for
security issues, misconfigurations or anomalies. Provide a brief summary
and specific recommendations.

{report_content}
""".strip()

# Default system message for the AI assistant
DEFAULT_SYSTEM_MESSAGE = "You are a professional Linux admin and security expert."


class ServerAnalyzer:
    """Analyzes server reports using OpenAI GPT for security insights."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4.1-nano",
        analysis_prompt: Optional[str] = None,
        system_message: Optional[str] = None,
    ) -> None:
        """Initialize the ServerAnalyzer.

        Args:
            api_key: OpenAI API key. If None, reads from
                OPENAI_API_KEY environment variable.
            model: OpenAI model to use for analysis.
            analysis_prompt: Custom analysis prompt template. Must contain
                {report_content} placeholder. If None, uses default.
            system_message: Custom system message for the AI assistant.
                If None, uses default.

        Raises:
            ValueError: If no API key is provided or found in environment,
                or if custom analysis_prompt doesn't contain required
                placeholder.
        """
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OpenAI API key must be provided or set in OPENAI_API_KEY environment variable"
            )

        # Validate custom prompt template
        if analysis_prompt is not None:
            if "{report_content}" not in analysis_prompt:
                raise ValueError("Custom analysis_prompt must contain {report_content} placeholder")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.analysis_prompt = analysis_prompt or DEFAULT_ANALYSIS_PROMPT
        self.system_message = system_message or DEFAULT_SYSTEM_MESSAGE

    def analyze_report(self, report_content: str) -> str:
        """Analyze a server report for security issues and anomalies.

        Args:
            report_content: The content of the server report to analyze.

        Returns:
            Analysis and recommendations from GPT.

        Raises:
            ValueError: If report content is empty.
            Exception: If the GPT analysis fails.
        """
        if not report_content.strip():
            raise ValueError("Report content cannot be empty")

        # Format the prompt with the report content
        formatted_prompt = self.analysis_prompt.format(report_content=report_content)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_message,
                    },
                    {"role": "user", "content": formatted_prompt},
                ],
            )
            return response.choices[0].message.content or "No analysis returned"
        except Exception as e:
            raise Exception(f"Error in GPT analysis: {str(e)}") from e

    def get_model(self) -> str:
        """Get the current model being used.

        Returns:
            The model name.
        """
        return self.model

    def set_model(self, model: str) -> None:
        """Set the model to use for analysis.

        Args:
            model: The OpenAI model name to use.
        """
        self.model = model

    def get_analysis_prompt(self) -> str:
        """Get the current analysis prompt template.

        Returns:
            The analysis prompt template string.
        """
        return self.analysis_prompt

    def set_analysis_prompt(self, prompt: str) -> None:
        """Set a custom analysis prompt template.

        Args:
            prompt: The prompt template. Must contain {report_content}
                placeholder.

        Raises:
            ValueError: If prompt doesn't contain required placeholder.
        """
        if "{report_content}" not in prompt:
            raise ValueError("Analysis prompt must contain {report_content} placeholder")
        self.analysis_prompt = prompt

    def get_system_message(self) -> str:
        """Get the current system message.

        Returns:
            The system message string.
        """
        return self.system_message

    def set_system_message(self, message: str) -> None:
        """Set a custom system message for the AI assistant.

        Args:
            message: The system message to use.
        """
        self.system_message = message

    @staticmethod
    def get_default_analysis_prompt() -> str:
        """Get the default analysis prompt template.

        Returns:
            The default analysis prompt template.
        """
        return DEFAULT_ANALYSIS_PROMPT

    @staticmethod
    def get_default_system_message() -> str:
        """Get the default system message.

        Returns:
            The default system message.
        """
        return DEFAULT_SYSTEM_MESSAGE
