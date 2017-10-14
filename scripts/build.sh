
# Run from git root directory

pyinstaller -F --workpath="../build" -n "ytmp3" ytmp3.py
rm -rf __pycache__
