# ServerAnalyzer Prompt Customization Guide

## Overview

The `ServerAnalyzer` class now supports customizable prompt templates and system messages, allowing users to tailor the AI analysis to their specific needs.

## Features

### 1. Configurable Analysis Prompt

The analysis prompt can be customized during initialization or at runtime:

```python
from serverwatch_analyzer.analyzer import ServerAnalyzer

# Custom prompt during initialization
custom_prompt = """
As a cybersecurity specialist, analyze this server report for:
1. Critical security vulnerabilities
2. Configuration weaknesses
3. Performance issues

Report: {report_content}
"""

analyzer = ServerAnalyzer(
    api_key="your-api-key",  # pragma: allowlist secret
    analysis_prompt=custom_prompt
)

# Or change it at runtime
analyzer.set_analysis_prompt(custom_prompt)
```

### 2. Configurable System Message

The system message that defines the AI's role can also be customized:

```python
# Custom system message during initialization
custom_system = "You are a senior DevOps engineer specializing in cloud security and infrastructure monitoring."

analyzer = ServerAnalyzer(
    api_key="your-api-key",   # pragma: allowlist secret
    system_message=custom_system
)

# Or change it at runtime
analyzer.set_system_message(custom_system)
```

### 3. Prompt Template Requirements

**Important:** Custom analysis prompts must contain the `{report_content}` placeholder:

```python
# ✅ Valid prompt
valid_prompt = "Analyze this report: {report_content}"

# ❌ Invalid prompt - will raise ValueError
invalid_prompt = "Analyze this report"  # Missing {report_content}
```

## API Reference

### Constructor Parameters

```python
ServerAnalyzer(
    api_key: Optional[str] = None,
    model: str = "gpt-4.1-nano",
    analysis_prompt: Optional[str] = None,
    system_message: Optional[str] = None
)
```

- `analysis_prompt`: Custom analysis prompt template (must contain `{report_content}`)
- `system_message`: Custom system message for the AI assistant

### Runtime Methods

```python
# Prompt management
analyzer.get_analysis_prompt() -> str
analyzer.set_analysis_prompt(prompt: str) -> None

# System message management
analyzer.get_system_message() -> str
analyzer.set_system_message(message: str) -> None

# Get defaults
ServerAnalyzer.get_default_analysis_prompt() -> str
ServerAnalyzer.get_default_system_message() -> str
```

## Use Cases

### 1. Specialized Security Analysis

```python
security_prompt = """
Perform a comprehensive security audit of this server report:

PRIORITY AREAS:
1. Authentication and authorization issues
2. Network security misconfigurations
3. Outdated software with known vulnerabilities
4. Privilege escalation risks
5. Data exposure concerns

SERVER REPORT:
{report_content}

Provide:
- Risk severity ratings (Critical/High/Medium/Low)
- Immediate action items
- Long-term recommendations
"""

analyzer = ServerAnalyzer(
    api_key="your-key",  # pragma: allowlist secret
    analysis_prompt=security_prompt,
    system_message="You are a certified security auditor with 10+ years experience in Linux server hardening."
)
```

### 2. Performance Focused Analysis

```python
performance_prompt = """
Analyze this server report focusing on performance optimization:

{report_content}

Focus on:
- CPU and memory utilization patterns
- Disk I/O bottlenecks
- Network performance issues
- Service optimization opportunities
"""

analyzer = ServerAnalyzer(
    api_key="your-key",  # pragma: allowlist secret
    analysis_prompt=performance_prompt,
    system_message="You are a performance tuning specialist for high-traffic web applications."
)
```

### 3. Compliance Auditing

```python
compliance_prompt = """
Review this server configuration for compliance violations:

Standards: SOC 2, PCI DSS, GDPR technical requirements
Server Report: {report_content}

Identify:
- Non-compliant configurations
- Missing security controls
- Documentation gaps
- Remediation steps
"""

analyzer = ServerAnalyzer(
    api_key="your-key", # pragma: allowlist secret
    analysis_prompt=compliance_prompt,
    system_message="You are a compliance officer specializing in IT security standards and regulations."
)
```

## Error Handling

```python
try:
    # This will raise ValueError
    analyzer.set_analysis_prompt("Invalid prompt without placeholder")
except ValueError as e:
    print(f"Error: {e}")
    # Error: Analysis prompt must contain {report_content} placeholder
```

## Best Practices

### 1. Template Validation

Always ensure your custom prompts contain the required placeholder:

```python
def validate_prompt(prompt: str) -> bool:
    return "{report_content}" in prompt

if validate_prompt(my_custom_prompt):
    analyzer.set_analysis_prompt(my_custom_prompt)
```

### 2. Prompt Versioning

For production systems, consider versioning your prompts:

```python
PROMPTS = {
    "v1.0": "Basic analysis prompt...",
    "v1.1": "Enhanced analysis prompt...",
    "v2.0": "Completely revised prompt..."
}

analyzer.set_analysis_prompt(PROMPTS["v2.0"])
```

### 3. Environment-Specific Configurations

```python
import os

# Different prompts for different environments
if os.getenv("ENVIRONMENT") == "production":
    prompt = PRODUCTION_SECURITY_PROMPT
elif os.getenv("ENVIRONMENT") == "staging":
    prompt = STAGING_TESTING_PROMPT
else:
    prompt = DEVELOPMENT_PROMPT

analyzer = ServerAnalyzer(
    api_key=os.getenv("OPENAI_API_KEY"),
    analysis_prompt=prompt
)
```

## Migration from Hardcoded Prompts

If you're upgrading from a version with hardcoded prompts:

```python
# Old way (hardcoded)
# prompt = f"Analyze this: {report_content}"

# New way (configurable)
analyzer = ServerAnalyzer(api_key="your-key")
# Uses default prompt, or customize as needed
result = analyzer.analyze_report(report_content)
```

The default prompt maintains backward compatibility with the original behavior.
