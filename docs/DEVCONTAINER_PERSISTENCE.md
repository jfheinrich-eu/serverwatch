# DevContainer Persistence Strategy

## 🔄 Automatischer Rebuild bei Container-Neustart

Ihr Setup wird **automatisch bei jedem DevContainer-Rebuild** wiederhergestellt!

## 🛠️ Was passiert beim Container-Rebuild?

### 1. PostCreateCommand (.devcontainer/postCreateCommands.sh)

```bash
# Läuft einmalig nach Container-Erstellung
1. System-Packages installieren (python3-venv, python3-pip)
2. Virtual Environment erstellen (.venv/)
3. Dependencies installieren (aus requirements-dev.lock)
4. Pre-commit Hooks installieren
5. Permissions setzen
```

### 2. PostAttachCommand (.devcontainer/postAttachCommands.sh)

```bash
# Läuft bei jedem Attach/Reconnect
1. PyEnv setup (falls gewünscht)
2. Virtual Environment Status prüfen
3. Hilfreiche Befehle anzeigen
```

### 3. VSCode Settings

```json
// Automatisch in devcontainer.json integriert:
- Python Interpreter: ./.venv/bin/python
- Linting: pylint, flake8, mypy, bandit
- Formatierung: black, isort
- Testing: pytest
- Auto-Format on Save
```

## 📋 Lock File Strategy

### Exakte Reproduzierbarkeit

```bash
# requirements-dev.lock enthält exakte Versionen:
annotated-types==0.7.0
anyio==4.10.0
astroid==3.3.11
bandit==1.8.6
# ... (58 packages total)
```

### Update Workflow

```bash
# Dependencies aktualisieren:
./update-dev-env.sh

# Oder manuell:
source .venv/bin/activate
pip install -e ".[dev]"
pip freeze > requirements-dev.lock
git add requirements-dev.lock
git commit -m "chore: update dev dependencies"
```

## 🚀 Automatisierung im Detail

### Container Build Flow

```text
1. DevContainer startet
   ↓
2. postCreateCommands.sh ausführen
   ↓
3. .venv/ erstellen
   ↓
4. requirements-dev.lock installieren
   ↓
5. VSCode Settings aktivieren
   ↓
6. ✅ Entwicklungsumgebung bereit!
```

### Rebuild-sichere Dateien

- ✅ `pyproject.toml` - Project configuration
- ✅ `requirements-dev.lock` - Exact dependency versions
- ✅ `.devcontainer/devcontainer.json` - Container configuration
- ✅ `.devcontainer/postCreateCommands.sh` - Setup script
- ✅ `.vscode/settings.json` - VSCode configuration (auch im devcontainer.json)
- ✅ `activate-dev.sh` - Activation script
- ✅ `update-dev-env.sh` - Update script

### Was wird neu erstellt

- 🔄 `.venv/` - Virtual environment (aber identisch reproduziert)
- 🔄 Installierte packages (aber exakte Versionen aus Lock-Datei)

## 🎯 Testing der Persistierung

### Rebuild testen

```bash
# 1. Aktuellen Zustand dokumentieren
source .venv/bin/activate
python -c "import sys; print(f'Python: {sys.version}')"
pip list

# 2. Container rebuild
Cmd+Shift+P → "Dev Containers: Rebuild Container"

# 3. Nach Rebuild prüfen
source .venv/bin/activate  # Sollte sofort funktionieren
python -c "import serverwatch_analyzer; print('✅ Package available')"
make test  # Sollte alle Tests ausführen
```

## 🔧 Manual Recovery

Falls etwas schiefgeht:

```bash
# Virtual Environment neu erstellen
rm -rf .venv
make dev-setup

# Oder vollständig:
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.lock
pre-commit install
```

## 🌟 Vorteile dieser Strategie

✅ **Automatisch:** Kein manueller Setup nach Rebuild
✅ **Reproduzierbar:** Exakte Versionen via Lock-Datei
✅ **Schnell:** Cached dependencies, nur bei Änderungen neu installieren
✅ **Konsistent:** Gleiche Umgebung für alle Entwickler
✅ **Versioniert:** Lock-Datei im Git Repository
✅ **VSCode Integration:** Settings automatisch angewendet

## 📈 Best Practices

### 1. Lock-Datei aktuell halten

```bash
# Nach Dependency-Änderungen:
./update-dev-env.sh
git add requirements-dev.lock
git commit -m "chore: update dependencies"
```

### 2. Rebuild bei großen Änderungen

```bash
# Nach größeren pyproject.toml Änderungen:
Cmd+Shift+P → "Dev Containers: Rebuild Container"
```

### 3. Environment validieren

```bash
# Nach Rebuild prüfen:
source .venv/bin/activate
make test
make lint
```

## 🚨 Troubleshooting

### Problem: Virtual Environment fehlt nach Rebuild

```bash
# Lösung: Setup erneut ausführen
make dev-setup
```

### Problem: Dependencies veraltet

```bash
# Lösung: Lock-Datei aktualisieren
./update-dev-env.sh
```

### Problem: VSCode erkennt Python nicht

```bash
# Lösung: Interpreter neu auswählen
Cmd+Shift+P → "Python: Select Interpreter" → ./.venv/bin/python
```

## ✅ Status: Vollständig automatisiert

Ihr Setup übersteht jeden Container-Rebuild und wird identisch wiederhergestellt! 🎉
