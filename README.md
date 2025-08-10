# ServerWatch Analyzer

[![Python CI](https://github.com/jfheinrich-eu/serverwatch/actions/workflows/python.yml/badge.svg)](https://github.com/jfheinrich-eu/serverwatch/actions/workflows/python.yml)
[![Integration Test](https://github.com/jfheinrich-eu/serverwatch/actions/workflows/integration.yml/badge.svg)](https://github.com/jfheinrich-eu/serverwatch/actions/workflows/integration.yml)
[![codecov](https://codecov.io/gh/jfheinrich-eu/serverwatch/branch/main/graph/badge.svg)](https://codecov.io/gh/jfheinrich-eu/serverwatch)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A Python package for analyzing server reports and generating security insights using OpenAI's language models.

## 🚀 Features

- **Automated Report Analysis**: Parse and analyze server monitoring reports
- **Security Insights**: Generate actionable security recommendations
- **OpenAI Integration**: Leverage GPT models for intelligent analysis
- **Flexible Output**: Generate reports in multiple formats (Markdown, HTML, etc.)
- **Easy Integration**: Simple API for embedding into existing workflows

## 📋 Requirements

- Python 3.9 or higher
- OpenAI API key
- Valid server reports (supported formats: text, JSON, XML)

## 🛠️ Installation

### From PyPI (Coming Soon)

```bash
pip install serverwatch-analyzer
```

### From Source

```bash
git clone https://github.com/jfheinrich-eu/serverwatch.git
cd serverwatch
make install
```

### Development Installation

```bash
git clone https://github.com/jfheinrich-eu/serverwatch.git
cd serverwatch
make install-dev
```

### Complete Development Setup with Virtual Environment

For a complete isolated development environment:

```bash
git clone https://github.com/jfheinrich-eu/serverwatch.git
cd serverwatch

# Option 1: Automated setup (recommended)
make dev-setup

# Option 2: Quick activation script
./activate-dev.sh

# Option 3: Manual setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

This creates a virtual environment in `.venv/` with all dependencies installed. VSCode will automatically detect and use this environment.

### 🐳 DevContainer Development (Recommended)

For the most consistent development experience with automatic environment persistence:

```bash
# Open in DevContainer (VS Code)
1. Install "Dev Containers" extension
2. Cmd+Shift+P → "Dev Containers: Open Folder in Container"
3. ✨ Everything is automatically set up!

# Features:
- ✅ Persistent virtual environment across container rebuilds
- ✅ Pre-configured Python development tools
- ✅ Automated dependency management with lock files
- ✅ Pre-commit hooks installed and ready
- ✅ 40+ VS Code extensions for Python development
```

The DevContainer automatically:

- Creates and maintains a persistent `.venv/` virtual environment
- Installs exact dependencies from `requirements-dev.lock`
- Configures VS Code settings for optimal Python development
- Sets up linting, formatting, and testing tools
- Survives container rebuilds with zero manual intervention

**Test your environment**: Run `./test-persistence.sh` to validate the setup.

📚 **For detailed DevContainer persistence info**: See [`docs/DEVCONTAINER_PERSISTENCE.md`](docs/DEVCONTAINER_PERSISTENCE.md)

## 🔧 Configuration

1. Set your OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY="your-api-key-here" # pragma: allowlist secret
   ```

2. Or create a `.env` file in your project root:

   ```env
   OPENAI_API_KEY=your-api-key-here # pragma: allowlist secret
   ```

## 🚦 Quick Start

### Basic Usage

```python
from serverwatch_analyzer import ServerAnalyzer

# Initialize the analyzer
analyzer = ServerAnalyzer()

# Analyze a server report
report_path = "path/to/your/server_report.txt"
analysis = analyzer.analyze_report(report_path)

# Generate insights
insights = analyzer.generate_insights(analysis)
print(insights)
```

### Advanced Usage

```python
from serverwatch_analyzer import ServerAnalyzer, ReportGenerator

# Initialize with custom settings and prompts
custom_prompt = """
Analyze this server report for security compliance:
Focus on PCI DSS and SOC 2 requirements.

{report_content}
"""

analyzer = ServerAnalyzer(
    model="gpt-4",
    analysis_prompt=custom_prompt,
    system_message="You are a security compliance auditor."
)

# Read and analyze a report
with open("server_report.txt", "r") as f:
    report_content = f.read()

analysis = analyzer.analyze_report(report_content)

# Generate comprehensive report
generator = ReportGenerator()
markdown_report = generator.generate_markdown_report(analysis)

# Save report
with open("security_analysis.md", "w") as f:
    f.write(markdown_report)
```

### Customizable Analysis Prompts

The analyzer supports fully customizable analysis prompts and system messages:

```python
# Security-focused analysis
security_analyzer = ServerAnalyzer(
    analysis_prompt="""
    Perform a security audit focusing on:
    1. Vulnerability assessment
    2. Access control review
    3. Network security evaluation

    Server Report: {report_content}
    """,
    system_message="You are a certified security auditor."
)

# Performance-focused analysis
performance_analyzer = ServerAnalyzer(
    analysis_prompt="""
    Analyze performance metrics and identify bottlenecks:
    {report_content}
    """,
    system_message="You are a performance optimization specialist."
)
```

For detailed prompt customization guide, see [docs/PROMPT_CUSTOMIZATION.md](docs/PROMPT_CUSTOMIZATION.md)
generator.save_report(comprehensive_report, "security_analysis.md")

## 📖 API Reference

### ServerAnalyzer

The main class for analyzing server reports.

#### Methods

- `analyze_report(report_path: str) -> Dict`: Analyze a single server report
- `generate_insights(analysis: Dict) -> str`: Generate human-readable insights
- `batch_analyze(report_paths: List[str]) -> List[Dict]`: Analyze multiple reports

#### Parameters

- `model` (str): OpenAI model to use (default: "gpt-3.5-turbo")
- `temperature` (float): Model temperature (default: 0.2)
- `max_tokens` (int): Maximum tokens in response (default: 500)

### ReportGenerator

Utility class for generating formatted reports.

#### ReportGenerator Methods

- `generate_report(analyses: List[Dict], **kwargs) -> str`: Generate formatted report
- `save_report(content: str, filename: str) -> None`: Save report to file

## 🧪 Testing

Run the test suite using the Makefile:

```bash
# Run all tests with coverage
make test

# Run complete code quality checks
make check

# Validate package before release
make package-check
```

For manual testing:

```bash
# Install in development mode first
make install-dev

# Run tests manually
pytest tests/ -v --cov=src --cov-report=html
```

## 🔍 Code Quality and Linting

The project uses several tools for maintaining code quality. Use the Makefile for convenience:

```bash
# Format code (black + isort)
make format

# Run linting (flake8 + pylint)
make lint

# Run type checking (mypy)
make type-check

# Run all quality checks at once
make check

# Setup pre-commit hooks
make pre-commit-install

# Run pre-commit on all files
make pre-commit-run

# Auto-fix formatting issues only
make pre-commit-fix
```

### Auto-Formatting

The project includes comprehensive auto-formatting tools:

```bash
# Quick fix for common issues
make pre-commit-fix

# This automatically runs:
# - isort (import sorting)
# - black (code formatting)
# - autopep8 (PEP8 compliance including line length)
# - prettier (YAML/JSON formatting)
# - markdownlint (Markdown fixes)
```

Manual usage:

```bash
# Format code
black src tests
isort src tests

# Auto-fix PEP8 issues (including line length)
autopep8 --max-line-length=79 --aggressive --in-place src/**/*.py

# Lint with flake8
flake8 src tests

# Type checking
mypy src

# Security check
bandit -r src
```

## 🏗️ Building and Distribution

### Building the Package

```bash
# Clean previous builds and create distributions
make build

# Create only wheel distribution
make wheel

# Create only source distribution
make sdist

# Validate build configuration
make validate-build
```

### Publishing to PyPI

```bash
# Upload to Test PyPI (for testing)
make upload-test

# Upload to production PyPI (requires proper credentials)
make upload

# Complete release validation
make release-check
```

### Installation Dependencies

Install build dependencies:

```bash
make install-build-deps
```

## 📁 Project Structure

```bash
serverwatch/
├── src/
│   └── serverwatch_analyzer/
│       ├── **init**.py
│       ├── analyzer.py
│       └── report_generator.py
├── tests/
│   ├── conftest.py
│   ├── test_analyzer.py
│   ├── test_init.py
│   └── test_report_generator.py
├── .github/
│   └── workflows/
│       ├── python.yml
│       ├── integration.yml
│       ├── release.yml
│       └── tag.yml
├── Makefile
├── pyproject.toml
├── requirements.txt
├── README.md
└── LICENSE
```

## 🚀 Quick Development Workflow

```bash
# 1. Clone and setup
git clone https://github.com/jfheinrich-eu/serverwatch.git
cd serverwatch

# 2. Setup development environment
make dev-setup

# 3. Make your changes...

# 4. Run quality checks
make check

# 5. Build and validate
make package-check

# 6. If everything passes, build for release
make build
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Setup development environment: `make dev-setup`
4. Make your changes
5. Run quality checks: `make check`
6. Validate package: `make package-check`
7. Commit your changes: `git commit -am 'Add amazing feature'`
8. Push to the branch: `git push origin feature/amazing-feature`
9. Open a Pull Request

### Code Style

This project follows PEP 8 and uses:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking
- **bandit** for security analysis

## 📊 Examples

Check out the [examples](examples/) directory for more usage examples:

- [Basic Analysis](examples/basic_analysis.py)
- [Batch Processing](examples/batch_processing.py)
- [Custom Report Generation](examples/custom_reports.py)

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes to this project.

## 🛡️ Security

If you discover a security vulnerability, please send an email to [admin@example.com](mailto:admin@example.com). All security vulnerabilities will be promptly addressed.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the language models
- The Python community for excellent tooling and libraries
- Contributors who help improve this project

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/jfheinrich-eu/serverwatch/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jfheinrich-eu/serverwatch/discussions)
- **Email**: [admin@example.com](mailto:admin@example.com)

---

Made with ❤️ by the ServerWatch Team
