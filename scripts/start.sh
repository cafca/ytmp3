export LC_ALL=de_DE.utf-8
export LANG=de_DE.utf-8

cd /Users/vaul/Projects/ytmp3/src
source /Users/vaul/.bash_profile
source ../bin/activate
export PATH=$PATH:/usr/local/bin
python ytmp3.py --loop
deactivate
