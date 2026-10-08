#!/data/data/com.termux/files/usr/bin/bash
set -e

cd ~/Leather

CXX="${CXX:-clang++}"

"$CXX" \
    -std=c++20 \
    -O2 \
    -Wall \
    -Wextra \
    -pedantic \
    src/lth06/lth06.cpp \
    tests/lth06/test_lth06.cpp \
    -o /tmp/leather_lth06_test

/tmp/leather_lth06_test
