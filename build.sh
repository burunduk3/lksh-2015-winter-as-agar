suf=`echo 'import time; print(time.strftime("%y%m%d_%H"))' | python`
client=dist/client_user/
client2=dist/client_opengl/
server=dist/server_main/

pyinstaller client_opengl.py || exit
cp config.txt $client2

pyinstaller client_user.py || exit
cp config.txt $client

pyinstaller server_main.py || exit
cp config.txt $server

mv $client2 dist/win-client2-$suf
mv $client dist/win-client-$suf
mv $server dist/win-server-$suf

path=dist/python-src-$suf
mkdir $path
cp -r *.py config.txt Client-bot $path/
