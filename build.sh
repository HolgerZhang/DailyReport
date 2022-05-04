#!/bin/bash

pip install pyinstaller

pyinstaller main.py
mkdir -p dist/main/data/mail
mkdir -p dist/main/configurations
cp data/version.json dist/main/data/version.json
cp data/mail/* dist/main/data/mail/
cp configurations/example.* dist/main/configurations/
cp configurations/introduction.* dist/main/configurations/
cd dist/main
mv main DailyReport
./DailyReport --initialize --config configurations/example.general.json

cd ..
mv main DailyReport
file_name='DailyReport.3910-2.5.4-alpha.zip'
zip -r $file_name DailyReport
cd ..
rm -rf ./build
echo "dist/${file_name}生成完毕"