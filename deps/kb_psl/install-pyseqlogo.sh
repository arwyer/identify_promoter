#!/bin/bash

pip install pyBigWig
pip install --upgrade numpy
#mkdir /tmp/python-eggs
#export PYTHON_EGG_CACHE = /tmp/python-eggs
#sudo easy_install six=1.10
#sudo easy_install matplotlib
pip install --upgrade six
pip install matplotlib
pip install pandas
git clone https://github.com/saketkc/pyseqlogo.git
cd pyseqlogo
python setup.py build
python setup.py install
cd ..
