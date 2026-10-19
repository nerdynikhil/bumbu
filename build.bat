@echo off
pip install pyinstaller pillow
pyinstaller --onefile --noconsole --name Bumbu --add-data "sounds;sounds" --add-data "sprites;sprites" bumbu.py
echo Built dist\Bumbu.exe
