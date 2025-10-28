use std::fs;
use std::process::Command;
use itertools::{iproduct, Itertools};
use rayon::prelude::*;
use regex::Regex;

static COMPILERS : [&str; 3] = ["gcc", "clang", "ccomp"];
static ARCHS : [&str; 2] = ["x86_64", "riscv"];

static OPT : [&str; 2] = ["", "_opt"];

fn main() {
    let test_names = fs::read_to_string("../TESTS").expect("Failed to read ../TESTS");
    let test_names: Vec<&str> = test_names.trim().split("\n").collect();
    let test_cases = iproduct!(test_names, COMPILERS,ARCHS, OPT).collect_vec();
    let re = Regex::new(r"Time taken (?<secs>\d+\.\d+) seconds (?<mili>\d+\.\d+) milliseconds").unwrap();
    let gem5_x86 = "../../../gem5/build/X86/gem5.opt";
    let gem5_riscv = "../../../gem5/build/RISCV/gem5.opt";
    let simulate_device = "../gem5_configs/simulate_device.py";

    let results : Vec<_> = test_cases.into_par_iter().map(|(test, compiler, arch, opt)| {
        ((test, compiler, arch, opt),
         match arch {
             "x86_64" => Command::new(gem5_x86).args([simulate_device, &format!("../{test}_{compiler}_{arch}{opt}"), "--isa", "x86"]).output(),
             "riscv" => Command::new(gem5_riscv).args([simulate_device, &format!("../{test}_{compiler}_{arch}{opt}"), "--isa", "riscv"]).output(),
             _ => unreachable!()
         }
        )
    }).collect();
    let table_header = "|program|compiler|optimization|milliseconds|\n|---|---|---|---|\n";
    let mut riscv_results = table_header.to_owned();
    let mut x86_results = table_header.to_owned();
    for ((test, compiler, arch, opt), output) in results {
        let Ok(out) = output else {
            println!("Error for {test}_{compiler}_{arch}: {output:?}");
            continue
        };
        let stdout = String::from_utf8_lossy(&out.stdout);
        let Some(capt) = re.captures(&stdout) else {
            println!("Error parsing {test}_{compiler}_{arch}'s output");
            continue
        };
        let (secs, millis) : (f64, f64) = (capt["secs"].parse().unwrap(), capt["mili"].parse().unwrap());
        let table = match arch {
            "x86_64" => &mut x86_results,
            "riscv" => &mut riscv_results,
            _ => unreachable!()
        };
        let opt = if opt == "_opt" {"O1"} else { "O0" };
        *table += &format!("|{test}|{compiler}|{opt}|{millis}|\n");
    }
    println!("# RISCV RESULTS\n{riscv_results}");
    println!("# X86_64 RESULTS\n{x86_results}");
}

