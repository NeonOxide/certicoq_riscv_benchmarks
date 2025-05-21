#!/usr/bin/env python3
import os
import re
import subprocess
import concurrent.futures
from rich.live import Live
from rich.table import Table
from pathlib import Path

# Default values for environment variables, similar to bash script
GEM5_HOME = os.environ.get("GEM5_HOME", "./gem5")
GEM5_CONF_HOME = os.environ.get("GEM5_CONF_HOME", "./gem5_configs")

# Read test files
with open("TESTS", "r") as f:
    FILES = f.read().strip().split()

# List of compilers
COMPILERS = ["ccomp", "clang", "gcc"]

# Markdown table headers
MD_TABLE_HEADER = "|program|compiler|style|optimization|seconds|milliseconds|\n|---|---|---|---|---|---|\n"
md_table_x86 = MD_TABLE_HEADER
md_table_riscv = MD_TABLE_HEADER

# Regular expression for extracting time information
TIME_REGEX = r"Time taken (?P<secs>\d+\.\d+) seconds (?P<mili>\d+\.\d+) milliseconds"


def run_benchmark(file, compiler, arch, style, opt):
    """Run a single benchmark and return the results in markdown format"""
    # Construct the filename according to the pattern
    style_suffix = "_cps" if style == "CPS" else ""
    opt_suffix = "_opt" if opt == "O1" else ""

    if arch == "x86":
        executable = f"./{file}_{compiler}_x86_64{style_suffix}{opt_suffix}"
        gem5_cmd = f"{GEM5_HOME}/build/X86/gem5.opt"
        isa_flag = "x86"
    else:  # riscv
        executable = f"./{file}_{compiler}_riscv{style_suffix}{opt_suffix}"
        gem5_cmd = f"{GEM5_HOME}/build/RISCV/gem5.opt"
        isa_flag = "riscv"

    # Check if the executable exists
    if not Path(executable).is_file():
        return None

    # Print status
    style_name = "CPS" if style == "CPS" else "direct-style"
    print(f"Running {file} comp {compiler} in {style_name} arch {arch} with {opt}")

    # Run the command
    cmd = [
        gem5_cmd,
        f"{GEM5_CONF_HOME}/simulate_device.py",
        executable,
        "--isa",
        isa_flag,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Extract timing information using regex
    match = re.search(TIME_REGEX, result.stdout)
    if match:
        secs = match.group("secs")
        mili = match.group("mili")
        return f"|{file}|{compiler}|{style_name}|{opt}|{secs}|{mili}|\n"

    return None


# List to collect all tasks
all_tasks = []

# Create all benchmark tasks
for compiler in COMPILERS:
    for file in FILES:
        # X86 tasks
        all_tasks.append(("x86", file, compiler, "direct-style", "O0"))
        # all_tasks.append(("x86", file, compiler, "CPS", "O0"))
        all_tasks.append(("x86", file, compiler, "direct-style", "O1"))
        # all_tasks.append(("x86", file, compiler, "CPS", "O1"))

        # RISCV tasks
        all_tasks.append(("riscv", file, compiler, "direct-style", "O0"))
        # all_tasks.append(("riscv", file, compiler, "CPS", "O0"))
        all_tasks.append(("riscv", file, compiler, "direct-style", "O1"))
        # all_tasks.append(("riscv", file, compiler, "CPS", "O1"))

# Execute tasks in parallel
with concurrent.futures.ProcessPoolExecutor() as executor:
    # Create a dictionary to map each future to its parameters
    future_to_params = {
        executor.submit(run_benchmark, file, compiler, arch, style, opt): (
            arch,
            file,
            compiler,
            style,
            opt,
        )
        for arch, file, compiler, style, opt in all_tasks
    }
    total = len(all_tasks)

    def generate_table() -> Table:
        table = Table()
        table.add_column(f"Remaining {len(future_to_params)} out of {total}")
        for f, (arch, file, compiler, style, opt) in future_to_params.items():
            style_suffix = "_cps" if style == "CPS" else ""
            opt_suffix = "_opt" if opt == "O1" else ""
            table.add_row(f"{file}_{compiler}_{arch}{style_suffix}{opt_suffix}")
        return table

    with Live(generate_table(), refresh_per_second=4) as live:
        # Process the completed futures as they come in
        for future in concurrent.futures.as_completed(list(future_to_params.keys())):
            params = future_to_params[future]
            arch = params[0]
            result = future.result()
            del future_to_params[future]
            live.update(generate_table())
            if result:
                if arch == "x86":
                    md_table_x86 += result
                else:  # riscv
                    md_table_riscv += result

# Print the results
print("# RISCV RESULTS")
print(md_table_riscv)
print("# X86_64 RESULTS")
print(md_table_x86)
