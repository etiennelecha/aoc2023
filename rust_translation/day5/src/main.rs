use regex::Regex;
use std::fs::File;
use std::io::{BufRead, BufReader};

//ans1 : 825516882
//ans2 : 136096660

fn map_singleton(range: [i64; 2], proj: [i64; 3]) -> (Option<Vec<[i64; 2]>>, Option<[i64; 2]>) {
    // First retrun value is the parts untouched, second the itersect;
    let [a, b] = range;
    let [des, start, length] = proj;
    let offset = des - start;
    let end = start + length - 1; // inclusive : the end gets moved also
    if b < start || a > end {
        (Some(vec![range]), None)
    } else if a >= start && b <= end {
        (None, Some([a + offset, b + offset]))
    } else if a < start && b <= end {
        (
            Some(vec![[a, start - 1]]),
            Some([start + offset, b + offset]),
        )
    } else if a >= start && b > end {
        (Some(vec![[end + 1, b]]), Some([a + offset, end + offset]))
    } else if a < start && b > end {
        (
            Some(vec![[a, start - 1], [end + 1, b]]),
            Some([start + offset, end + offset]),
        )
    } else {
        (None, None)
    }
}
fn map_2_rec(
    mut ranges: Vec<[i64; 2]>,
    projs: Vec<[i64; 3]>,
    acc: &mut Vec<[i64; 2]>,
) -> Vec<[i64; 2]> {
    if projs.is_empty() {
        ranges.append(acc);
        ranges
    } else {
        let mut new_ranges = vec![];
        let (proj, new_projs) = (&projs[0], &projs[1..]);
        for range in ranges {
            let (untouched, isct) = map_singleton(range, *proj);
            if let Some(mut vecs) = untouched {
                new_ranges.append(&mut vecs);
            };
            if let Some(arr) = isct {
                acc.push(arr);
            }
        }
        map_2_rec(new_ranges, new_projs.to_vec(), acc)
    }
}
fn map_2_recrec(ranges: Vec<[i64; 2]>, projss: &Vec<Vec<[i64; 3]>>) -> Vec<[i64; 2]> {
    if projss.is_empty() {
        ranges
    } else {
        let mut acc = vec![];
        let (projs, new_args) = (&projss[0], &projss[1..]);
        map_2_recrec(
            map_2_rec(ranges, projs.clone(), &mut acc),
            &new_args.to_vec(),
        )
    }
}
fn main() {
    let file =
        File::open("/Users/etienne_lechat/aoc2023/inputs/day5.txt").expect("Failed to open file");
    let reader = BufReader::new(file);
    let re = Regex::new(r"\d+").unwrap();
    let mut projss: Vec<Vec<[i64; 3]>> = vec![];
    let mut projs: Vec<[i64; 3]> = vec![];
    let mut input1: Vec<[i64; 2]> = vec![];
    let mut input2: Vec<[i64; 2]> = vec![];
    for (i, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        if i == 0 {
            let input: Vec<i64> = re
                .find_iter(&line)
                .map(|m| m.as_str().parse::<i64>().unwrap())
                .collect::<Vec<i64>>();
            input1.append(&mut input.iter().map(|e| [*e, *e]).collect());
            let mut inputit = input.iter();
            loop {
                if let (Some(a), Some(b)) = (inputit.next(), inputit.next()) {
                    input2.push([*a, a + b - 1]);
                } else {
                    break;
                }
            }
        } else {
            if re.is_match(&line) {
                projs.push(
                    re.find_iter(&line)
                        .map(|m| m.as_str().parse::<i64>().unwrap())
                        .collect::<Vec<i64>>()
                        .try_into()
                        .unwrap(),
                );
            } else {
                if projs.len() != 0 {
                    projss.push(projs);
                    projs = vec![];
                }
            }
        }
    }
    projss.push(projs);
    for pjs in &projss {
        for p in pjs {
            for n in p {
                print!("{} ", n);
            }
            println!();
        }
        println!();
    }
    println!("======================================");
    for arr in &input1 {
        for n in arr {
            print!("{} ", n);
        }
        println!();
    }
    let ranges1 = map_2_recrec(input1, &projss);
    let ans1 = ranges1.iter().min_by_key(|arr| arr[0]).unwrap()[0];
    println!("--------------------------------------");
    println!("The first answer is: {}", ans1);
    println!("======================================");
    let ranges2 = map_2_recrec(input2, &projss);
    let ans2 = ranges2.iter().min_by_key(|arr| arr[0]).unwrap()[0];
    println!("--------------------------------------");
    println!("The second answer is: {}", ans2);
    println!("======================================");
}
