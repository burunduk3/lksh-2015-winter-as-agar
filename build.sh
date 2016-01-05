suf=`echo 'import time; print(time.strftime("%y%m%d_%H"))' | python`
client=dist/client_user/
server=dist/server_main/

pyinstaller client_user.py || exit
cp config.txt $client

pyinstaller server_main.py || exit
cp config.txt $server

mv $client dist/win-client-$suf
mv $server dist/win-server-$suf

path=dist/python-src-$suf
mkdir $path
cp -r *.py config.txt Client-bot $path/
