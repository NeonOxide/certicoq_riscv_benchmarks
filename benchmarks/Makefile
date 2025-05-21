COQOPTS = -R ./ CertiCoq.Benchmarks -R lib CertiCoq.Benchmarks.lib
# Names of the benchmarks
TESTS=$(shell cat TESTS)


# Define compilers and architectures
COMPILERS = ccomp clang gcc
ARCHS = riscv x86_64

# Names of the generated cfiles
CFILES= $(patsubst %, CertiCoq.Benchmarks.tests.%.c, $(TESTS))

# Names of the generated executables

# Base tests
BASE_EXECS = $(TESTS)

# Tests with _opt suffix
OPT_EXECS = $(patsubst %, %_opt, $(TESTS))

# Tests with compiler and architecture combinations
COMPILER_ARCH_EXECS = $(foreach test,$(TESTS),$(foreach compiler,$(COMPILERS),$(foreach arch,$(ARCHS),$(test)_$(compiler)_$(arch))))

# Tests with compiler, architecture, and _opt suffix
COMPILER_ARCH_OPT_EXECS = $(foreach test,$(TESTS),$(foreach compiler,$(COMPILERS),$(foreach arch,$(ARCHS),$(test)_$(compiler)_$(arch)_opt)))

# Combined list of all executables
EXEC = $(BASE_EXECS) $(OPT_EXECS) $(COMPILER_ARCH_EXECS) $(COMPILER_ARCH_OPT_EXECS)


INCLUDE=../runtime
TOOLS=/usr/local/certicoq
all: lib
default: exec run
.PHONY: all default clean lib cleanlib tests run $(TESTS)
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
	rm -f *.png
	$(MAKE) clean -C lib
cleanexec:
	rm -f $(EXEC)
cleanresults:
	rm -f *.png
lib/Makefile:
	cd lib; coq_makefile -f _CoqProject -o Makefile
lib: lib/Makefile
	$(MAKE) -C lib
cleanlib:
	$(MAKE) clean -C lib
tests.stamp: tests.v
	coqc $(COQOPTS) tests.v
	touch tests.stamp

rust_tests.stamp: rust_tests.v
	coqc $(COQOPTS) rust_tests.v
	touch rust_tests.stamp

$(CFILES) : tests.stamp

# Define a rule pattern for each executable variant

# RISCV CCOMP
%_ccomp_riscv: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%.c glue_%.c
	$(TOOLS)/riscv/ccomp -static -o $@ -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*.c glue_$*.c

%_ccomp_riscv_opt: %_main.c $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.%_opt.c glue_%.c
	$(TOOLS)/riscv/ccomp -static -o $@ -w -O2 -I$(INCLUDE) $< $(INCLUDE)/gc_stack.c CertiCoq.Benchmarks.tests.$*_opt.c glue_$*.c

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



run_rust: rust_tests.stamp
	bash ./process-rust-extraction.sh



# Generate all variants for each test
define generate_test_targets
$(1): $(1)_ccomp_riscv $(1)_ccomp_riscv_opt \
      $(1)_gcc_riscv $(1)_gcc_riscv_opt \
      $(1)_clang_riscv $(1)_clang_riscv_opt \
      $(1)_ccomp_x86_64 $(1)_ccomp_x86_64_opt \
      $(1)_gcc_x86_64 $(1)_gcc_x86_64_opt \
      $(1)_clang_x86_64 $(1)_clang_x86_64_opt
endef

$(foreach test,$(TESTS),$(eval $(call generate_test_targets,$(test))))
