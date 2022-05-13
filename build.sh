#!/bin/bash

version="3980-2.5.13-alpha"

pip install pyinstaller

if [ -d dist/DailyReport/ ]; then
  rm -rf dist/DailyReport
fi

pyinstaller main.py
pyinstaller watcher.py
mkdir -p dist/main/data/mail
mkdir -p dist/main/configurations
cp data/version.json dist/main/data/version.json
cp data/mail/* dist/main/data/mail/
cp configurations/example.* dist/main/configurations/
cp configurations/introduction.* dist/main/configurations/
cd dist/main
mv main DailyReport
export _BOT_BUILD_NOT_DOWNLOAD=1
./DailyReport --initialize --config configurations/example.general.json

cd ..
mv main DailyReport
cp -rf watcher/* DailyReport/
mv DailyReport/watcher DailyReport/DailyReport.Watcher
rm -rf watcher
file_name="DailyReport.$version-`uname -s`-`uname -m`.zip"
zip -r $file_name DailyReport
cd ..
rm -rf ./build
echo "dist/${file_name}生成完毕"