#!/bin/bash

curl -O http://meme-suite.org/meme-software/5.0.1/meme_5.0.1_1.tar.gz
tar zxf meme_5.0.1_1.tar.gz
cd meme-5.0.1
./configure --prefix=/kb/module/work/meme
make
make install
export PATH=/kb/module/work/meme/bin:$PATH
cd ..
