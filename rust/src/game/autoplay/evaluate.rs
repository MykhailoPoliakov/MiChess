use super::*;




pub fn deeper_player(game: &Game, init_player: Color) -> bool { 
    true 
}

pub fn deeper_opponent(game: &Game, init_player: Color) -> bool { 
    true 
}


// calculate position worth
pub fn evaluate(game: &Game) -> i32 {
    return 0;
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