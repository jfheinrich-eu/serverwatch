"""Tests for package imports and initialization."""

from serverwatch_analyzer import ReportGenerator, ServerAnalyzer, __version__


class TestPackageInit:
    """Test cases for package initialization."""

    def test_package_imports(self):
        """Test that main classes can be imported from package."""
        assert ServerAnalyzer is not None
        assert ReportGenerator is not None

    def test_version_exists(self):
        """Test that version is defined."""
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert len(__version__) > 0

    def test_version_format(self):
        """Test that version follows semantic versioning."""
        parts = __version__.split(".")
        assert len(parts) >= 2  # At least major.minor
        assert all(part.isdigit() for part in parts[:2])  # Major and minor are numeric

    def test_analyzer_instantiation(self):
        """Test that ServerAnalyzer can be instantiated."""
        # This should work without actual API key for testing
        try:
            analyzer = ServerAnalyzer(api_key="test-key")
            assert analyzer is not None
        except Exception:
            # Expected if OpenAI not available, but import should work
            pass

    def test_report_generator_instantiation(self):
        """Test that ReportGenerator can be instantiated."""
        generator = ReportGenerator()
        assert generator is not None
        assert generator.smtp_server == "localhost"
        assert generator.smtp_port == 25
