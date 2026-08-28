use super::*;

use rand::prelude::*;


// chooses move aut of all given moves
pub fn choose_move( moves: &mut Vec<(Move, i32)> ) -> Move {
    let mut rng = rand::thread_rng();

    // sort by weight
    moves.sort_by_key(|mv_vl| std::cmp::Reverse(mv_vl.1));
    println!("Sorted moves : {moves:?}");

    let max_value = moves[0].1;
    let min_value = moves.last().unwrap().1;
    if max_value == min_value {
        return moves[rng.gen_range(0..moves.len()) as usize].0;
    }
    let mut sorted: Vec<(Move, f64)> = Vec::new();
    
    for mv_vl in moves {
        let coef: f64 = ((mv_vl.1 - min_value) as f64 / (max_value - min_value) as f64).powf(5.0);
        sorted.push((mv_vl.0, coef));
    }

    println!("Coef moves : {sorted:?}");
    let chosen = sorted.choose_weighted(&mut rng, |item| item.1).unwrap();

    return chosen.0
}

