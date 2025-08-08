"""Server Report Analyzer using OpenAI GPT."""

import os
from typing import Optional

from openai import OpenAI


class ServerAnalyzer:
    """Analyzes server reports using OpenAI GPT for security insights."""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "gpt-4.1-nano"
    ) -> None:
        """Initialize the ServerAnalyzer.

        Args:
            api_key: OpenAI API key. If None, reads from
                OPENAI_API_KEY environment variable.
            model: OpenAI model to use for analysis.

        Raises:
            ValueError: If no API key is provided or found in environment.
        """
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OpenAI API key must be provided or set in "
                "OPENAI_API_KEY environment variable"
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def analyze_report(self, report_content: str) -> str:
        """Analyze a server report for security issues and anomalies.

        Args:
            report_content: The content of the server report to analyze.

        Returns:
            Analysis and recommendations from GPT.

        Raises:
            Exception: If the GPT analysis fails.
        """
        if not report_content.strip():
            raise ValueError("Report content cannot be empty")

        prompt = f"""
You are a Linux security analyst. Analyze the following server report for
security issues, misconfigurations or anomalies. Provide a brief summary
and specific recommendations.

{report_content}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional Linux admin and "
                            "security expert."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            return (
                response.choices[0].message.content or "No analysis returned"
            )
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
