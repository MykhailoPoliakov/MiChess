pub use super::play_fn::play;
pub use super::game::*;

use rand::distributions::WeightedIndex;
use rand::prelude::*;

mod analyze;
use analyze::{analyze_opponent};
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




pub fn autoplay(game: &mut Game, max_depth: i8) -> () {

    let config = Config {
        init_player: game.player,
        max_depth,
    };

    let mut moves: Vec<(Move, i32)> = Vec::new(); 

    // iterating through all legal moves
    for start_pos in ALL_POS {
        if game.board[start_pos].is_some_and(|p| p.color == game.player) { 
            continue;
        }
        for &end_pos in &game.legal[start_pos] {
            // create new game and make move if legal
            let new_game = &mut game.clone();
            if play(new_game, start_pos, end_pos, false) {
                // get value for every legal move


                let mut way: Vec<((i8,i8),(i8,i8))> = vec![(start_pos, end_pos)];
                way.push((start_pos, end_pos));
                let move_info = MoveInfo {
                    liquidity: 2,
                    depth: 0,
                    way,
                };

                let value = analyze_opponent(&config, new_game, &move_info);

                moves.push(((start_pos, end_pos), value));

            } 
        }
    }

    // make move
    let chosen_move = choose_move(&mut moves);
    play(game, chosen_move.0, chosen_move.1, true);

    // console ouput
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





fn print_visual_horisontal() {
    println!("\n          Autoplay");
    println!("{}{}{}", "┌───","───┬───".repeat(18), "───┐" );
}




