#!/usr/bin/env python3
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator
from gem5.isas import ISA
from gem5.isas import get_isa_from_str
from gem5.components.processors.cpu_types import get_cpu_type_from_str
from gem5.components.cachehierarchies.classic.private_l1_shared_l2_cache_hierarchy import (
    PrivateL1SharedL2CacheHierarchy,
)
import argparse

# Set up the argument parser
parser = argparse.ArgumentParser()
# Positional argument for executable
parser.add_argument("executable", help="Path to the executable file to simulate")
# Argument for the number of executions to measure
parser.add_argument(
    "--num_exec",
    type=int,
    default=1,
    help="Number of executions to measure performance (default: 1)",
)
# Argument for L1 data cache size
parser.add_argument(
    "--l1d_size", default="64KiB", help="L1 data cache size (default: 64KiB)"
)
# Argument for L1 instruction cache size
parser.add_argument(
    "--l1i_size", default="64KiB", help="L1 instruction cache size (default: 64KiB)"
)
# Argument for L2 cache size
parser.add_argument("--l2_size", default="1MiB", help="L2 cache size (default: 1MiB)")
# Argument for number of cores in the processor
parser.add_argument(
    "--num_cores", type=int, default=1, help="Number of processor cores (default: 1)"
)
# Argument for the ISA type (X86 or RISCV)
parser.add_argument(
    "--isa",
    choices=["x86", "riscv"],
    required=True,
    type=str,
    help="Set the ISA type (X86 or RISCV)",
)
# Argument for CPU type (timing or atomic)
parser.add_argument(
    "--cpu_type",
    choices=["atomic", "timing"],
    default="timing",
    help="Set the CPU type (TIMING or ATOMIC) (default: TIMING)",
)
# Argument for memory size
parser.add_argument(
    "--memory_size",
    default="1GiB",
    help="Size of the memory (e.g., '1GiB') (default: 1GiB)",
)
# Argument for the clock frequency
parser.add_argument(
    "--clk_freq",
    default="1GHz",
    help="Clock frequency of the processor (default: 1GHz)",
)
# Parse the arguments
args = parser.parse_args()
# Obtain the components.
cache_hierarchy = PrivateL1SharedL2CacheHierarchy(
    l1d_size=args.l1d_size, l1i_size=args.l1i_size, l2_size=args.l2_size
)
memory = SingleChannelDDR3_1600(args.memory_size)
processor = SimpleProcessor(
    cpu_type=get_cpu_type_from_str(args.cpu_type),
    num_cores=args.num_cores,
    isa=get_isa_from_str(args.isa),
)
# Add them to the board.
board = SimpleBoard(
    clk_freq=args.clk_freq,
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
# Set the workload.
binary = BinaryResource(args.executable)
board.set_se_binary_workload(binary, arguments=[args.num_exec])
# Setup the Simulator and run the simulation.
simulator = Simulator(board=board)
simulator.run()
