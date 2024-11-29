use regex::Regex;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file =
        File::open("/Users/etienne_lechat/aoc2023/inputs/day2.txt").expect("Failed to open file");
    let mut ans1: usize = 0;
    let mut ans2: usize = 0;
    let reader = BufReader::new(file);
    let rb = Regex::new(r"(\d+) blue").unwrap();
    let rg = Regex::new(r"(\d+) green").unwrap();
    let rr = Regex::new(r"(\d+) red").unwrap();
    for (i, line) in reader.lines().enumerate() {
        match line {
            Ok(line) => {
                let blues = rb
                    .captures_iter(&line)
                    .map(|c| {
                        let (_, [n_blues]) = c.extract();
                        n_blues.parse::<usize>().unwrap()
                    })
                    .collect::<Vec<usize>>();
                let greens = rg
                    .captures_iter(&line)
                    .map(|c| {
                        let (_, [n_blues]) = c.extract();
                        n_blues.parse::<usize>().unwrap()
                    })
                    .collect::<Vec<usize>>();
                let reds = rr
                    .captures_iter(&line)
                    .map(|c| {
                        let (_, [n_blues]) = c.extract();
                        n_blues.parse::<usize>().unwrap()
                    })
                    .collect::<Vec<usize>>();
                let bm = blues.iter().max().unwrap();
                let rm = reds.iter().max().unwrap();
                let gm = greens.iter().max().unwrap();
                ans2 += bm * gm * rm;
                if blues.iter().all(|d| *d <= 14)
                    && greens.iter().all(|d| *d <= 13)
                    && reds.iter().all(|d| *d <= 13)
                {
                    ans1 += i;
                };
            }
            Err(_) => println!("Prout"),
        }
    }
    println!("First part is {}", ans1);
    println!("Second part is {}", ans2);
}
