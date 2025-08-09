#!/bin/bash

ENV_FILE="/root/.env.serverwatch"

echo "🛡️  ServerWatch Setup – Creating configuration..."

# Check if the file already exists
if [ -f "$ENV_FILE" ]; then
  echo "⚠️  Configuration file $ENV_FILE already exists."
  read -r -p "Do you want to overwrite it? [y/N]: " confirm
  if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
  fi
fi

# Query OpenAI API Key
read -r -p "🔑 OpenAI API Key (starts with 'sk-'): " OPENAI_API_KEY
if [[ ! "$OPENAI_API_KEY" =~ ^sk- ]]; then
  echo "❌ Invalid OpenAI API Key."
  exit 1
fi

# Query email address
read -r -p "📧 Recipient email for reports (e.g. admin@example.com): " ALERT_RECIPIENT
if [[ ! "$ALERT_RECIPIENT" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
  echo "❌ Invalid email address."
  exit 1
fi

# Write configuration file
cat <<EOF | sudo tee "$ENV_FILE" > /dev/null
# ServerWatch Configuration File
OPENAI_API_KEY=$OPENAI_API_KEY
ALERT_RECIPIENT=$ALERT_RECIPIENT
EOF

# Set permissions
sudo chmod 600 "$ENV_FILE"

echo "✅ Configuration saved in $ENV_FILE"
