#!/bin/bash

mkdir -p homer
cd homer
wget http://homer.ucsd.edu/homer/configureHomer.pl
perl configureHomer.pl -install
cp ./bin/* /usr/local/bin
cd ..
