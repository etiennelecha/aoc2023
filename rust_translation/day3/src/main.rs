use std::fs::File;
use std::io::{BufRead, BufReader};

fn get_number(numbers: &str, input: &mut Vec<Vec<char>>, i: usize, j: usize) -> usize {
    let m = input.len();
    let n = input.iter().next().unwrap().len();
    if i < m {
        if j < n {
            let char_ = input[i][j];
            if !numbers.contains(char_) {
                0
            } else {
                let mut s = input[i][j].to_string();
                let mut k = j - 1;
                loop {
                    let char_ = input[i][k];
                    if !numbers.contains(char_) {
                        break;
                    } else {
                        s = char_.to_string() + &s;
                        input[i][k] = '.';
                        if k == 0 {
                            break;
                        } else {
                            k -= 1;
                        };
                    };
                }
                let mut l = j + 1;
                while let Some(char_) = input[i].get(l) {
                    if !numbers.contains(*char_) {
                        break;
                    } else {
                        s = s + &char_.to_string();
                        input[i][l] = '.';
                        l += 1;
                    };
                }
                s.parse::<usize>().unwrap()
            }
        } else {
            0
        }
    } else {
        0
    }
}
fn get_number2(numbers: &str, input: &Vec<Vec<char>>, i: usize, j: usize) -> usize {
    let m = input.len();
    let n = input.iter().next().unwrap().len();
    if i < m {
        if j < n {
            let char_ = input[i][j];
            if !numbers.contains(char_) {
                0
            } else {
                let mut s = input[i][j].to_string();
                let mut k = j - 1;
                loop {
                    let char_ = input[i][k];
                    if !numbers.contains(char_) {
                        break;
                    } else {
                        s = char_.to_string() + &s;
                        if k == 0 {
                            break;
                        } else {
                            k -= 1;
                        };
                    };
                }
                let mut l = j + 1;
                while let Some(char_) = input[i].get(l) {
                    if !numbers.contains(*char_) {
                        break;
                    } else {
                        s = s + &char_.to_string();
                        l += 1;
                    };
                }
                s.parse::<usize>().unwrap()
            }
        } else {
            0
        }
    } else {
        0
    }
}
fn get_numbers(numbers: &str, input: &Vec<Vec<char>>, i: usize, j: usize) -> Vec<usize> {
    let mut ans: Vec<usize> = vec![];
    if i > 0 {
        let charup = input[i - 1][j];
        if !numbers.contains(charup) {
            let upright = get_number2(numbers, &input, i - 1, j + 1);
            if upright > 0 {
                ans.push(upright);
            };
            if j > 0 {
                let upleft = get_number2(numbers, &input, i - 1, j - 1);
                if upleft > 0 {
                    ans.push(upleft);
                };
            };
        } else {
            let up = get_number2(numbers, &input, i - 1, j);
            if up > 0 {
                ans.push(up);
            }
        }
    };
    let right = get_number2(numbers, &input, i, j + 1);
    if right > 0 {
        ans.push(right);
    };
    if j > 0 {
        let left = get_number2(numbers, &input, i, j - 1);
        if left > 0 {
            ans.push(left);
        };
    };
    if let Some(_) = input.get(i + 1) {
        let chardown = input[i + 1][j];
        if !numbers.contains(chardown) {
            let downright = get_number2(numbers, &input, i + 1, j + 1);
            if downright > 0 {
                ans.push(downright);
            };
            if j > 0 {
                let downleft = get_number2(numbers, &input, i + 1, j - 1);
                if downleft > 0 {
                    ans.push(downleft);
                };
            };
        } else {
            let down = get_number2(numbers, &input, i + 1, j);
            if down > 0 {
                ans.push(down);
            }
        }
    };
    ans
}
fn main() {
    let file =
        File::open("/Users/etienne_lechat/aoc2023/inputs/day3.txt").expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut input: Vec<Vec<char>> = reader
        .lines()
        .map(|l| l.unwrap().chars().collect::<Vec<char>>())
        .collect();
    let symbols = "*$+-%#&=/@";
    let numbers = "0123456789";
    let m = input.len();
    let n = input.iter().next().unwrap().len();
    let mut ans1: usize = 0;
    for i in 0..m {
        for j in 0..n {
            if symbols.contains(input[i][j]) {
                ans1 += get_number(numbers, &mut input, i + 1, j + 1);
                ans1 += get_number(numbers, &mut input, i, j + 1);
                ans1 += get_number(numbers, &mut input, i + 1, j);
                if i > 0 {
                    ans1 += get_number(numbers, &mut input, i - 1, j);
                    ans1 += get_number(numbers, &mut input, i - 1, j + 1);
                };
                if j > 0 {
                    ans1 += get_number(numbers, &mut input, i, j - 1);
                    ans1 += get_number(numbers, &mut input, i + 1, j - 1);
                };
                if j > 0 && i > 0 {
                    ans1 += get_number(numbers, &mut input, i - 1, j - 1);
                };
            }
        }
    }
    println!("height {}, width {}", m, n);
    println!("The first answer is  {}", ans1);
    // ----------- PART TWO ----------------
    let file =
        File::open("/Users/etienne_lechat/aoc2023/inputs/day3.txt").expect("Failed to open file");
    let reader = BufReader::new(file);
    let input: Vec<Vec<char>> = reader
        .lines()
        .map(|l| l.unwrap().chars().collect::<Vec<char>>())
        .collect();
    // for i in 0..m {
    //     for j in 0..n {
    //         print!("{}", input[i][j]);
    //     }
    //     println!();
    // }

    let mut ans2: usize = 0;
    for i in 0..m {
        for j in 0..n {
            if input[i][j] == '*' {
                let nums = get_numbers(numbers, &input, i, j);
                // for num in nums.iter() {
                //     print!("{} ", num);
                // }
                // println!("");
                if nums.len() == 2 {
                    ans2 += nums[0] * nums[nums.len() - 1];
                }
            }
        }
    }
    println!("The second answer is {}", ans2);
}
