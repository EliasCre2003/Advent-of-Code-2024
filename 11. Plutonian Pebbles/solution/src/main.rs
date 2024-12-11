use std::{collections::HashMap, f64, time::Instant};


fn split_stone(stone: u64) -> Vec<u64> {
    if stone == 0 {
        return vec![1]
    }
    let n_digits = stone.ilog10() + 1;
    if n_digits % 2 == 0 {
        let tens = 10f64.powf((n_digits / 2) as f64) as u64;
        // powf64(a, x)
        return vec![
            stone / tens,
            stone % tens
        ]
    }
    return vec![stone * 2024];
}

fn width_at_depth(stone: u64, target_depth: u64, cache: &mut HashMap<(u64, u64), u64>, current_depth: u64) -> u64 {
    if target_depth == current_depth {return 1}
    let key = (stone, target_depth - current_depth);
    if cache.contains_key(&key) {return *cache.get(&key).unwrap()}
    let result = split_stone(stone)
        .iter().map(|x| {
            width_at_depth(*x, target_depth, cache, current_depth + 1)
        })
        .sum();
    cache.insert(key, result);
    result
}

fn main() {
    let input: Vec<u64> = vec![5910927, 0, 1, 47, 261223, 94788, 545, 7771];
    let map = &mut HashMap::new();
    for (i, depth) in [25, 75].iter().enumerate() {
        let now = Instant::now();
        let result: u64 = input.iter().map(|x| {
            width_at_depth(*x, *depth, map, 0)
        })
        .sum();
        let elapsed = now.elapsed();
        println!("Part {}: {}, Time: {}", i+1, result, elapsed.as_secs_f32())
    }

}
