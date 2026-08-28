use super::*;




pub fn deeper_player(game: &Game, init_player: Color) -> bool { 
    true 
}

pub fn deeper_opponent(game: &Game, init_player: Color) -> bool { 
    true 
}


// calculate position worth
pub fn evaluate(game: &Game) -> i32 {
    let mut value = 0;

    let pl_king = game.king_pos[game.player as usize];
    let op_king = game.king_pos[game.player.opp() as usize];

    for pos in ALL_POS {

        if let Some(piece) = game.board[pos] {
            let worth = piece_worth(piece);

            if piece.color == game.player {
                value += worth * 1000;
                value += game.legal[pos].count() * 5;
                value += game.cover[pos].count() * 5;

                if game.cover_comb[game.player as usize].get(pos) {
                    value += 100;
                }

                if game.cover_comb[game.player.opp() as usize].get(pos) {
                    value -= 500;
                }

            } else {
                value -= worth * 1000;
                value -= game.legal[pos].count() * 5;
                value += game.cover[pos].count() * 5;

                if game.cover_comb[game.player.opp() as usize].get(pos) {
                    value -= 100;
                }

                if game.cover_comb[game.player as usize].get(pos) {
                    value += 500;
                }

            }
        }
            

            // material amount
            


            // // lost pieces
            // if game.cover_comb[game.player as usize].get(place) {
            //     // if attacked and not defended
            //     if !game.cover_comb[game.player.opp() as usize].get(place) {
            //         value -= current_piece_worth * 1000;
            //     // if attacked and defended
            //     } else {
            //         // game simulation
            //         let mut pl_points: Vec<i32> = Vec::new();
            //         let mut op_points: Vec<i32> = Vec::new();
                    
            //         for &cover_piece in &game.cover(game.player)[place] {
            //             op_points.push(piece_worth(game.board[cover_piece].unwrap()));
            //         }
            //         for &cover_piece in &game.cover(game.player.opp())[place] {
            //             pl_points.push(piece_worth(game.board[cover_piece].unwrap()));
            //         }

            //         pl_points.sort_by(|a, b| b.cmp(a));
            //         op_points.sort_by(|a, b| b.cmp(a));

            //         let mut current: i32 = current_piece_worth;
            //         let mut points: i32 = 0;
                
            //         loop {

            //             points -= current;
            //             current = op_points.pop().unwrap();
            //             if pl_points.is_empty() {
            //                 if points < 0 {
            //                     value += points * 1000;
            //                 }
            //                 break;
            //             }
                        
            //             points += current;
            //             current = pl_points.pop().unwrap();
            //             if op_points.is_empty() {
            //                 if points < 0 {
            //                     value += points * 1000;
            //                 }
            //                 break;
            //             }

            //             if points < 0 {
            //                 value += points * 1000;
            //                 break;
            //             }
            //         }
            //     }
            // }


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