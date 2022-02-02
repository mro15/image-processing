CC = gcc
CFLAGS = -Wall -O3 -march=native

INCL = -I ./include

DEPS = include/*

OBJ = knn.o

EXEC = knn

$(EXEC): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c $(DEPS)
	$(CC) $(CFLAGS) -c -o $@ $< $(INCL)

all: $(EXEC)

clean:
	rm -f $(OBJ) knn

