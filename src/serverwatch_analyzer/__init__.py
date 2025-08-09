"""ServerWatch Analyzer Package.

A Python package for analyzing server reports and generating security insights
using OpenAI GPT models.
"""

from .analyzer import ServerAnalyzer
from .report_generator import ReportGenerator

__all__ = ["ServerAnalyzer", "ReportGenerator"]
__version__ = "0.1.0"
