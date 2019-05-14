export LC_ALL=de_DE.utf-8
export LANG=de_DE.utf-8

cd /Users/pv/projects/ytmp3/src
source /Users/pv/.bash_profile
source ../venv/bin/activate
export PATH=$PATH:/usr/local/bin
python ytmp3.py
deactivate
