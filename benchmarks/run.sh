#!/bin/bash

FILES=$(cat TESTS)

compilers=(ccomp clang gcc)

echo "Running each test ${1} times"

for comp in "${compilers[@]}"; do
    for f in $FILES; do
        if [ -f "${f}_${comp}_x86_64" ]; then
            echo "Running ${f} comp ${comp} in direct-style arch x86_64 with O0"
            ./${f}_${comp}_x86_64 $1
        fi
        if [ -f "${f}_${comp}_x86_64_cps" ]; then
            echo "Running ${f} comp ${comp} in CPS arch x86_64 with O0"
            ./${f}_${comp}_x86_64_cps $1
        fi
        if [ -f "${f}_${comp}_x86_64_opt" ]; then
            echo "Running ${f} comp ${comp} in direct-style arch x86_64 with O1"
            ./${f}_${comp}_x86_64_opt $1
        fi
        if [ -f "${f}_${comp}_x86_64_cps_opt" ]; then
            echo "Running ${f} comp ${comp} in CPS arch x86_64 with O1"
            ./${f}_${comp}_x86_64_cps_opt $1
        fi
        if [ -f "${f}_${comp}_riscv" ]; then
            echo "Running ${f} comp ${comp} in direct-style arch riscv with O0"
            ./${f}_${comp}_riscv $1
        fi
        if [ -f "${f}_${comp}_riscv_cps" ]; then
            echo "Running ${f} comp ${comp} in CPS arch riscv with O0"
            ./${f}_${comp}_riscv_cps $1
        fi
        if [ -f "${f}_${comp}_riscv_opt" ]; then
            echo "Running ${f} comp ${comp} in direct-style arch riscv with O1"
            ./${f}_${comp}_riscv_opt $1
        fi
        if [ -f "${f}_${comp}_riscv_cps_opt" ]; then
            echo "Running ${f} comp ${comp} in CPS arch riscv with O1"
            ./${f}_${comp}_riscv_cps_opt $1
        fi
    done
done
