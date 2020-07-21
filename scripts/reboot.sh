#/bin/bash

screen -dmS discord-bot bash -c "
cd ~/discord-bot/

echo '[Script] Pulling changes from Git...'
git pull
echo '[Script] Starting Discord Bot...'
python3 discord-bot.py

"