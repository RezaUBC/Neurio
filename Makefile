CC = gcc
CPP = g++
# compiler flags:
CFLAGS = -g -Wall
# python linking flags:
PyFlags=-I/home/zangeneh/anaconda2/envs/aind/include/python3.6m -I/home/zangeneh/anaconda2/envs/aind/include/python3.6m  -Wsign-compare  -DNDEBUG -fwrapv -O3 -Wall -Wstrict-prototypes

# the target executable:
TARGET = production

all: $(TARGET)
	$(CPP) $(CFLAGS) &(PyFLAGS) -o $(TARGET) $(TARGET).cpp
clean:
	$(rm) $(TARGET)
