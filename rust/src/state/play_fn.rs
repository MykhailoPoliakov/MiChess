use super::game::*;





// makes a move, returns bool
pub fn play(game: &mut Game, mv: Move, save: bool) -> bool {
    let (start_pos, end_pos ) = mv;
    // checks if the move is legal
    if game.mode != GameMode::Active {
        return false;
    }
    if !game.board[start_pos].is_some_and(|p| p.color == game.player) {
        return false;
    }
    if !game.legal[start_pos].contains( &end_pos ) {
        return false;
    };

    
    // saving for back_up
    let log: GameLog = game.save();

    // MAKING THE MOVE

    // en passant
    game.en_passant = None;


    let piece = game.board[start_pos].unwrap();
    match piece.role {
        Role::Pawn => {
            // play en passant
            if game.board[(start_pos.0, end_pos.1)] == Some(Piece{color: game.player.opp(), role: Role::Pawn}) &&
            Some(end_pos.1) == log.en_passant {
                game.board[(start_pos.0, end_pos.1)] = None;
            }
            // create en passant possibility
            if (start_pos.0 - end_pos.0).abs() == 2 {
                game.en_passant = Some(start_pos.1);
            }
        },
        Role::Rook => {
            // cancel castle
            match start_pos.1 {
                0 => game.castle[piece.color as usize][0] = false,
                7 => game.castle[piece.color as usize][1] = false,
                _     => {},
            }
        },
        Role::King => {
            // make castle
            match mv {
                ((7,4),(7,2)) => { 
                    game.board[(7,3)] = Some(Piece{color: game.player, role: Role::Rook}); 
                    game.board[(7,0)] = None 
                },
                ((7,4),(7,6)) => { 
                    game.board[(7,5)] = Some(Piece{color: game.player, role: Role::Rook}); 
                    game.board[(7,7)] = None 
                },
                ((0,4),(0,2)) => { 
                    game.board[(0,3)] = Some(Piece{color: game.player, role: Role::Rook}); 
                    game.board[(0,0)] = None 
                },
                ((0,4),(0,6)) => { 
                    game.board[(0,5)] = Some(Piece{color: game.player, role: Role::Rook}); 
                    game.board[(0,7)] = None 
                },
                _  => {},
            }
            // cancel castle
            game.castle[piece.color as usize] = [false,false];
        },
        _ => {}
    }

    // 50 move rule
    if game.board[end_pos].is_some() || piece.role == Role::Pawn {
        game.rule_50moves = 0;
    } else {
        game.rule_50moves += 1;
    }

    // possible promotion or basic move
    if piece.role == Role::Pawn && [0,7].contains(&end_pos.0) {
        game.board[end_pos] = Some(Piece{color: game.player, role: Role::Queen});
        game.board[start_pos] = None;
    } else {
        game.board[end_pos] = Some(piece);
        game.board[start_pos] = None;
    }

    // change the player
    game.player = game.player.opp();
    // update info
    game.update();


    // check if move is legal, if not loads back up 
    let king_pos: Pos = game.king_pos[game.player.opp() as usize];
    if !game.cover(game.player)[king_pos].is_empty() {
        game.load(log);
        game.update();
        return false;
    }

    
    // check for wins and draws
    check_check( game );
    win_check( game );
    draw_check( game );
    no_material_check( game );


    // saving move history if needed
    if save {
        //
    }

    return true;
}



// Changes : game.check
fn check_check(game: &mut Game) -> () {
    let king_pos = game.king_pos[game.player as usize];
    game.check = !game.cover(game.player.opp())[king_pos].is_empty()
}



// Changes : game.mode
fn win_check(game: &mut Game) -> () {
    if !game.check {
        return;
    }

    let king_pos = game.king_pos[game.player as usize];
    if !game.legal[king_pos].is_empty() {
        return;
    }

    let log = game.save();

    let legal_moves = game.moves[game.player as usize].clone();
    for mv in legal_moves {

        game.board[mv.1] = game.board[mv.0];
        game.board[mv.0] = None;
        game.update();

        if game.cover(game.player.opp())[king_pos].is_empty() {
            game.load(log);
            game.update();
            return;
        }

        game.load(log.clone());
    }
    game.mode = GameMode::Finished(Some(game.player.opp()));
}


// Changes : game.mode
fn draw_check(game: &mut Game) -> () {
    // 50 move rule
    if game.rule_50moves > 100 {
        game.mode = GameMode::Finished(None);
        return;
    }
    
    // stalemate
    if !game.check {
        for pos in ALL_POS {
            if game.board[pos].is_some_and(|p| p.color == game.player) &&
            !game.legal[pos].is_empty() {
                return;
            }
        }
        game.mode = GameMode::Finished(None);
        return;
    }
}


// Changes : game.mode
fn no_material_check(game: &mut Game) -> () {

    let mut w_material: i8 = 0;
    let mut b_material: i8 = 0;

    for place in ALL_POS {
        match game.board[place] {
            WB | WH => w_material += 1,
            BB | BH => b_material += 1,
            WK | BK | __ => (),
            _         =>  { return }
        }
    }
    if w_material == 0 && b_material <= 1 || w_material <= 1 && b_material == 0 {
        game.mode = GameMode::Finished(None);
        return;
    }
}

