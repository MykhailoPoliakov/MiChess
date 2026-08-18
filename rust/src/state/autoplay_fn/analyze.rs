use super::super::game::*;
use super::play;

use super::evaluate::{evaluate, deeper_opponent, deeper_player};
use super::{Config, MoveInfo};


const PINF: i32 =  10_000_000;
const NINF: i32 = -10_000_000;



pub fn analyze_opponent(config: &Config, game: &Game, old_move_info: &MoveInfo) -> i32 {

    let mut moves: Vec<( ((i8,i8),(i8,i8)) , i32 )> = Vec::new(); 

    println!("started analyzing opponent");

    // start iteration
    for start_pos in ALL_POS {
        if game.board[start_pos].is_some_and(|p| p.color == game.player) { 
            continue;
        }
        for &end_pos in &game.legal[start_pos] {

            // make imaginary move
            let new_game = &mut game.clone();
            if play(new_game, start_pos, end_pos, false) {
                // if move is legal

                // if game is finished
                let status = status_check(&new_game.mode, config.init_player);
                if status != 0 {
                    moves.push(((start_pos, end_pos), status));
                    continue;
                }

                // if game continues
                let deeper = deeper_opponent(game, config.init_player);

                if deeper || moves.is_empty() {
                    let mut way = old_move_info.way.clone();
                    way.push((start_pos, end_pos));
                    let move_info = MoveInfo {
                        liquidity: old_move_info.liquidity,
                        depth: old_move_info.depth + 1,
                        way,
                    };


                    let value = analyze_player(config, new_game, &move_info);
                    moves.push(((start_pos, end_pos), value));
                }
            }
        }
    };

    // choose worst player outcome
    let chosen_move = moves.iter().min_by_key(|x| x.1).unwrap().1;
    return chosen_move
}







pub fn analyze_player(config: &Config, game: &Game, old_move_info: &MoveInfo) -> i32 {
    let mut moves: Vec<( ((i8,i8),(i8,i8)) , i32 )> = Vec::new(); 

    println!("started analyzing player");

    // start iteration
    for start_pos in ALL_POS {
        if game.board[start_pos].is_some_and(|p| p.color == game.player) { 
            continue;
        } 
        for &end_pos in &game.legal[start_pos] {

            // make imaginary move
            let new_game = &mut game.clone();

            if play(new_game, start_pos, end_pos, false) {
                // if move is legal

                // if game is finished
                let status = status_check(&new_game.mode, config.init_player);
                if status != 0 {
                    moves.push(((start_pos, end_pos), status));
                    continue;
                }

                // if game continues
                let deeper = deeper_player(game, config.init_player);
                let value: i32;

                // go deeper if needed
                if deeper && (old_move_info.depth < config.max_depth) {

                    let mut way = old_move_info.way.clone();
                    way.push((start_pos, end_pos));
                    let move_info = MoveInfo {
                        liquidity: old_move_info.liquidity,
                        depth: old_move_info.depth + 1,
                        way,
                    };

                    value = analyze_opponent(config, new_game, &move_info);
                } else {
                    value = evaluate(game);
                }

                // save move info
                moves.push(((start_pos, end_pos), value));

            }
        }
    };

    // choose best player move
    let chosen_move = moves.iter().max_by_key(|x| x.1).unwrap().1;
    return chosen_move
}




// check if game is runnig or it is finished
fn status_check( mode: &GameMode, init_player: Color ) -> i32 {
    match mode {
        &GameMode::Active | &GameMode::Finished(None) => 0,
        &GameMode::Finished(Some(value)) => { if value == init_player { PINF } else { NINF }}
    }
}