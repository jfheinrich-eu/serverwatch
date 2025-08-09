# VSCode Python Virtual Environment Setup Guide

## 🐍 Automatische Virtuelle Umgebung für VSCode

Dieses Projekt ist konfiguriert, um automatisch eine isolierte Python-Umgebung zu verwenden, in der alle Dependencies installiert und von VSCode korrekt erkannt werden.

## 🚀 Schnellstart

### Option 1: Automatisches Setup Script

```bash
# Aktiviert automatisch die virtuelle Umgebung
./activate-dev.sh
```

### Option 2: Makefile (empfohlen)

```bash
# Komplettes Development Setup
make dev-setup
```

### Option 3: Manuell

```bash
# Virtuelle Umgebung erstellen
python3 -m venv .venv

# Aktivieren
source .venv/bin/activate

# Dependencies installieren
pip install -e ".[dev]"
```

## ⚙️ VSCode Konfiguration

### Automatische Interpreter-Erkennung

Die `.vscode/settings.json` ist konfiguriert für:

```json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true
}
```

### Features aktiviert

✅ **Linting:** pylint, flake8, mypy, bandit
✅ **Formatierung:** black (79 Zeichen), isort
✅ **Testing:** pytest mit automatischer Erkennung
✅ **Type Checking:** mypy mit basic mode
✅ **Auto Import:** Intelligente Vervollständigung
✅ **Format on Save:** Automatische Formatierung beim Speichern

## 🔍 Debugging Konfiguration

Die `.vscode/launch.json` enthält vorgefertigte Debug-Konfigurationen:

### Verfügbare Debug-Modi

- **Python: Current File** - Debug der aktuellen Datei
- **Python: Run Tests** - Debug von Tests
- **Python: Run Specific Test** - Debug eines spezifischen Tests
- **Python: Analyzer Demo** - Debug des Analyzers mit API-Key

## 📦 Dependency Management

### Installierte Packages

**Runtime Dependencies:**

- `openai>=1.99.3` - OpenAI API Client
- `markdown>=3.8.2` - Markdown processing

**Development Dependencies:**

- `pytest>=8.4.1` - Testing framework
- `pytest-cov>=6.2.1` - Coverage reporting
- `pytest-mock>=3.14.1` - Mocking utilities
- `pylint>=3.3.7` - Python linter
- `black>=25.1.0` - Code formatter
- `isort>=6.0.1` - Import sorter
- `flake8>=7.3.0` - Style guide enforcement
- `mypy>=1.17.1` - Static type checker
- `bandit>=1.8.6` - Security linter
- `pre-commit>=4.2.0` - Git hook framework

### Package Installation

```bash
# Editierbare Installation (für Entwicklung)
pip install -e ".[dev]"

# Nur Runtime-Dependencies
pip install -e .

# Nur Development-Dependencies
pip install pytest black isort flake8 mypy pylint bandit
```

## 🧪 Testing Integration

### VSCode Test Discovery

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests", "-v", "--tb=short"],
    "python.testing.autoTestDiscoverOnSaveEnabled": true
}
```

### Test Commands

```bash
# Im Terminal (mit aktivierter venv)
pytest tests/ -v

# Über VSCode Test Explorer
# - Automatische Erkennung aller Tests
# - Run/Debug einzelner Tests
# - Coverage Integration
```

## 🔧 Development Workflow

### 1. Environment aktivieren

```bash
source .venv/bin/activate
# oder
./activate-dev.sh
```

### 2. Code schreiben

- VSCode erkennt automatisch die virtuelle Umgebung
- IntelliSense funktioniert mit allen installierten Packages
- Auto-Import schlägt verfügbare Module vor

### 3. Code formatieren

```bash
# Automatisch bei Save in VSCode
# oder manuell:
make format
make pre-commit-fix
```

### 4. Tests ausführen

```bash
# Über VSCode Test Explorer
# oder Terminal:
make test
pytest tests/ -v
```

### 5. Linting prüfen

```bash
make lint
make pre-commit-run
```

## 🔍 Troubleshooting

### Problem: VSCode erkennt virtuelle Umgebung nicht

**Lösung 1:** Python Interpreter manuell auswählen

1. `Ctrl+Shift+P` → "Python: Select Interpreter"
2. Wähle `./.venv/bin/python`

**Lösung 2:** VSCode Settings überprüfen

```bash
# Prüfe .vscode/settings.json
cat .vscode/settings.json | grep defaultInterpreterPath
```

**Lösung 3:** Reload VSCode Window

1. `Ctrl+Shift+P` → "Developer: Reload Window"

### Problem: Module nicht gefunden

**Lösung:** Editable Installation prüfen

```bash
source .venv/bin/activate
pip list | grep serverwatch-analyzer
# Sollte zeigen: serverwatch-analyzer 0.1.0 /workspaces/serverwatch
```

**Neuinstallation falls nötig:**

```bash
pip install -e ".[dev]"
```

### Problem: Linting Fehler in VSCode

**Lösung:** Linter-Pfade prüfen

```bash
source .venv/bin/activate
which pylint  # Sollte .venv/bin/pylint sein
which black   # Sollte .venv/bin/black sein
which mypy    # Sollte .venv/bin/mypy sein
```

### Problem: Tests nicht erkannt

**Lösung 1:** Test Discovery neu ausführen

1. `Ctrl+Shift+P` → "Python: Refresh Tests"

**Lösung 2:** pytest-Konfiguration prüfen

```bash
# pyproject.toml sollte enthalten:
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

## 📁 File Structure

```text
serverwatch/
├── .venv/                     # Virtuelle Umgebung
│   ├── bin/python            # Python Interpreter
│   ├── lib/python3.12/       # Installierte Packages
│   └── pyvenv.cfg            # venv Konfiguration
├── .vscode/
│   ├── settings.json         # VSCode Python Einstellungen
│   └── launch.json           # Debug-Konfigurationen
├── src/serverwatch_analyzer/ # Source Code
├── tests/                    # Test Files
├── activate-dev.sh           # Development Environment Script
└── pyproject.toml           # Project Configuration
```

## ✅ Erfolgsstatus prüfen

```bash
# Alle Checks ausführen
source .venv/bin/activate

# 1. Python Version
python --version

# 2. Virtual Environment aktiv?
echo $VIRTUAL_ENV  # Sollte /workspaces/serverwatch/.venv sein

# 3. Package importierbar?
python -c "import serverwatch_analyzer; print('✅ OK')"

# 4. Dependencies verfügbar?
python -c "import openai, pytest, black; print('✅ Dependencies OK')"

# 5. VSCode Integration?
code --list-extensions | grep python  # ms-python.python sollte da sein
```

## 🎯 Best Practices

### 1. Immer virtuelle Umgebung verwenden

```bash
# Vor jeder Entwicklungsession:
source .venv/bin/activate
```

### 2. Dependencies in pyproject.toml verwalten

```toml
# Neue Runtime-Dependency hinzufügen:
dependencies = ["openai>=1.99.3", "new-package>=1.0.0"]

# Neue Dev-Dependency hinzufügen:
[project.optional-dependencies]
dev = ["pytest>=8.4.1", "new-dev-tool>=1.0.0"]
```

### 3. Pre-commit Hooks nutzen

```bash
# Einmalig installieren:
pre-commit install

# Vor jedem Commit laufen automatisch:
# - black (Code-Formatierung)
# - isort (Import-Sortierung)
# - flake8 (Linting)
# - mypy (Type-Checking)
# - bandit (Security-Check)
```

### 4. Tests regelmäßig ausführen

```bash
# Während der Entwicklung:
pytest tests/ --tb=short  # Schneller Überblick

# Vor Commits:
make test  # Vollständige Tests mit Coverage
```

## 🚀 Ready for Development

Mit dieser Konfiguration haben Sie eine vollständig isolierte, reproduzierbare Python-Entwicklungsumgebung, die nahtlos mit VSCode integriert ist. Alle Dependencies sind korrekt installiert und VSCode erkennt sie automatisch für IntelliSense, Debugging und Testing.
