#!/bin/bash

set -e

echo "Install python dependencies..."
/opt/venv/bin/pip3 install openai markdown

echo "Install serverwatch daily cron job..."
cp src/serverwatch /etc/cron.daily/serverwatch && \
	chmod +x /etc/cron.daily/serverwatch && \
	chown root:root /etc/cron.daily/serverwatch

echo "Install /root/.env.serverwatch example file."
echo "Update the /root/.env.serverwatch with the real secrets."
cp src/.env.serverwatch.example /root/.env.serverwatch && \
	chmod 600 /root/.env.serverwatch


./setup-serverwatch.sh
