#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import seaborn as sns


# Function to read and parse markdown tables
def parse_markdown_table(md_table):
    lines = md_table.strip().split("\n")
    # Skip the header and separator lines
    data_lines = lines[2:]

    data = []
    for line in data_lines:
        # Split by | and remove empty elements
        parts = [part.strip() for part in line.split("|")]
        parts = [part for part in parts if part]

        if len(parts) == 6:  # Ensure we have the expected number of columns
            program, compiler, style, optimization, seconds, milliseconds = parts
            # Convert time values to numeric
            seconds = float(seconds)
            milliseconds = float(milliseconds)
            # Calculate total time in milliseconds for easier comparison
            total_ms = seconds * 1000

            data.append(
                {
                    "program": program,
                    "compiler": compiler,
                    "style": style,
                    "optimization": optimization,
                    "seconds": seconds,
                    "milliseconds": milliseconds,
                    "total_ms": total_ms,
                }
            )

    return pd.DataFrame(data)


# Function to read the markdown output file
def read_md_output(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    # Split the content into RISCV and X86_64 parts
    parts = content.split("# RISCV RESULTS\n")
    if len(parts) > 1:
        riscv_and_x86 = parts[1].split("# X86_64 RESULTS\n")
        riscv_md = riscv_and_x86[0]
        x86_md = riscv_and_x86[1] if len(riscv_and_x86) > 1 else ""
    else:
        riscv_md = ""
        x86_md = ""
    # Parse the markdown tables
    riscv_df = parse_markdown_table(riscv_md) if riscv_md else pd.DataFrame()
    x86_df = parse_markdown_table(x86_md) if x86_md else pd.DataFrame()

    # Add architecture column to each DataFrame
    if not riscv_df.empty:
        riscv_df["architecture"] = "RISCV"
    if not x86_df.empty:
        x86_df["architecture"] = "x86"

    # Combine into a single DataFrame
    combined_df = pd.concat([riscv_df, x86_df], ignore_index=True)
    return combined_df


# Function to create charts
def create_charts(df):
    if df.empty:
        print("No data available for charts")
        return

    # Set the style
    sns.set(style="whitegrid")
    plt.rcParams.update({"font.size": 12})

    # Chart 1: Average time by architecture, comparing unoptimized and optimized
    plt.figure(figsize=(12, 8))

    # Group by architecture and optimization
    arch_opt_df = (
        df.groupby(["architecture", "optimization"])["total_ms"].mean().reset_index()
    )
    print(arch_opt_df)
    # Plot
    ax = sns.barplot(
        x="architecture",
        y="total_ms",
        hue="optimization",
        data=arch_opt_df,
        palette="viridis",
    )

    plt.title("Average Execution Time by Architecture and Optimization Level")
    plt.xlabel("Architecture")
    plt.ylabel("Time (milliseconds)")
    plt.grid(True, linestyle="--", alpha=0.7)
    for bars in ax.containers:
        ax.bar_label(bars)

    plt.tight_layout()
    plt.savefig("avg_time_by_arch_opt.png")
    plt.close()

    # Chart 2: Program-by-program comparison across architectures
    # Get unique programs
    programs = df["program"].unique()

    for program in programs:
        plt.figure(figsize=(14, 8))

        # Filter data for this program
        program_df = df[df["program"] == program]

        # Group by architecture, compiler, and optimization
        plot_df = (
            program_df.groupby(["architecture", "compiler", "optimization"])["total_ms"]
            .mean()
            .reset_index()
        )

        # Create a more readable x-axis label
        plot_df["config"] = plot_df["compiler"] + " (" + plot_df["optimization"] + ")"

        # Plot
        ax = sns.barplot(
            x="config", y="total_ms", hue="architecture", data=plot_df, palette="Set2"
        )

        plt.title(f"Execution Time for {program} across Architectures and Compilers")
        plt.xlabel("Compiler (Optimization Level)")
        plt.ylabel("Time (milliseconds)")
        plt.legend(title="Architecture")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.xticks(rotation=45)

        for bars in ax.containers:
            ax.bar_label(bars)

        plt.tight_layout()
        plt.savefig(f"{program}_comparison.png")
        plt.close()

    # Chart 3: Average time by compiler for each architecture (optimized and unoptimized)
    plt.figure(figsize=(16, 10))

    # Group by architecture, compiler, and optimization
    compiler_df = (
        df.groupby(["architecture", "compiler", "optimization"])["total_ms"]
        .mean()
        .reset_index()
    )

    # Plot
    g = sns.catplot(
        data=compiler_df,
        x="compiler",
        y="total_ms",
        hue="optimization",
        col="architecture",
        kind="bar",
        height=6,
        aspect=0.8,
        palette="deep",
    )
    sns.move_legend(g, "upper right")

    g.set_axis_labels("Compiler", "Average Time (milliseconds)")
    g.set_titles("{col_name}")
    g.fig.suptitle(
        "Average Execution Time by Compiler and Optimization Level", y=5.05, fontsize=16
    )

    # Add value labels

    # for bars in g.containers:
    #    g.bar_label(bars)
    for ax in g.axes.flat:
        for container in ax.containers:
            ax.bar_label(container)
    plt.tight_layout()
    plt.savefig("avg_time_by_compiler.png")
    plt.close()

    # Chart 4: Style comparison (direct-style vs CPS) for each architecture
    plt.figure(figsize=(14, 8))

    # Group by architecture, style, and optimization
    style_df = (
        df.groupby(["architecture", "style", "optimization"])["total_ms"]
        .mean()
        .reset_index()
    )

    # Plot
    g = sns.catplot(
        data=style_df,
        x="style",
        y="total_ms",
        hue="optimization",
        col="architecture",
        kind="bar",
        height=6,
        aspect=0.8,
        palette="Set1",
    )

    g.set_axis_labels("Programming Style", "Average Time (milliseconds)")
    g.set_titles("{col_name}")
    g.fig.suptitle(
        "Average Execution Time by Programming Style and Optimization Level",
        y=1.05,
        fontsize=16,
    )

    # Add value labels
    for ax in g.axes.flat:
        for p in ax.patches:
            ax.annotate(
                f"{p.get_height():.2f}",
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="bottom",
                xytext=(0, 5),
                textcoords="offset points",
            )

    plt.tight_layout()
    plt.savefig("avg_time_by_style.png")
    plt.close()


def main():
    # Prompt for the input file or use a default
    input_file = input(
        "Enter the path to the markdown output file (or press Enter to use 'benchmark_results.md'): "
    ).strip()
    if not input_file:
        input_file = "benchmark_results.md"

    print(f"Reading data from {input_file}...")

    try:
        # Read and process the markdown file
        df = read_md_output(input_file)

        if df.empty:
            print("No data was parsed from the file. Please check the file format.")
            return

        print(f"Parsed {len(df)} data points.")
        print("\nGenerating charts...")

        # Create all charts
        create_charts(df)

        print("\nCharts have been generated successfully:")
        print(
            "1. avg_time_by_arch_opt.png - Average time comparison between x86 and RISCV (optimized vs. unoptimized)"
        )
        print(
            "2. [program]_comparison.png - Individual program comparisons across architectures and compilers"
        )
        print(
            "3. avg_time_by_compiler.png - Average time by compiler for each architecture"
        )
        print(
            "4. avg_time_by_style.png - Comparison of programming styles (direct-style vs CPS)"
        )

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
