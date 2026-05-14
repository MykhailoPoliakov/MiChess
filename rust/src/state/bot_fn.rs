use super::Game;
use super::ALL_POS;

use crate::state::play_fn::movement;

use rand::distributions::WeightedIndex;
use rand::prelude::*;

const PINF: i32 =  10_000_000;
const NINF: i32 = -10_000_000;




pub fn bot_play(game: &mut Game, max_depth: i8) {

    let init_player = game.player;
    let mut moves: Vec<( ((i8,i8),(i8,i8)) , i32 )> = Vec::new(); 

    // iterating through all legal moves
    for start_pos in ALL_POS {
        if game.board[start_pos.0 as usize][start_pos.1 as usize].0 == game.player { 
            for ref_end_pos in &game.legal[start_pos.0 as usize][start_pos.1 as usize] {
                let end_pos = *ref_end_pos;
                // create new game and make move if legal
                let new_game = &mut game.clone();
                if movement(new_game, &start_pos, &end_pos, false) {
                    // for every legal move

                    let value = analyze_opponent(0, new_game, init_player, max_depth);
                    moves.push(((start_pos, end_pos), value));

                }
            }
        }
    }

    // make move
    let chosen_move = choose_move(&mut moves);
    movement(game, &chosen_move.0, &chosen_move.1, true);

    // console ouput
    println!("---------------------");
    println!("---Bot makes move!---");
    println!(" chosen move: {chosen_move:?}");
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





fn analyze_opponent(depth: i8, game: &Game, init_player: char, max_depth: i8) -> i32 {
    let mut moves: Vec<( ((i8,i8),(i8,i8)) , i32 )> = Vec::new(); 

    println!("started analyzing opponent");

    // start iteration
    for start_pos in ALL_POS {
        if game.board[start_pos.0 as usize][start_pos.1 as usize].0 == game.player { 
            for r_end_pos in &game.legal[start_pos.0 as usize][start_pos.1 as usize] {
                let end_pos = *r_end_pos;

                // make imaginary move
                let new_game = &mut game.clone();
                if movement(new_game, &start_pos, &end_pos, false) {
                    // if move is legal

                    // if game is finished
                    let status = status_check(new_game.mode, init_player);
                    if status != 0 {
                        moves.push(((start_pos, end_pos), status));
                        continue;
                    }

                    // if game continues
                    let deeper = deeper_opponent(game, init_player);

                    if deeper || moves.is_empty() {
                        let value = analyze_player(depth, new_game, init_player, max_depth);
                        moves.push(((start_pos, end_pos), value));
                    }
                }
            }
        }
    };

    // choose worst player outcome
    let chosen_move = moves.iter().min_by_key(|x| x.1).unwrap().1;
    return chosen_move
}







fn analyze_player(depth: i8, game: &Game, init_player: char, max_depth: i8) -> i32 {
    let mut moves: Vec<( ((i8,i8),(i8,i8)) , i32 )> = Vec::new(); 

    println!("started analyzing player");

    // start iteration
    for start_pos in ALL_POS {
        if game.board[start_pos.0 as usize][start_pos.1 as usize].0 == game.player { 
            for r_end_pos in &game.legal[start_pos.0 as usize][start_pos.1 as usize] {
                let end_pos = *r_end_pos;

                // make imaginary move
                let new_game = &mut game.clone();
                if movement(new_game, &start_pos, &end_pos, false) {
                    // if move is legal

                    // if game is finished
                    let status = status_check(new_game.mode, init_player);
                    if status != 0 {
                        moves.push(((start_pos, end_pos), status));
                        continue;
                    }

                    // if game continues
                    let deeper = deeper_player(game, init_player);
                    let value: i32;

                    // go deeper if needed
                    if deeper && depth < max_depth {
                        value = analyze_opponent(depth + 1, new_game, init_player, max_depth);
                    } else {
                        value = evaluate(game);
                    }

                    // save move info
                    moves.push(((start_pos, end_pos), value));

                }
            }
        }
    };

    // choose best player move
    let chosen_move = moves.iter().max_by_key(|x| x.1).unwrap().1;
    return chosen_move
}




// check if game is runnig or it is finished
fn status_check( mode: char, init_player: char ) -> i32 {
    match mode {
        'd' => return 0,
        'w' => if init_player == 'w' { return PINF; } else { return NINF },
        'b' => if init_player == 'b' { return PINF; } else { return NINF },
         _  => 0, 
    }
}




fn deeper_player(game: &Game, init_player: char) -> bool { 
    true 
}

fn deeper_opponent(game: &Game, init_player: char) -> bool { 
    true 
}


// calculate position worth
pub fn evaluate(game: &Game) -> i32 {
    let mut value = 0;

    let init_player = game.opponent;
    let init_opponent = game.player;

    let pl_king = game.king_pos(init_player);
    let op_king = game.king_pos(init_opponent);

    for place in ALL_POS {

        // init_player pieces 
        if game.board[place.0 as usize][place.1 as usize].0 == init_player {
            let current_piece_worth = piece_worth(game.board[place.0 as usize][place.1 as usize]);

            // material amount
            value += current_piece_worth * 1000;


            // lost pieces
            if !game.pl_cover()[place.0 as usize][place.1 as usize].is_empty() {
                // if attacked and not defended
                if game.op_cover()[place.0 as usize][place.1 as usize].is_empty() {
                    value -= current_piece_worth * 1000;
                // if attacked and defended
                } else {
                    // game simulation
                    let mut pl_points: Vec<i32> = Vec::new();
                    let mut op_points: Vec<i32> = Vec::new();
                    
                    for piece in &game.pl_cover()[place.0 as usize][place.1 as usize] {
                        op_points.push(piece_worth(game.board[piece.0 as usize][piece.1 as usize]));
                    }
                    for piece in &game.op_cover()[place.0 as usize][place.1 as usize] {
                        pl_points.push(piece_worth(game.board[piece.0 as usize][piece.1 as usize]));
                    }

                    pl_points.sort_by(|a, b| b.cmp(a));
                    op_points.sort_by(|a, b| b.cmp(a));

                    let mut current: i32 = current_piece_worth;
                    let mut points: i32 = 0;
                
                    loop {

                        points -= current;
                        current = op_points.pop().unwrap();
                        if pl_points.is_empty() {
                            if points < 0 {
                                value += points * 1000;
                            }
                            break;
                        }
                        
                        points += current;
                        current = pl_points.pop().unwrap();
                        if op_points.is_empty() {
                            if points < 0 {
                                value += points * 1000;
                            }
                            break;
                        }

                        if points < 0 {
                            value += points * 1000;
                            break;
                        }
                    }
                }
            }



                
            
            // how many covers
            for _ in &game.op_cover()[place.0 as usize][place.1 as usize] {
                value += 10; 
            }

            // how many threats
            for _ in &game.pl_cover()[place.0 as usize][place.1 as usize] {
                value -= 10; 
            }
            
            // more possible moves
            if game.legal[place.0 as usize][place.1 as usize].is_empty() {
                value -= current_piece_worth * 100;
            } else {
                for _ in &game.legal[place.0 as usize][place.1 as usize] {
                    value += 5;
                }
            }




        // init_opponent pieces
        } else if game.board[place.0 as usize][place.1 as usize].0 == init_opponent {
            let current_piece_worth = piece_worth(game.board[place.0 as usize][place.1 as usize]);

            // material amount
            value -= current_piece_worth * 1000;



        }
    }
    
    return value;
}




// get how much a player`s all pieces worth
fn _player_worth(board: &[[(char,char);8];8], player: char) -> i32 {
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
        'k' => return 12,
            _  => return 0,
    }
}