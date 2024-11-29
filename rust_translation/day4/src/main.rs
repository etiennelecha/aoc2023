use regex::Regex;
use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};
// ans 1 : 23235
// ans 2 : 5920640
fn main() {
    let file =
        File::open("/Users/etienne_lechat/aoc2023/inputs/day4.txt").expect("Failed to open file");
    let reader = BufReader::new(file);
    let input: Vec<String> = reader.lines().map(|l| l.unwrap()).collect();
    let re = Regex::new(r"\d+").unwrap();
    let mut ans1: u32 = 0;
    let mut ans2: u32 = 0;
    let mut n_cards: [u32; 202] = [1; 202]; //  n_cards per game
    for (i, line) in input.iter().enumerate() {
        ans2 += n_cards[i];
        let numbers: Vec<&str> = re.find_iter(line).map(|m| m.as_str()).collect();
        let winning_hand = &numbers[1..11];
        let actual_hand: HashSet<_> = numbers[11..36].into_iter().collect();

        let mut count: u32 = 0;
        for num in winning_hand.iter() {
            if actual_hand.contains(num) {
                count += 1;
            }
        }
        if count > 0 {
            ans1 += u32::pow(2, count - 1);
            for offset in 1..(<u32 as TryInto<usize>>::try_into(count).unwrap() + 1) {
                n_cards[i + offset] += n_cards[i];
            }
        }
    }
    println!("This first answer is {}", ans1);
    println!("This second answer is {}", ans2);
}
