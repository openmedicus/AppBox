#!/bin/bash

SOURCEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TMPDIR=`mktemp -d -p "/tmp"`

cp createmsi.py $TMPDIR/
cp LICENSE $TMPDIR/License.rtf
cp GSharpSdk.json $TMPDIR/

# Install to staging
TMP="$TMPDIR/tmp"
DIR="$TMPDIR/framework/35"

mkdir -p $TMPDIR/tmp/usr/x86_64-w64-mingw32/sys-root/mingw

sh make-msi-install.sh /usr/x86_64-w64-mingw32/sys-root/mingw $TMP/usr/x86_64-w64-mingw32/sys-root/mingw x64

mkdir -p $TMPDIR/framework
mv $TMP/usr/x86_64-w64-mingw32/sys-root/mingw $DIR
sed -i -e 's!<\!--<auth>EXTERNAL</auth>-->!<auth>EXTERNAL</auth>!g' $DIR/share/dbus-1/session.conf

find $DIR -iname '*.dll' -exec echo {} \; -exec osslsigncode sign -pkcs12 ~/.pki/gsharpkit.p12 -pass xcare -n GSharpSdk -i http://www.gsharpkit.com -t http://timestamp.digicert.com -h sha2 -in '{}' -out '{}.signed' \; -exec mv -f '{}.signed' '{}' \;
find $DIR -iname '*.dll' -exec echo {} \; -exec osslsigncode sign -pkcs12 ~/.pki/gsharpkit.p12 -pass xcare -n GSharpSdk -i http://www.gsharpkit.com -t http://timestamp.digicert.com -nest -h sha512 -in '{}' -out '{}.signed' \; -exec mv -f '{}.signed' '{}' \;

find $DIR -iname '*.exe' -exec echo {} \; -exec osslsigncode sign -pkcs12 ~/.pki/gsharpkit.p12 -pass xcare -n GSharpSdk -i http://www.gsharpkit.com -t http://timestamp.digicert.com -h sha2 -in '{}' -out '{}.signed' \; -exec mv -f '{}.signed' '{}' \;
find $DIR -iname '*.exe' -exec echo {} \; -exec osslsigncode sign -pkcs12 ~/.pki/gsharpkit.p12 -pass xcare -n GSharpSdk -i http://www.gsharpkit.com -t http://timestamp.digicert.com -nest -h sha512 -in '{}' -out '{}.signed' \; -exec mv -f '{}.signed' '{}' \;

pushd $TMPDIR
python createmsi.py GSharpSdk.json
cp GSharpSdk-35.0.1-64.msi $SOURCEDIR/GSharpSdk-35.0-x64.msi
popd

