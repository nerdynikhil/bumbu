@echo off
pip install pyinstaller
pyinstaller --onefile --noconsole --name Bumbu --add-data "sounds;sounds" bumbu.py
echo Built dist\Bumbu.exe
