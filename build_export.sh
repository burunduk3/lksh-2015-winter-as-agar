pushd dist
for f in `ls` ; do
  echo compress $f
  7z a $f $f || exit
done
scp -P 22 -i C:/WorkGit/Keys/id_rsa *.7z ejudge@192.168.2.254:/var/www/vhosts/sis/AS/agario/
popd 
