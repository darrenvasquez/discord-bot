#/bin/bash

for session in $(screen -ls | grep -o '[0-9]*\.discord-bot'); do screen -S "${session}" -X quit; done

screen -dmS discord-bot

screen -S discord-bot -X stuff "
cd ~/discord-bot/

echo '[Script] Pulling changes from Git...'
git pull
echo '[Script] Starting Discord Bot...'
python3 discord_bot.py

"