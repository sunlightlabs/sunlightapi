wget http://dl.maptools.org/dl/shapelib/shapelib-1.2.10.tar.gz
tar xvf shapelib-1.2.10.tar.gz
cd shapelib-1.2.10/
wget http://ftp.intevation.de/users/bh/pyshapelib/pyshapelib-0.3.tar.gz
tar xvf pyshapelib-0.3.tar.gz
cd pyshapelib-0.3/
python setup.py build install
