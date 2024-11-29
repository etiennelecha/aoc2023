use regex::Regex;
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file =
        File::open("/Users/etienne_lechat/aoc2023/inputs/day1.txt").expect("Failed to open file");
    let reader = BufReader::new(file);
    let re = Regex::new(
        r"[0-9]|eightwo|twone|oneight|nineight|one|two|three|four|five|six|seven|eight|nine",
    )
    .unwrap();
    let mut ans2: u32 = 0;
    let mut hmap: HashMap<&str, &str> = HashMap::new();
    hmap.insert("one", "1");
    hmap.insert("two", "2");
    hmap.insert("three", "3");
    hmap.insert("four", "4");
    hmap.insert("five", "5");
    hmap.insert("six", "6");
    hmap.insert("seven", "7");
    hmap.insert("eight", "8");
    hmap.insert("nine", "9");
    hmap.insert("oneight", "18");
    hmap.insert("twone", "21");
    hmap.insert("eightwo", "82");
    for line in reader.lines() {
        match line {
            Ok(line) => {
                let mut iter_mathces = re.find_iter(&line).map(|s| s.as_str()).peekable();
                let first = iter_mathces.peek().cloned().unwrap();
                let first_d = &hmap.get(first).unwrap_or(&first)[0..1];
                let last_ = iter_mathces.last().unwrap();
                let last_val = hmap.get(last_).unwrap_or(&last_);
                let last_d = &last_val[last_val.len() - 1..];
                //println!("Line : {}", line);
                //println!("1st: {}, last: {}", first_d, last_d);
                let res = (first_d.to_owned().to_owned() + last_d)
                    .parse::<u32>()
                    .unwrap();
                //println!("res {}", res);
                ans2 += res;
            }
            Err(e) => println!("Error reading line: {}", e),
        }
    }
    println!("Part 2 result is {}", ans2);
}
