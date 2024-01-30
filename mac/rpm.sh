#!/bin/bash

SCRIPT_ROOT=`pwd`
BUILD_ROOT=$SCRIPT_ROOT/GSharpKitBuild

NAME=GSharpKit
PREFIX=/Library/$NAME
SYMLINK=/Library/$NAME

RPM_VERSION=4.11.2

sudo mkdir -p $PREFIX

cd $SCRIPT_ROOT
cp sources/rpm-${RPM_VERSION}.tar.bz2 $BUILD_ROOT/

cd $BUILD_ROOT
if [[ ! -f nspr-4.35.tar.gz ]]; then
curl -o nspr-4.35.tar.gz http://ftp.mozilla.org/pub/nspr/releases/v4.35/src/nspr-4.35.tar.gz
fi
if [[ ! -f nss-3.96.1.tar.gz  ]]; then
curl -o nss-3.96.1.tar.gz https://archive.mozilla.org/pub/security/nss/releases/NSS_3_96_1_RTM/src/nss-3.96.1.tar.gz
fi
if [[ ! -f file-5.16.tar.gz ]]; then
curl -o file-5.16.tar.gz ftp://ftp.astron.com/pub/file/file-5.16.tar.gz
fi
if [[ ! -f popt-1.19.tar.gz ]]; then
curl -o popt-1.19.tar.gz http://ftp.rpm.org/popt/releases/popt-1.x/popt-1.19.tar.gz
fi
if [[ ! -f db-4.5.20.tar.gz ]]; then
curl -o db-4.5.20.tar.gz https://ftpmirror.your.org/pub/misc/Berkeley-DB/db-4.5.20.tar.gz
fi

#if [[ ! -f rpm-${RPM_VERSION}.tar.bz2 ]]; then
#curl -o rpm-${RPM_VERSION}.tar.bz2 http://ftp.rpm.org/releases/rpm-4.19.x/rpm-${RPM_VERSION}.tar.bz2
#fi

if [[ -d nspr-4.35 ]]; then
	rm -rf nspr-4.35
fi

if [[ -d nss-3.96.1  ]]; then
        rm -rf nss-3.96.1
fi

if [[ -d file-5.16 ]]; then
        rm -rf file-5.16
fi

if [[ -d popt-1.19 ]]; then
        rm -rf popt-1.19
fi

if [[ -d db-4.5.20 ]]; then
        rm -rf db-4.5.20
fi
if [[ -d rpm-${RPM_VERSION} ]]; then
        rm -rf rpm-${RPM_VERSION}
fi

tar xfz nspr-4.35.tar.gz
tar xfz nss-3.96.1.tar.gz
tar xfz file-5.16.tar.gz 
tar xfz popt-1.19.tar.gz
tar xfz db-4.5.20.tar.gz
tar xfj rpm-${RPM_VERSION}.tar.bz2

cd $BUILD_ROOT/nspr-4.35/nspr
./configure --target=aarch64-apple-darwin23.2.0 --prefix=$PREFIX --exec-prefix=$PREFIX
make
sudo make install


cd $BUILD_ROOT/nss-3.96.1
patch -p1 < $SCRIPT_ROOT/sources/nss-crypto.patch
cd $BUILD_ROOT/nss-3.96.1/nss
make BUILD_OPT=1 NSPR_INCLUDE_DIR=$PREFIX/include/nspr NSPR_LIB_DIR=$PREFIX/lib USE_SYSTEM_ZLIB=1 ZLIB_LIBS=-lz USE_64=1
cd ../dist
sudo install -v -m755 Darwin*/lib/*.dylib           $PREFIX/lib
sudo install -v -m644 Darwin*/lib/{*.chk,libcrmf.a} $PREFIX/lib
sudo install -v -m755 -d                            $PREFIX/include/nss
sudo cp -v -RL {public,private}/nss/*               $PREFIX/include/nss
sudo chmod -v 644                                   $PREFIX/include/nss/*
sudo install -v -m755 Darwin*/bin/{certutil,nss-config,pk12util} $PREFIX/bin
sudo install -v -m644 Darwin*/lib/pkgconfig/nss.pc  $PREFIX/lib/pkgconfig

cd $BUILD_ROOT/file-5.16
./configure --target=aarch64-apple-darwin23.2.0 --prefix=$PREFIX --exec-prefix=$PREFIX
make
sudo make install

cd $BUILD_ROOT/popt-1.19
./configure --target=aarch64-apple-darwin23.2.0 --prefix=$PREFIX --exec-prefix=$PREFIX
make
sudo make install

cd $BUILD_ROOT/db-4.5.20/build_unix
../dist/configure --target=aarch64-apple-darwin23.2.0 --prefix=$PREFIX --exec-prefix=$PREFIX --disable-replication
make
sudo make install

cd $BUILD_ROOT/rpm-${RPM_VERSION}
#patch -p1 < $SCRIPT_ROOT/rpm-4.11.2-mac.patch
PATH=$PREFIX/bin:$PATH CPPFLAGS="-I$PREFIX/include -I$PREFIX/include/nspr -I$PREFIX/include/nss" LDFLAGS="-L$PREFIX/lib" ./configure --target=aarch64-apple-darwin23.2.0 --prefix=$PREFIX --exec-prefix=$PREFIX --with-external-db --without-lua --disable-optimized --disable-aio --with-glob --enable-broken-chown --disable-rpath
make
sudo make install
sudo install_name_tool -change @executable_path/libssl3.dylib $PREFIX/lib/libssl3.dylib $PREFIX/lib/libssl3.dylib
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/lib/libssl3.dylib
sudo install_name_tool -change @executable_path/libnssutil3.dylib $PREFIX/lib/libnssutil3.dylib $PREFIX/lib/libssl3.dylib
sudo install_name_tool -change @executable_path/libplc4.dylib $PREFIX/lib/libplc4.dylib $PREFIX/lib/libssl3.dylib
sudo install_name_tool -change @executable_path/libplds4.dylib $PREFIX/lib/libplds4.dylib $PREFIX/lib/libssl3.dylib
sudo install_name_tool -change @executable_path/libnspr4.dylib $PREFIX/lib/libnspr4.dylib $PREFIX/lib/libssl3.dylib

sudo install_name_tool -change @executable_path/libsqlite3.dylib $PREFIX/lib/libsqlite3.dylib $PREFIX/lib/libsqlite3.dylib

sudo install_name_tool -change @executable_path/libsoftokn3.dylib $PREFIX/lib/libsoftokn3.dylib $PREFIX/lib/libsoftokn3.dylib
sudo install_name_tool -change @executable_path/libsqlite3.dylib $PREFIX/lib/libsqlite3.dylib $PREFIX/lib/libsoftokn3.dylib
sudo install_name_tool -change @executable_path/libnssutil3.dylib $PREFIX/lib/libnssutil3.dylib $PREFIX/lib/libsoftokn3.dylib
sudo install_name_tool -change @executable_path/libplc4.dylib $PREFIX/lib/libplc4.dylib $PREFIX/lib/libsoftokn3.dylib
sudo install_name_tool -change @executable_path/libplds4.dylib $PREFIX/lib/libplds4.dylib $PREFIX/lib/libsoftokn3.dylib
sudo install_name_tool -change @executable_path/libnspr4.dylib $PREFIX/lib/libnspr4.dylib $PREFIX/lib/libsoftokn3.dylib

sudo install_name_tool -change @executable_path/libsmime3.dylib $PREFIX/lib/libsmime3.dylib $PREFIX/lib/libsmime3.dylib
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/lib/libsmime3.dylib
sudo install_name_tool -change @executable_path/libnssutil3.dylib $PREFIX/lib/libnssutil3.dylib $PREFIX/lib/libsmime3.dylib
sudo install_name_tool -change @executable_path/libplc4.dylib $PREFIX/lib/libplc4.dylib $PREFIX/lib/libsmime3.dylib
sudo install_name_tool -change @executable_path/libplds4.dylib $PREFIX/lib/libplds4.dylib $PREFIX/lib/libsmime3.dylib
sudo install_name_tool -change @executable_path/libnspr4.dylib $PREFIX/lib/libnspr4.dylib $PREFIX/lib/libsmime3.dylib

sudo install_name_tool -change @executable_path/libfreebl3.dylib $PREFIX/lib/libfreebl3.dylib $PREFIX/lib/libfreebl3.dylib
sudo install_name_tool -change @executable_path/libnssutil3.dylib $PREFIX/lib/libnssutil3.dylib $PREFIX/lib/libfreebl3.dylib
sudo install_name_tool -change @executable_path/libnspr4.dylib $PREFIX/lib/libnspr4.dylib $PREFIX/lib/libfreebl3.dylib
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/lib/libnss3.dylib
sudo install_name_tool -change @executable_path/libnssutil3.dylib $PREFIX/lib/libnssutil3.dylib $PREFIX/lib/libnss3.dylib
sudo install_name_tool -change @executable_path/libplc4.dylib $PREFIX/lib/libplc4.dylib $PREFIX/lib/libnss3.dylib
sudo install_name_tool -change @executable_path/libplds4.dylib $PREFIX/lib/libplds4.dylib $PREFIX/lib/libnss3.dylib
sudo install_name_tool -change @executable_path/libnspr4.dylib $PREFIX/lib/libnspr4.dylib $PREFIX/lib/libnss3.dylib
sudo install_name_tool -change @executable_path/libnssckbi.dylib $PREFIX/lib/libnssckbi.dylib $PREFIX/lib/libnssckbi.dylib
sudo install_name_tool -change @executable_path/libplc4.dylib $PREFIX/lib/libplc4.dylib $PREFIX/lib/libnssckbi.dylib
sudo install_name_tool -change @executable_path/libplds4.dylib $PREFIX/lib/libplds4.dylib $PREFIX/lib/libnssckbi.dylib
sudo install_name_tool -change @executable_path/libnspr4.dylib $PREFIX/lib/libnspr4.dylib $PREFIX/lib/libnssckbi.dylib
sudo install_name_tool -change @executable_path/libnssdbm3.dylib $PREFIX/lib/libnssdbm3.dylib $PREFIX/lib/libnssdbm3.dylib
sudo install_name_tool -change @executable_path/libnssutil3.dylib $PREFIX/lib/libnssutil3.dylib $PREFIX/lib/libnssdbm3.dylib
sudo install_name_tool -change @executable_path/libplc4.dylib $PREFIX/lib/libplc4.dylib $PREFIX/lib/libnssdbm3.dylib
sudo install_name_tool -change @executable_path/libplds4.dylib $PREFIX/lib/libplds4.dylib $PREFIX/lib/libnssdbm3.dylib
sudo install_name_tool -change @executable_path/libnspr4.dylib $PREFIX/lib/libnspr4.dylib $PREFIX/lib/libnssdbm3.dylib
sudo install_name_tool -change @executable_path/libnssutil3.dylib $PREFIX/lib/libnssutil3.dylib $PREFIX/lib/libnssutil3.dylib
sudo install_name_tool -change @executable_path/libplc4.dylib $PREFIX/lib/libplc4.dylib $PREFIX/lib/libnssutil3.dylib
sudo install_name_tool -change @executable_path/libplds4.dylib $PREFIX/lib/libplds4.dylib $PREFIX/lib/libnssutil3.dylib
sudo install_name_tool -change @executable_path/libnspr4.dylib $PREFIX/lib/libnspr4.dylib $PREFIX/lib/libnssutil3.dylib
sudo install_name_tool -change @executable_path/libplc4.dylib $PREFIX/lib/libplc4.dylib $PREFIX/lib/libplc4.dylib
sudo install_name_tool -change @executable_path/libnspr4.dylib $PREFIX/lib/libnspr4.dylib $PREFIX/lib/libplc4.dylib
sudo install_name_tool -change @executable_path/libplds4.dylib $PREFIX/lib/libplds4.dylib $PREFIX/lib/libplds4.dylib
sudo install_name_tool -change @executable_path/libnspr4.dylib $PREFIX/lib/libnspr4.dylib $PREFIX/lib/libplds4.dylib
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/bin/rpm
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/bin/rpm2cpio
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/bin/rpmbuild
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/bin/rpmdb
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/bin/rpmgraph
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/bin/rpmkeys
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/bin/rpmsign
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/bin/rpmspec 
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/lib/librpm.3.dylib
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/lib/librpmbuild.3.dylib
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/lib/librpmio.3.dylib
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/lib/librpmsign.1.dylib

sudo install_name_tool -change @executable_path/libssl3.dylib $PREFIX/lib/libssl3.dylib $PREFIX/bin/certutil
sudo install_name_tool -change @executable_path/libsmime3.dylib $PREFIX/lib/libsmime3.dylib $PREFIX/bin/certutil
sudo install_name_tool -change @executable_path/libnss3.dylib $PREFIX/lib/libnss3.dylib $PREFIX/bin/certutil
sudo install_name_tool -change @executable_path/libnssutil3.dylib $PREFIX/lib/libnssutil3.dylib $PREFIX/bin/certutil
sudo install_name_tool -change @executable_path/libplc4.dylib $PREFIX/lib/libplc4.dylib $PREFIX/bin/certutil
sudo install_name_tool -change @executable_path/libplds4.dylib $PREFIX/lib/libplds4.dylib $PREFIX/bin/certutil
sudo install_name_tool -change @executable_path/libnspr4.dylib $PREFIX/lib/libnspr4.dylib $PREFIX/bin/certutil

sudo mkdir -p $PREFIX/var/lib/rpm
sudo mkdir -p $PREFIX/etc/rpm
sudo cp $SCRIPT_ROOT/../rpm/SOURCES/macros.darwinx $PREFIX/etc/rpm/
sudo cp $SCRIPT_ROOT/../rpm/SOURCES/macros.dist $PREFIX/etc/rpm/
#sudo cp $SCRIPT_ROOT/darwinx-find-lang.sh $PREFIX/lib/rpm/
#sudo cp $SCRIPT_ROOT/darwinx-find-provides.sh $PREFIX/lib/rpm/
#sudo cp $SCRIPT_ROOT/darwinx-find-requires.sh $PREFIX/lib/rpm/
sudo chmod 777 $PREFIX/var/tmp
sudo chmod 777 $PREFIX/var/lib
sudo chmod 777 $PREFIX/var/lib/rpm

sudo ln -sf $SYMLINK/bin/rpm /usr/local/bin/rpm
sudo ln -sf $SYMLINK/bin/rpm2cpio /usr/local/bin/rpm2cpio
sudo ln -sf $SYMLINK/bin/rpmbuild /usr/local/bin/rpmbuild
sudo ln -sf $SYMLINK/bin/rpmdb /usr/local/bin/rpmdb
sudo ln -sf $SYMLINK/bin/rpmgraph /usr/local/bin/rpmgraph
sudo ln -sf $SYMLINK/bin/rpmkeys /usr/local/bin/rpmkeys
sudo ln -sf $SYMLINK/bin/rpmsign /usr/local/bin/rpmsign
sudo ln -sf $SYMLINK/bin/rpmspec /usr/local/bin/rpmspec

rpm --initdb
