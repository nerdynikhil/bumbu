@echo off
pip install pyinstaller
pyinstaller --onefile --noconsole --name Bumbu bumbu.py
echo Built dist\Bumbu.exe
