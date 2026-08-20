pub use super::game::*;

use rand::distributions::WeightedIndex;
use rand::prelude::*;

mod analyze;
use analyze::{analyze};
mod evaluate;



struct Config {
    init_player: Color,
    max_depth: i8
}

struct MoveInfo {
    liquidity: i8,
    depth: i8,
    way: Vec<Move>,
}




pub fn autoplay(real_game: &mut Game, max_depth: i8) -> () {
    let game = &mut real_game.clone(); // clone for safety

    let mut iterated = 0;

    let config = Config {
        init_player: game.player,
        max_depth,
    };

    let mut moves: Vec<(Move, i32)> = Vec::new(); 

    // iterating through all legal moves
    for &mv in &real_game.moves[real_game.player as usize] {

        if game.play(mv) {
            // get value for every legal move

            let move_info = MoveInfo {
                liquidity: 2,
                depth: 0,
                way: vec![mv],
            };

            let value = analyze(&config, game, &move_info, &mut iterated);
            moves.push((mv, value));
            game.undo();

        } 
    }

    // make move
    let chosen_move = choose_move(&mut moves);
    real_game.play(chosen_move);

    // console ouput
    println!("\nIteratrions done : {}", iterated);
    println!("\n---Bot makes move!---\nchosen move: {chosen_move:?}\n");
}



// chooses move aut of all given moves
fn choose_move( moves: &mut Vec<( ((i8,i8),(i8,i8)) , i32 )> ) -> ((i8,i8),(i8,i8)) {

    // sort by weight
    moves.sort_by_key(|x| std::cmp::Reverse(x.1));

    println!("Sorted moves : {moves:?}");

    // for rand function
    let mut choices: Vec<((i8,i8),(i8,i8))> = Vec::new();
    let mut weights: Vec<i32> = Vec::new();

    let mut max_weight: i32 = moves[0].1;
    println!("max weight : {max_weight:?}");

    let mut level: i32 = 0;

    for themove in moves {
        choices.push(themove.0);


        if themove.1 < max_weight {
            level += 1;
            max_weight = themove.1;
        }

        let weight: i32;
        match level {
            0 => weight = 1000,
            1 => weight = 10,
            _ => weight = 1,
        }

        weights.push(weight);
    }

    println!("--Choose move result : --");
    println!("{:?}",choices);
    println!("{:?}",weights);

    let dist = WeightedIndex::new(&weights).unwrap();
    let mut rng = thread_rng();

    let chosen_move = choices[dist.sample(&mut rng)];

    return chosen_move
}





fn _print_visual_horisontal() {
    println!("\n          Autoplay");
    println!("{}{}{}", "┌───","───┬───".repeat(18), "───┐" );
}




