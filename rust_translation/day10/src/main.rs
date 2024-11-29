use std::collections::{HashMap, HashSet, VecDeque};
use std::fs::File;
use std::io::{BufRead, BufReader};
//
// ans1: 6886
// ans2 :371
fn main() {
    let directions: HashMap<char, [[isize; 2]; 2]> = HashMap::from([
        ('|', [[-1, 0], [1, 0]]),
        ('-', [[0, -1], [0, 1]]),
        ('L', [[-1, 0], [0, 1]]),
        ('J', [[-1, 0], [0, -1]]),
        ('7', [[1, 0], [0, -1]]),
        ('F', [[1, 0], [0, 1]]),
    ]);
    let mut main_loop: Vec<[isize; 2]> = vec![];
    let file =
        File::open("/Users/etienne_lechat/aoc2023/inputs/day10.txt").expect("Failed to open file");
    let reader = BufReader::new(file);
    let mut input: Vec<Vec<char>> = reader
        .lines()
        .map(|l| l.unwrap().chars().collect::<Vec<char>>())
        .collect();
    let m = &input.len();
    let n = &input[0].len();
    'outer: for i in 0..*m {
        for j in 0..*n {
            if input[i][j] == 'S' {
                input[i][j] = 'L'; // input dependent but who cares
                let (mut x, mut y) = (i as isize, j as isize);
                //main_loop.insert([x, y]);
                let [mut dx, mut dy]: [isize; 2] = [0, 1]; // input dep also
                x += dx;
                y += dy;
                loop {
                    main_loop.push([x, y]);
                    if [x as usize, y as usize] == [i, j] {
                        break;
                    } else {
                        let [[a, b], [c, d]] =
                            directions.get(&input[x as usize][y as usize]).unwrap();
                        if [*a, *b] == [-dx, -dy] {
                            (dx, dy) = (*c, *d);
                        } else {
                            (dx, dy) = (*a, *b);
                        }
                        x += dx;
                        y += dy;
                    }
                }
                println!("The first answer is {}", main_loop.len() / 2);
                let mut vertices = main_loop
                    .iter()
                    .filter(|e| !vec!['|', '-'].contains(&input[e[0] as usize][e[1] as usize]))
                    .collect::<Vec<_>>(); // collect to temporary vec
                vertices.push(vertices[0]);
                let weird_area = vertices
                    .windows(2) // get adjacent pairs
                    .map(|w| (w[0][0] - w[1][0]) * (w[1][1] + w[0][1]))
                    .sum::<isize>();

                println!("The second answer is {}", {
                    (weird_area.abs() as usize - main_loop.len() + 2) / 2 // Apparently this is
                                                                          // called Pick s theorem
                });
                break 'outer;
            }
        }
    }
}
