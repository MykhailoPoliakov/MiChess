use super::super::game::*;




pub fn deeper_player(game: &Game, init_player: Color) -> bool { 
    true 
}

pub fn deeper_opponent(game: &Game, init_player: Color) -> bool { 
    true 
}


// calculate position worth
pub fn evaluate(game: &Game) -> i32 {
    let mut value = 0;

    let init_player = game.player.opp();
    let init_opponent = game.player;

    let pl_king = game.king_pos[init_player as usize];
    let op_king = game.king_pos[init_opponent as usize];

    for place in ALL_POS {

        // init_player pieces 
        if let Some(piece) = game.board[place] &&
        piece.color == init_player {
            let current_piece_worth = piece_worth(piece);

            // material amount
            value += current_piece_worth * 1000;


            // lost pieces
            if !game.cover(game.player)[place].is_empty() {
                // if attacked and not defended
                if game.cover(game.player.opp())[place].is_empty() {
                    value -= current_piece_worth * 1000;
                // if attacked and defended
                } else {
                    // game simulation
                    let mut pl_points: Vec<i32> = Vec::new();
                    let mut op_points: Vec<i32> = Vec::new();
                    
                    for &cover_piece in &game.cover(game.player)[place] {
                        op_points.push(piece_worth(game.board[cover_piece].unwrap()));
                    }
                    for &cover_piece in &game.cover(game.player.opp())[place] {
                        pl_points.push(piece_worth(game.board[cover_piece].unwrap()));
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
            for _ in &game.cover(game.player)[place] {
                value += 10; 
            }

            // how many threats
            for _ in &game.cover(game.player.opp())[place] {
                value -= 10; 
            }
            
            // more possible moves
            if game.legal[place].is_empty() {
                value -= current_piece_worth * 100;
            } else {
                value += 5*(game.legal[place].len() as i32);
            }




        // init_opponent pieces
        } else if let Some(piece) = game.board[place] &&
        piece.color == init_opponent {
            let current_piece_worth = piece_worth(piece);

            // material amount
            value -= current_piece_worth * 1000;



        }
    }
    
    return value;
}




// get how much a player`s all pieces worth
fn player_worth(board: &[[Option<Piece>;8];8], player: Color) -> i32 {
    let mut value: i32 = 0;
    // iterate through all pieces
    for place in ALL_POS {
        if let Some(piece) = board[place.0 as usize][place.1 as usize] {
            if piece.color == player {
                value += piece_worth(piece);
            }
        }
    }   
    return value;
}


// get how much a piece worth
fn piece_worth(piece: Piece) -> i32 {
    match piece.role {
        Role::Pawn   =>  1,
        Role::Knight =>  3,
        Role::Bishop =>  5,
        Role::Rook   =>  3,
        Role::Queen  =>  9,
        Role::King   => 12,
    }
}