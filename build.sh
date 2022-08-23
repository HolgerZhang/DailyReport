#!/bin/bash

version="4.0.1-beta-FIX01"

pip install -r requirements.txt || exit

if [ -d dist/DailyReport/ ]; then
  rm -rf dist/DailyReport || exit
fi

pyinstaller main.py || exit
pyinstaller watcher.py || exit
mkdir -p dist/main/data/mail || exit
mkdir -p dist/main/configurations || exit
cp data/version.json dist/main/data/version.json || exit
cp data/mail/* dist/main/data/mail/ || exit
cp configurations/example.* dist/main/configurations/ || exit
cp configurations/introduction.* dist/main/configurations/ || exit
cd dist/main || exit
mv main DailyReport || exit
export _BOT_BUILD_NOT_DOWNLOAD=1
./DailyReport --initialize --config configurations/example.general.json || exit
rm BotLog.log EmailSender.log || exit

cd .. || exit
mv main DailyReport || exit
cp -rf watcher/* DailyReport/ || exit
mv DailyReport/watcher DailyReport/DailyReport.Watcher || exit
rm -rf watcher || exit
file_name="DailyReport.$version-`uname -s`-`uname -m`.zip"
zip -r $file_name DailyReport || exit
cd .. || exit
rm -rf ./build || exit
echo "dist/${file_name}生成完毕"