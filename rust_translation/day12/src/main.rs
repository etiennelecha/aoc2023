use std::fs::File;
use std::io::{BufRead, BufReader};
use std::iter::repeat;
//
//
// ans1: 8419
// ans2 : 160500973317706
fn main() {
    let file =
        File::open("/Users/etienne_lechat/aoc2023/inputs/day12.txt").expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut ans2: u64 = 0;
    let mut ans1: u64 = 0;
    for line in reader.lines() {
        match line {
            Ok(content) => {
                let [word, groups] = content.split(' ').collect::<Vec<_>>().try_into().unwrap();
                let groupss: Vec<_> = groups
                    .split(',')
                    .map(|e| e.parse::<u64>().unwrap())
                    .collect();
                let word2 = repeat(word).take(5).collect::<Vec<&str>>().join("?");
                let groupsss: Vec<u64> = groupss.repeat(5);
                ans1 += arrangements(word.trim_matches('.'), groupss);
                ans2 += arrangements(word2.trim_matches('.'), groupsss);
            }
            Err(_) => {}
        }
    }
    println!("The first answer is {}", ans1);
    println!("The second answer is {}", ans2);
}
fn arrangements(word: &str, groups: Vec<u64>) -> u64 {
    let mut dp: Vec<Vec<u64>> = vec![vec![0; 1 + groups.len()]; 1 + word.len()];
    // dp[i][j] # number of arrgmebts for groups[:i], words[:j] ("up to i, but not including i)
    dp[0][0] = 1;
    let mut with_roken: bool = false;
    for i in 1..=word.len() {
        if !with_roken && &word[i - 1..i] == "#" {
            with_roken = true;
        }
        if !with_roken {
            dp[i][0] = 1
        } else {
            dp[i][0] = 0
        }
        for j in 1..=groups.len() {
            if &word[i - 1..i] == "." {
                dp[i][j] = dp[i - 1][j];
            } else {
                let n_broken: u64;
                let tar: usize = groups[j - 1].try_into().unwrap();
                let mut k = 0;
                while i - 1 - k > 0 {
                    if &word[i - 2 - k..i - k - 1] == "." {
                        break;
                    } else if k == tar - 1 && &word[i - 2 - k..i - k - 1] == "?" {
                        break;
                    } else if k > tar - 1 {
                        break;
                    } else {
                        k += 1;
                    }
                }
                if k == tar - 1 {
                    if i - k - 1 == 0 {
                        n_broken = dp[0][j - 1];
                    } else {
                        n_broken = dp[i - k - 2][j - 1];
                    }
                } else {
                    n_broken = 0;
                }
                match &word[i - 1..i] {
                    "#" => dp[i][j] = n_broken,
                    _ => dp[i][j] = dp[i - 1][j] + n_broken,
                }
            }
        }
    }
    dp[word.len()][groups.len()]
}
