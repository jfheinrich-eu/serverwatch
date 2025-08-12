"""Usage Example Basic"""

import os
import shutil
from tempfile import gettempdir

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

from serverwatch_analyzer import ReportGenerator, ServerAnalyzer

console: Console = Console()
try:
    script_directory: str = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(dotenv_path=script_directory + "/.env", override=True)

    api_key: str | None = os.getenv("OPENAI_API_KEY")
    recipient: str | None = os.getenv("ALERT_RECIPIENT")
    hostname: str | None = os.getenv("HOSTNAME")
    report_data_env: str | None = os.getenv("REPORT_DATA")
    report_path_env: str | None = os.getenv("REPORT_PATH")
    html_path_env: str | None = os.getenv("HTML_PATH")
    date_str: str | None = os.getenv("DATE_STR")

    if not all(
        [
            api_key,
            recipient,
            hostname,
            report_data_env,
            report_path_env,
            html_path_env,
            date_str,
        ]
    ):
        raise ValueError("One or more environment variables are not set.")

    report_data: str = f"{script_directory}/{report_data_env}"
    report_path: str = f"{gettempdir()}/{report_path_env}"
    html_path: str = f"{gettempdir()}/{html_path_env}"

    analyzer: ServerAnalyzer = ServerAnalyzer(api_key=api_key)
    report_generator: ReportGenerator = ReportGenerator()

    shutil.copy(report_data, report_path)
    logdata: str = ""
    with open(report_path, "r", encoding="utf-8") as file:
        logdata = file.read()

    analysis: str = analyzer.analyze_report(logdata)
    report_generator.append_analysis_to_report(report_path, analysis)

    console.status("Rendering report...")

    with open(report_path, "r", encoding="utf-8") as file:
        # If the report data uses literal '\\n' to represent newlines, convert them to actual paragraph breaks for markdown rendering.
        markdown_content = Markdown(file.read().replace("\\n", "\n\n"))

    with console.status("Rendering report..."):
        with open(report_path, "r", encoding="utf-8") as file:
            markdown_content = Markdown(file.read().replace("\\n", "\n\n"))

        console.print(markdown_content)
except Exception as e:
    console.print(f"Error: {e}", style="bold red")
    console.print("Failed to generate report.", style="bold red")
