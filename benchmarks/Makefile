COQOPTS = -R ./ CertiCoq.Benchmarks -R lib CertiCoq.Benchmarks.lib
TOOLS=../../tools
# Names of the benchmarks
TESTS=$(shell cat TESTS)
# Names of the generated cfiles
CFILES= $(patsubst %, CertiCoq.Benchmarks.tests.%.c, $(TESTS))



GCC_X86_TARGETS=$(foreach test,$(TESTS),$(test)_gcc_x86_64)
GCC_X86_OPT_TARGETS=$(foreach test,$(TESTS),$(test)_gcc_x86_64_opt)
GCC_RISCV_TARGETS=$(foreach test,$(TESTS),$(test)_gcc_riscv)
GCC_RISCV_OPT_TARGETS=$(foreach test,$(TESTS),$(test)_gcc_riscv_opt)

CCOMP_X86_TARGETS=$(foreach test,$(TESTS),$(test)_ccomp_x86_64)
CCOMP_X86_OPT_TARGETS=$(foreach test,$(TESTS),$(test)_ccomp_x86_64_opt)
CCOMP_RISCV_TARGETS=$(foreach test,$(TESTS),$(test)_ccomp_riscv)
CCOMP_RISCV_OPT_TARGETS=$(foreach test,$(TESTS),$(test)_ccomp_riscv_opt)

CLANG_X86_TARGETS=$(foreach test,$(TESTS),$(test)_clang_x86_64)
CLANG_X86_OPT_TARGETS=$(foreach test,$(TESTS),$(test)_clang_x86_64_opt)
CLANG_RISCV_TARGETS=$(foreach test,$(TESTS),$(test)_clang_riscv)
CLANG_RISCV_OPT_TARGETS=$(foreach test,$(TESTS),$(test)_clang_riscv_opt)

compile: $(GCC_X86_TARGETS) $(GCC_X86_OPT_TARGETS) $(GCC_RISCV_TARGETS) $(GCC_RISCV_OPT_TARGETS) \
         $(CCOMP_X86_TARGETS) $(CCOMP_X86_OPT_TARGETS) $(CCOMP_RISCV_TARGETS) $(CCOMP_RISCV_OPT_TARGETS) \
         $(CLANG_X86_TARGETS) $(CLANG_X86_OPT_TARGETS) $(CLANG_RISCV_TARGETS) $(CLANG_RISCV_OPT_TARGETS)

INCLUDE=../runtime

all: lib tests.stamp compile

default: exec run

.PHONY: all default clean lib cleanlib run compile $(TESTS)

exec: $(TESTS)

clean:
	rm -f ./main.c
	rm -f ./*.*.c
	rm -f ./*.*.h
	rm -f ./glue.*.*.c
	rm -f ./glue.*.*.h
	rm -f ./glue_*.h
	rm -f ./glue_*.c
	rm -f ./*.vo
	rm -f ./*.vos
	rm -f ./*.vok
	rm -f ./*.glob
	rm -f ${EXEC}

cleanexec:
	rm -f $(EXEC)

lib/Makefile:
	cd lib; coq_makefile -f _CoqProject -o Makefile

lib: lib/Makefile
	$(MAKE) -C lib

cleanlib:
	$(MAKE) clean -C lib

tests.stamp: tests.v
	coqc $(COQOPTS) tests.v
	touch tests.stamp


# Define a rule pattern for each executable variant

# RISCV CCOMP
%_ccomp_riscv: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%.c glue_%.c
	$(TOOLS)/riscv/ccomp -static -o $@ -w -O2 -I$(INCLUDE) $< -L$(TOOLS)/riscv/ $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*.c glue_$*.c

%_ccomp_riscv_opt: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%_opt.c glue_%.c
	$(TOOLS)/riscv/ccomp -static -o $@ -w -O2 -I$(INCLUDE) $< -L$(TOOLS)/riscv/ $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*_opt.c glue_$*.c

# RISCV GCC
%_gcc_riscv: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%.c glue_%.c
	riscv64-linux-gnu-gcc -static -o $@ -fpermissive -fomit-frame-pointer -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*.c glue_$*.c

%_gcc_riscv_opt: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%_opt.c glue_%.c
	riscv64-linux-gnu-gcc -static -o $@ -fpermissive -fomit-frame-pointer -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*_opt.c glue_$*.c

# RISCV CLANG
%_clang_riscv: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%.c glue_%.c
	clang -static -fuse-ld=/usr/riscv64-linux-gnu/bin/ld -march=rv64gc --target=riscv64-linux-gnu --sysroot=/usr/riscv64-linux-gnu -L/usr/lib/gcc-cross/riscv64-linux-gnu/12/ -o $@ -fpermissive -fomit-frame-pointer -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*.c glue_$*.c

%_clang_riscv_opt: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%_opt.c glue_%.c
	clang -static -fuse-ld=/usr/riscv64-linux-gnu/bin/ld -march=rv64gc --target=riscv64-linux-gnu --sysroot=/usr/riscv64-linux-gnu -L/usr/lib/gcc-cross/riscv64-linux-gnu/12/ -o $@ -fpermissive -fomit-frame-pointer -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*_opt.c glue_$*.c

# X86_64 CCOMP
%_ccomp_x86_64: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%.c glue_%.c
	$(TOOLS)/x86/ccomp -static -o $@ -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*.c glue_$*.c

%_ccomp_x86_64_opt: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%_opt.c glue_%.c
	$(TOOLS)/x86/ccomp -static -o $@ -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*_opt.c glue_$*.c

# X86_64 GCC
%_gcc_x86_64: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%.c glue_%.c
	gcc -static -o $@ -fpermissive -fomit-frame-pointer -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*.c glue_$*.c

%_gcc_x86_64_opt: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%_opt.c glue_%.c
	gcc -static -o $@ -fpermissive -fomit-frame-pointer -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*_opt.c glue_$*.c

# X86_64 CLANG
%_clang_x86_64: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%.c glue_%.c
	clang -o $@ -fpermissive -fomit-frame-pointer -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*.c glue_$*.c

%_clang_x86_64_opt: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%_opt.c glue_%.c
	clang -o $@ -fpermissive -fomit-frame-pointer -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*_opt.c glue_$*.c
