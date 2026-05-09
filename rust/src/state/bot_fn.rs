use super::Game;
use super::ALL_POS;

use crate::state::opponent;
use crate::state::play_fn::movement;

use rand::distributions::WeightedIndex;
use rand::prelude::*;

// const PINF: i32 =  10_000_000;
// const NINF: i32 = -10_000_000;

struct Debug {
    count: u64,
}




pub fn bot_play(game: &mut Game, max_depth: i8) {

    let init_player = game.player;
    let mut moves: Vec<( ((i8,i8),(i8,i8)) , i32 )> = Vec::new(); 

    // iterating through all legal moves
    for start_pos in ALL_POS {
        if game.board[start_pos.0 as usize][start_pos.1 as usize].0 == game.player { 
            for ref_end_pos in &game.legal[start_pos.0 as usize][start_pos.1 as usize] {
                let end_pos = *ref_end_pos;
                // create new game and make move if legal
                let new_game = & mut game.clone();
                if movement(new_game, &start_pos, &end_pos, false) {
                    // for every legal move
                    
                    // for debugging
                    let mut debug = Debug { count: 0 };

                    let value = deep_analyze(0, new_game, init_player, max_depth, &mut debug);
                    
                    moves.push(((start_pos, end_pos), value));


                    // for debugging
                    println!("---Move calculated : {:?}---", ((start_pos, end_pos), value));
                    println!("Amount of recursions : {:?}\n", debug.count);

                }
            }
        }
    }

    // make move
    let final_move = choose_move(&mut moves);
    movement(game, &final_move.0, &final_move.1, true);

    // console ouput
    println!("---------------------");
    println!("---Bot makes move!---");
    println!(" choosen move: {final_move:?}");
    println!("---------------------");
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



// broken, need fix
fn deep_analyze(depth: i8, game1: &mut Game, init_player: char, max_depth: i8, debug: & mut Debug) -> i32 {

    let mut opponent_moves: Vec<( ((i8,i8),(i8,i8)) , i32 )> = Vec::new(); 
    
    if game1.player == init_player {
        panic!("bot is broken")
    }

    // iterating through all legal opponent moves
    for op_start_pos in ALL_POS {
        if game1.board[op_start_pos.0 as usize][op_start_pos.1 as usize].0 == game1.player { 
            for rop_end_pos in &game1.legal[op_start_pos.0 as usize][op_start_pos.1 as usize] {
                let op_end_pos = *rop_end_pos;
                // create new game and make move if legal
                let game2 = &mut game1.clone();
                if movement(game2, &op_start_pos, &op_end_pos, false) {
                    // for every position
    
                    let mut player_moves:   Vec<( ((i8,i8),(i8,i8)) , i32 )> = Vec::new(); 


                    // iterating through all legal player moves
                    for pl_start_pos in ALL_POS {
                        if game2.board[pl_start_pos.0 as usize][pl_start_pos.1 as usize].0 == game2.player { 
                            for rpl_end_pos in &game2.legal[pl_start_pos.0 as usize][pl_start_pos.1 as usize] {
                                let pl_end_pos = *rpl_end_pos;
                                // create new game and make move if legal
                                let game3 = &mut game2.clone();
                                if movement(game3, &pl_start_pos, &pl_end_pos, false) {
                                    // for every position

                                    //debug
                                    debug.count += 1;

                                    let (mut player_value, verdict) = calculate(game3, init_player);
                                    if verdict && depth <= max_depth {
                                        player_value = deep_analyze(depth + 1, game3, init_player, max_depth, debug);
                                    }



                                    player_moves.push(((pl_start_pos, pl_end_pos), player_value));
                                }
                            }
                        }
                    }




                    let opponent_value = player_moves.iter().max_by_key(|x| x.1).unwrap().1;
                    opponent_moves.push(((op_start_pos, op_end_pos), opponent_value));
                }
            }
        }
    }

    let result = opponent_moves.iter().min_by_key(|x| x.1).unwrap().1;
    return result
}



// calculate position worth
fn calculate(game: &Game, init_player: char) -> (i32,bool) {
    let mut value = 0;

    // calculate basic piece amount
    value += (player_worth(&game.board, init_player) - player_worth(&game.board, opponent(init_player))) * 1000;
    
    return (value,true);
}




// get how much a player`s all pieces worth
fn player_worth(board: &[[(char,char);8];8], player: char) -> i32 {
    let mut value: i32 = 0;
    // iterate through all pieces
    for place in ALL_POS {
        if board[place.0 as usize][place.1 as usize].0 == player {
            value += piece_worth(board[place.0 as usize][place.1 as usize]);
        }
    }   
    return value;
}


// get how much a piece worth
fn piece_worth(piece: (char,char)) -> i32 {
    match piece.1 {
        'p' => return 1,
        'b'|'h' => return 3,
        'r' => return 5,
        'q' => return 9,
        'k' => return 100,
            _  => return 0,
    }
}