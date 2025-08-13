#!/usr/bin/env python3
"""
Advanced Security Analysis CLI Tool for ServerWatch
===================================================

A practical command-line tool for DevOps engineers to perform ad-hoc security
analysis of server reports using OpenAI's language models.

Features:
- Rich console output with syntax highlighting
- Custom security-focused AI prompts
- Real-time analysis of server monitoring data
- Detailed threat assessment and remediation recommendations

Usage:
    python security_analysis_cli.py

Author: DevOps Team
"""

import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from rich.syntax import Syntax
from rich.table import Table

from serverwatch_analyzer import ServerAnalyzer


class SecurityAnalysisCLI:
    """Advanced CLI tool for server security analysis."""

    def __init__(self) -> None:
        """Initialize the CLI tool."""
        self.console = Console()
        self.analyzer: Optional[ServerAnalyzer] = None

        # Load environment variables
        env_path = Path(__file__).parent / ".env"
        load_dotenv(env_path)

    def setup_analyzer(self) -> bool:
        """Setup the ServerAnalyzer with custom security prompt."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.console.print("❌ [red]Error: OPENAI_API_KEY not found in .env file[/red]")
            return False

        # Custom security-focused analysis prompt
        security_prompt = """
You are a senior cybersecurity analyst and DevOps expert with 15+ years
of experience in enterprise security operations. Analyze the following
server report with focus on:

🔒 SECURITY THREATS & VULNERABILITIES:
- Identify active security threats and attack vectors
- Assess vulnerable services and misconfigurations
- Evaluate authentication and access control issues
- Check for suspicious network activity and connections

⚡ IMMEDIATE ACTION ITEMS:
- Critical security issues requiring immediate attention
- Prioritized remediation steps with urgency levels
- Specific commands and configuration changes needed

🛡️ HARDENING RECOMMENDATIONS:
- Security best practices implementation
- System hardening measures
- Monitoring and alerting improvements
- Compliance considerations (SOC2, ISO27001, PCI-DSS)

📊 RISK ASSESSMENT:
- Risk levels: CRITICAL, HIGH, MEDIUM, LOW
- Business impact analysis
- Exploit probability and potential damage

Provide actionable, specific recommendations with exact commands when
possible.

SERVER REPORT DATA:
{report_content}

Format your response as structured markdown with clear sections and
actionable items.
"""

        try:
            self.analyzer = ServerAnalyzer(
                api_key=api_key,
                model="gpt-4o-mini",  # Cost-effective for DevOps usage
                analysis_prompt=security_prompt,
            )
            return True
        except Exception as e:
            self.console.print(f"❌ [red]Error setting up analyzer: {e}[/red]")
            return False

    def get_sample_server_report(self) -> str:
        """Generate realistic server report data for analysis."""
        hostname = os.getenv("HOSTNAME", "prod-web-01")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"""
# Server Security Report - {hostname}
Generated: {current_time}

## System Information
- Hostname: {hostname}
- OS: Ubuntu 22.04.3 LTS
- Kernel: 5.15.0-78-generic
- Uptime: 47 days, 12 hours
- Load Average: 2.34, 1.89, 1.67

## Security Events (Last 24h)
### Failed SSH Login Attempts
- 23 failed login attempts from IP 192.168.1.100
- 45 failed login attempts from IP 203.0.113.15 (EXTERNAL)
- 12 failed login attempts from IP 198.51.100.42 (EXTERNAL)

### Authentication Logs
```
Aug 13 14:23:15 {hostname} sshd[12345]: Failed password for root from \\
203.0.113.15 port 22 ssh2
Aug 13 14:23:18 {hostname} sshd[12346]: Failed password for admin from \\
203.0.113.15 port 22 ssh2
Aug 13 14:24:01 {hostname} sudo: devops : TTY=pts/0 ; PWD=/home/devops ; \\
USER=root ; COMMAND=/bin/cat /etc/shadow
Aug 13 14:25:33 {hostname} sshd[12389]: Accepted publickey for devops \\
from 10.0.1.50 port 22 ssh2
```

## Network Security
### Open Ports (nmap scan)
- 22/tcp (SSH) - OPEN - OpenSSH 8.9p1
- 80/tcp (HTTP) - OPEN - nginx 1.22.1
- 443/tcp (HTTPS) - OPEN - nginx 1.22.1
- 3306/tcp (MySQL) - OPEN - MySQL 8.0.34 (EXTERNAL ACCESS!)
- 6379/tcp (Redis) - OPEN - Redis 7.0.12 (NO AUTH!)

### Suspicious Network Activity
- Unusual outbound connections to 185.220.101.5:9050 (Tor exit node)
- High volume traffic to 172.16.254.1 (Internal network scanning?)
- Multiple connections to pastebin.com from web service

## Service Status
### Critical Services
- nginx: RUNNING (PID 1234) - SSL cert expires in 7 days
- mysql: RUNNING (PID 5678) - root password = 'password123'  # pragma: allowlist secret
- redis: RUNNING (PID 9012) - No authentication configured
- fail2ban: STOPPED - Last seen 3 days ago
- ufw: INACTIVE - Firewall disabled

### Process Analysis
```
root      1234  0.1  0.5  /usr/sbin/nginx
mysql     5678  2.3  8.2  /usr/sbin/mysqld --bind-address=0.0.0.0
redis     9012  0.8  1.2  /usr/bin/redis-server *:6379
nobody   15432  0.0  0.1  /tmp/.hidden/cryptominer --quiet
```

## File System Security
### Suspicious Files
- /tmp/.hidden/cryptominer (executable, 2.3MB, created 2 days ago)
- /var/www/html/admin/backdoor.php (PHP shell, modified 1 hour ago)
- /home/devops/.ssh/authorized_keys (world-writable!)

### Permission Issues
- /etc/shadow: 644 (should be 640)
- /var/log/auth.log: 666 (should be 640)
- /home/devops/.ssh: 777 (should be 700)

## System Updates
- 23 security updates pending (including kernel)
- Last update: 45 days ago
- Critical CVEs: CVE-2023-38408 (SSH), CVE-2023-32067 (MySQL)

## Compliance Issues
- PCI-DSS: FAILED - Database accessible externally
- SOC2: FAILED - No audit logging enabled
- GDPR: WARNING - Unencrypted user data in /var/backups/

## Recommendations Needed
1. Immediate security threat mitigation
2. Service hardening and access control
3. Network segmentation and firewall rules
4. Monitoring and alerting setup
5. Compliance remediation steps
"""

    def display_header(self) -> None:
        """Display the application header."""
        header = Panel.fit(
            "[bold blue]🔒 ServerWatch Security Analyzer CLI[/bold blue]\n"
            "[dim]Advanced Security Analysis for DevOps Engineers[/dim]",
            border_style="blue",
        )
        self.console.print(header)
        self.console.print()

    def display_report_preview(self, report_content: str) -> None:
        """Display a preview of the server report."""
        self.console.print("[bold yellow]📊 Server Report Preview:[/bold yellow]")

        # Show first few lines of the report
        lines = report_content.strip().split("\n")
        preview_lines = lines[:15]
        preview_text = "\n".join(preview_lines)

        if len(lines) > 15:
            extra_lines = len(lines) - 15
            preview_text += f"\n\n[dim]... ({extra_lines} more lines)[/dim]"

        syntax = Syntax(preview_text, "markdown", theme="monokai", line_numbers=True)
        self.console.print(Panel(syntax, title="Raw Server Report", border_style="yellow"))
        self.console.print()

    def analyze_with_progress(self, report_content: str) -> str:
        """Perform analysis with progress indicator."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:

            task = progress.add_task("🧠 Analyzing server report with AI...", total=None)

            try:
                analysis_result = (
                    self.analyzer.analyze_report(report_content) if self.analyzer else ""
                )
                progress.update(task, completed=True)
                return analysis_result
            except Exception as e:
                progress.update(task, completed=True)
                raise e

    def display_analysis_results(self, analysis: str) -> None:
        """Display the analysis results with rich formatting."""
        self.console.print("[bold green]🔍 Security Analysis Results:[/bold green]")
        self.console.print()

        # Parse and display as markdown
        markdown = Markdown(analysis)
        self.console.print(
            Panel(
                markdown,
                title="🛡️ Security Assessment Report",
                border_style="green",
                padding=(1, 2),
            )
        )

    def display_summary_table(self) -> None:
        """Extract and display a summary table of findings."""
        self.console.print("\n[bold cyan]📋 Executive Summary:[/bold cyan]")

        table = Table(
            title="Security Findings Overview",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Risk Level", style="bold", width=12)
        table.add_column("Category", style="bold", width=20)
        table.add_column("Finding", width=50)
        table.add_column("Priority", justify="center", width=10)

        # Sample findings - in real scenario, parse the AI response
        findings = [
            (
                "🔴 CRITICAL",
                "Authentication",
                "MySQL accessible externally with weak password",
                "P0",
            ),
            (
                "🔴 CRITICAL",
                "Malware",
                "Crypto miner detected in /tmp/.hidden/",
                "P0",
            ),
            (
                "🟠 HIGH",
                "Network Security",
                "Redis server without authentication",
                "P1",
            ),
            (
                "🟠 HIGH",
                "File Security",
                "SSH keys with incorrect permissions",
                "P1",
            ),
            (
                "🟡 MEDIUM",
                "System Updates",
                "23 pending security updates",
                "P2",
            ),
            (
                "🟡 MEDIUM",
                "SSL/TLS",
                "SSL certificate expires in 7 days",
                "P2",
            ),
        ]

        for risk, category, finding, priority in findings:
            table.add_row(risk, category, finding, priority)

        self.console.print(table)

    def save_report_option(self, analysis: str) -> None:
        """Offer to save the analysis report."""
        self.console.print()
        save_prompt = "💾 [bold blue]Save analysis report to file?[/bold blue]"
        if Confirm.ask(save_prompt):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_analysis_{timestamp}.md"

            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("# Security Analysis Report\n")
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"Generated: {timestamp}\n\n")
                    f.write(analysis)

                save_msg = f"✅ [green]Report saved to: {filename}[/green]"
                self.console.print(save_msg)
            except Exception as e:
                self.console.print(f"❌ [red]Error saving report: {e}[/red]")

    def run(self) -> int:
        """Main CLI execution flow."""
        self.display_header()

        # Setup analyzer
        if not self.setup_analyzer():
            return 1

        success_msg = "✅ [green]Security analyzer initialized successfully[/green]"
        self.console.print(success_msg)
        self.console.print()

        # Get server report data
        report_content = self.get_sample_server_report()

        # Display report preview
        self.display_report_preview(report_content)

        # Confirm analysis
        if not Confirm.ask("🚀 [bold blue]Proceed with security analysis?[/bold blue]"):
            self.console.print("👋 [yellow]Analysis cancelled by user[/yellow]")
            return 0

        try:
            # Perform analysis
            analysis_result = self.analyze_with_progress(report_content)

            # Display results
            self.display_analysis_results(analysis_result)
            self.display_summary_table()

            # Save option
            self.save_report_option(analysis_result)

            self.console.print(
                "\n🎉 [bold green]Security analysis completed " "successfully![/bold green]"
            )

        except Exception as e:
            self.console.print(f"\n❌ [bold red]Analysis failed: {e}[/bold red]")
            return 1

        return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ServerWatch Security Analysis CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python security_analysis_cli.py          # Run interactive analysis

Environment:
  Requires OPENAI_API_KEY in examples/.env file
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version="ServerWatch Security CLI v1.0.0",
    )

    parser.parse_args()

    try:
        cli = SecurityAnalysisCLI()
        return cli.run()
    except KeyboardInterrupt:
        print("\n👋 Analysis interrupted by user")
        return 130
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
