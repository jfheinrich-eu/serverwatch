# Pre-commit Auto-Formatting Configuration Guide

## 📝 Automatische Korrekturen aktiviert

Die `.pre-commit-config.yaml` wurde optimiert, um **automatische Korrekturen** durchzuführen:

### 🔧 Auto-Fix Tools

| Tool             | Was wird automatisch korrigiert      | Konfig-Flag               |
| ---------------- | ------------------------------------ | ------------------------- |
| **autopep8**     | Zeilenlänge, Einrückung, Leerzeichen | `--aggressive --in-place` |
| **black**        | Code-Formatierung, Stil              | `--line-length=79`        |
| **isort**        | Import-Sortierung                    | `--profile=black`         |
| **prettier**     | YAML/JSON Formatierung               | Auto-Format               |
| **markdownlint** | Markdown Formatierung                | `--fix`                   |

### 🚀 Execution Order (wichtig!)

```yaml
1. isort          # Sortiert Imports
2. black          # Formatiert Code
3. autopep8       # Behebt PEP8-Probleme (inkl. Zeilenlänge)
4. flake8         # Überprüft verbleibende Issues
5. mypy           # Type-Checking
```

## ⚡ Verwendung

### Automatische Korrektur vor Commit

```bash
# Alle Dateien automatisch korrigieren
make pre-commit-run

# Nur bestimmte Hooks ausführen
pre-commit run black --all-files
pre-commit run autopep8 --all-files
```

### Manuelle Korrekturen

```bash
# Nur Line-Length Probleme beheben
autopep8 --max-line-length=79 --aggressive --in-place src/**/*.py

# Black Formatierung
black --line-length=79 src/ tests/

# Import-Sortierung
isort --profile=black --line-length=79 src/ tests/
```

## 🎯 Spezielle Features

### autopep8 Configuration

```yaml
args: [--max-line-length=79, --aggressive, --aggressive, --in-place]
```

- `--max-line-length=79`: Bricht lange Zeilen um
- `--aggressive`: Macht aggressivere Korrekturen
- `--in-place`: Schreibt Änderungen direkt in Dateien

### Line Length Handling

```python
# Vorher (zu lang):
raise ValueError("Custom analysis_prompt must contain {report_content} placeholder")

# Nachher (automatisch korrigiert):
raise ValueError(
    "Custom analysis_prompt must contain "
    "{report_content} placeholder"
)
```

## 🔄 Pre-commit Hook Installation

Für automatische Ausführung bei jedem Commit:

```bash
# Pre-commit Hooks installieren
make dev-setup

# Oder manuell:
pre-commit install
```

Dann werden bei jedem `git commit` automatisch alle Korrekturen angewendet!

## 🛠️ Troubleshooting

### Häufige Probleme

**Problem:** Hook schlägt fehl mit "command not found"

```bash
# Lösung: Environment neu installieren
pre-commit clean
pre-commit install --install-hooks
```

**Problem:** Autopep8 und Black konfligieren

```bash
# Lösung: Reihenfolge ist wichtig - isort → black → autopep8
# Black läuft vor autopep8, sodass autopep8 nur PEP8-Fixes macht
```

**Problem:** Zu aggressive Änderungen

```bash
# Lösung: Weniger aggressive autopep8 Einstellungen
args: [--max-line-length=79, --in-place]  # Nur ein --aggressive
```

## 📊 Erfolgreiche Konfiguration

```bash
✅ trim trailing whitespace.....Passed
✅ fix end of files.............Passed
✅ check yaml..................Passed
✅ check toml..................Passed
✅ isort.......................Passed
✅ black.......................Passed
✅ autopep8....................Passed  # <- Automatische PEP8-Korrekturen!
✅ flake8......................Passed  # <- Keine Fehler mehr!
✅ mypy........................Passed
```

Die Konfiguration korrigiert jetzt **automatisch** die meisten Formatierungsprobleme! 🎉
