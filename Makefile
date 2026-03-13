# ============================================================
# Makefile — theoretical-physics-research C code
# ============================================================

CC      = gcc
CFLAGS  = -O2 -Wall -Wextra -std=c11
LIBS    = -lm -lgsl -lgslcblas
INCLUDE = -Isrc/include

SRC     = src/main.c
TARGET  = bin/main

.PHONY: all clean test

all: $(TARGET)

$(TARGET): $(SRC)
	@mkdir -p bin
	$(CC) $(CFLAGS) $(INCLUDE) -o $@ $^ $(LIBS)
	@echo "Build successful: $(TARGET)"

clean:
	rm -rf bin/
	@echo "Cleaned."

test:
	pytest tests/ -v
