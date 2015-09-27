.PHONY: all clean
.IGNORE: clean
.DEFAULT: all
CC=g++
CFLAGS=-DFP_PRECISION=float -DSINGLE -DGNU -DVEC_LENGTH=8 -DVEC_ALIGNMENT=16 -I/usr/lib64/python2.7/site-packages/numpy/core/include -I/usr/include/python2.7 -ffast-math -fopenmp -std=c++0x -fpic -g
OBJFILES=Surface.o LocalCoords.o Point.o Universe.o Cell.o Material.o log.o
SRCDIR=src

$(OBJFILES): %.o: $(SRCDIR)/%.cpp $(SRCDIR)/%.h
	$(CC) $(CFLAGS) -c $< -o $@

main: $(OBJFILES)
	#   python setup.py install --user --debug-mode --with-ccache
	echo $(CC) $(CFLAGS) -o $@ $(OBJFILES)

clean:
	#python setup.py clean
	rm -v $(OBJFILES) 2>/dev/null

all:main