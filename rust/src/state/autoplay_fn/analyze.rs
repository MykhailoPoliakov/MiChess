use super::super::game::*;
use super::play;

use super::evaluate::{evaluate, deeper_opponent, deeper_player};
use super::{Config, MoveInfo};


// use std::thread;
// use std::time::Duration;

const PINF: i32 =  10_000_000;
const NINF: i32 = -10_000_000;



pub fn analyze(config: &Config, game: &mut Game, old_move_info: &MoveInfo, iterated: &mut i32) -> i32 {

    let mut moves: Vec<( ((i8,i8),(i8,i8)) , i32 )> = Vec::new(); 

    println!("started analyzing {}", game.player);

    let log = game.save();

    // start iteration
    let legal_moves = game.moves[game.player as usize].clone();
    for mv in legal_moves {
        game.load(log.clone());
        game.update();

        if play(game, mv, false) {
            *iterated += 1;
            // print board
            // println!("{}\nmove : {:?}\n{}", game.board, mv, old_move_info.depth + 1);
            // thread::sleep(Duration::from_millis(100)); 

            // PLAYER
            if game.player != config.init_player {

                // if game is finished
                let status = status_check(&mut game.mode, config.init_player);
                if status != 0 {
                    moves.push((mv, status));
                    continue;
                }

                // if game continues
                let deeper = deeper_player(game, config.init_player);
                let value: i32;

                // go deeper if needed
                if deeper && (old_move_info.depth < config.max_depth) {

                    let mut way = old_move_info.way.clone();
                    way.push(mv);
                    let move_info = MoveInfo {
                        liquidity: old_move_info.liquidity,
                        depth: old_move_info.depth + 1,
                        way,
                    };

                    value = analyze(config, game, &move_info, iterated);
                } else {
                    value = evaluate(game);
                }

                // save move info
                moves.push((mv, value));

            // OPONENT
            } else {

                // if game is finished
                let status = status_check(&game.mode, config.init_player);
                if status != 0 {
                    moves.push((mv, status));
                    continue;
                } 
                
                let deeper = deeper_opponent(game, config.init_player);

                if deeper || moves.is_empty() {
                    let mut way = old_move_info.way.clone();

                    way.push(mv);

                    let move_info = MoveInfo {
                        liquidity: old_move_info.liquidity,
                        depth: old_move_info.depth + 1,
                        way,
                    };

                    let value = analyze(config, game, &move_info, iterated);
                    moves.push((mv, value));
                }

            }

            
        }
    };

    // choose worst player outcome
    let chosen_move: i32;
    if game.player == config.init_player {
        chosen_move = moves.iter().max_by_key(|x| x.1).unwrap().1;
    } else {
        chosen_move = moves.iter().min_by_key(|x| x.1).unwrap().1;
    }

    
    return chosen_move
}




// check if game is runnig or it is finished
fn status_check( mode: &GameMode, init_player: Color ) -> i32 {
    match mode {
        &GameMode::Active | &GameMode::Finished(None) => 0,
        &GameMode::Finished(Some(value)) => { if value == init_player { PINF } else { NINF }}
    }
}