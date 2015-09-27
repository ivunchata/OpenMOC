#ccache gcc -DFP_PRECISION=float -DSINGLE -DGNU -DVEC_LENGTH=8 -DVEC_ALIGNMENT=16 -I/usr/lib64/python2.7/site-packages/numpy/core/include -I/usr/include/python2.7 -c openmoc/openmoc_wrap.cpp -o build/temp.linux-x86_64-2.7/openmoc/openmoc_wrap.o -c -Wall -O1 -ffast-math -fopenmp -std=c++0x -fpic -g
CC=ccache g++
#CPP=g++
CFLAGS=-DFP_PRECISION=float -DSINGLE -DGNU -DVEC_LENGTH=8 -DVEC_ALIGNMENT=16 -I/usr/lib64/python2.7/site-packages/numpy/core/include -I/usr/include/python2.7 -ffast-math -fopenmp -std=c++0x -fpic -g
all: surface localcoords point cell universe material log
#   python setup.py install --user --debug-mode --with-ccache
	$(CC) $(CFLAGS) src/main.cpp surface.o localcoords.o point.o universe.o cell.o material.o log.o -o main
surface:
	$(CC) $(CFLAGS) -c src/Surface.cpp -o surface.o
localcoords: cell universe
	$(CC) $(CFLAGS) -c src/LocalCoords.cpp -o localcoords.o
point:
	$(CC) $(CFLAGS) -c src/Point.cpp -o point.o
universe:
	$(CC) $(CFLAGS) -c src/Universe.cpp -o universe.o
cell:
	$(CC) $(CFLAGS) -c src/Cell.cpp -o cell.o
material:
	$(CC) $(CFLAGS) -c src/Material.cpp -o material.o
log:
	$(CC) $(CFLAGS) -c src/log.cpp -o log.o
clean:
#   python setup.py clean
	rm *.o main
