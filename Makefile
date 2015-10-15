.PHONY: all clean uninstall
.IGNORE: clean
.DEFAULT: all
CC=g++
CFLAGS=-DFP_PRECISION=float -DSINGLE -DGNU -DVEC_LENGTH=8 -DVEC_ALIGNMENT=16 -I/usr/lib64/python2.7/site-packages/numpy/core/include -I/usr/include/python2.7 -ffast-math -fopenmp -std=c++0x -fpic -g
OBJFILES=Surface.o LocalCoords.o Point.o Universe.o Cell.o Material.o log.o
SRCDIR=src
INSTALLDIR=~/.local/lib/python2.7/site-packages

all:main

$(OBJFILES): %.o: $(SRCDIR)/%.cpp $(SRCDIR)/%.h
	$(CC) $(CFLAGS) -c $< -o $@

main: $(OBJFILES) $(SRCDIR)/main.cpp
	$(CC) $(CFLAGS) $(SRCDIR)/$@.cpp -o $@ $(OBJFILES)
	#python setup.py install --user --debug-mode --with-ccache
clean:
	rm -v main
	python setup.py clean
	rm -v $(OBJFILES) 2>/dev/null
uninstall:
	rm -rv $(INSTALLDIR)/*openmoc* 2>/dev/null
