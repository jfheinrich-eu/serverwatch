#!/bin/bash

ENV_FILE="/root/.env.serverwatch"

echo "🛡️  ServerWatch Setup – Konfiguration wird erstellt..."

# Prüfe, ob die Datei bereits existiert
if [ -f "$ENV_FILE" ]; then
  echo "⚠️  Konfigurationsdatei $ENV_FILE existiert bereits."
  read -p "Möchtest du sie überschreiben? [j/N]: " confirm
  if [[ ! "$confirm" =~ ^[Jj]$ ]]; then
    echo "Abgebrochen."
    exit 1
  fi
fi

# OpenAI API Key abfragen
read -p "🔑 OpenAI API Key (beginnt mit 'sk-'): " OPENAI_API_KEY
if [[ ! "$OPENAI_API_KEY" =~ ^sk- ]]; then
  echo "❌ Ungültiger OpenAI API Key."
  exit 1
fi

# E-Mail-Adresse abfragen
read -p "📧 Empfänger-E-Mail für Berichte (z. B. admin@example.com): " ALERT_RECIPIENT
if [[ ! "$ALERT_RECIPIENT" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
  echo "❌ Ungültige E-Mail-Adresse."
  exit 1
fi

# Konfigurationsdatei schreiben
cat <<EOF | sudo tee "$ENV_FILE" > /dev/null
# ServerWatch Konfigurationsdatei
OPENAI_API_KEY=$OPENAI_API_KEY
ALERT_RECIPIENT=$ALERT_RECIPIENT
EOF

# Berechtigungen setzen
sudo chmod 600 "$ENV_FILE"

echo "✅ Konfiguration gespeichert in $ENV_FILE"
