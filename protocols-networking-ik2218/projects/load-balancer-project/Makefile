CC = gcc
CFLAGS = -Iinclude -Wall -Wextra -pthread
SRC = src/main.c src/proxy.c src/backend.c
OBJ = $(SRC:.c=.o)
TARGET = bin/balancer

all: $(TARGET)

$(TARGET): $(OBJ)
	mkdir -p bin
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -rf src/*.o bin/
