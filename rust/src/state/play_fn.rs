use super::Game;
use super::State;
use super::ALL_POS;

// import info
use crate::state::info_fn::info;


impl State {
    
    // checks if the move is legal, returns bool
    pub fn check_move(&mut self, game: &Game, start_pos: &(i8,i8), end_pos: &(i8,i8)) -> bool {
        if game.board[start_pos.0 as usize][start_pos.1 as usize].0 != game.player     {return false;};
        if !game.legal[start_pos.0 as usize][start_pos.1 as usize].contains( end_pos ) {return false;};
        return true;
    }

    // makes a move, returns bool
    pub fn movement(&mut self, game: &mut Game, start_pos: &(i8,i8), end_pos: &(i8,i8), save: bool) -> bool {
        // saving for back_up
        let save_game = game.clone();

        // MAKING THE MOVE

        // en passant
        let en_passant_copy = game.en_passant;
        game.en_passant = -1;

        if game.board[start_pos.0 as usize][start_pos.1 as usize].1 == 'p' {
            // execute en passant
            if game.board[start_pos.0 as usize][end_pos.1 as usize] == (game.opponent,'p') && end_pos.1 == en_passant_copy {
                game.captured.push(game.board[start_pos.0 as usize][end_pos.1 as usize]);
                game.board[start_pos.0 as usize][end_pos.1 as usize] = (' ',' ');
            }
            // create en passant possibility
            if (start_pos.0 - end_pos.0).abs() == 2 {
                game.en_passant = start_pos.1;

            } 
        // castle for rook
        } else if game.board[start_pos.0 as usize][start_pos.1 as usize].1 == 'r' {
            match start_pos {
                (7,0) => game.castle[0][0] = false,
                (7,7) => game.castle[0][1] = false,
                (0,0) => game.castle[1][0] = false,
                (0,7) => game.castle[1][1] = false,
                _     => (),
            }
        // caslte for king 
        } else if game.board[start_pos.0 as usize][start_pos.1 as usize].1 == 'k' {
            match (start_pos, end_pos) {
                ((7,4),(7,2)) => { game.board[7][3] = (game.player, 'r') ; game.board[7][0] = (' ',' ') },
                ((7,4),(7,6)) => { game.board[7][5] = (game.player, 'r') ; game.board[7][7] = (' ',' ') },
                ((0,4),(0,2)) => { game.board[0][3] = (game.player, 'r') ; game.board[0][0] = (' ',' ') },
                ((0,4),(0,6)) => { game.board[0][5] = (game.player, 'r') ; game.board[0][7] = (' ',' ') },
                _             => (),
            }
            if game.player == 'w' {
                game.castle[0] = [false,false];
            } else {
                game.castle[1] = [false,false];
            }
        }

        // 50 move rule
        if game.board[end_pos.0 as usize][end_pos.1 as usize] != (' ',' ') {
            game.captured.push( game.board[end_pos.0 as usize][end_pos.1 as usize] );
            game.moves_amount = 0;
        } else {
            game.moves_amount += 1;
        }

        // possible promotion or basic move
        if game.board[start_pos.0 as usize][start_pos.1 as usize].1 == 'p' && [0,7].contains(&end_pos.0) {
            game.board[end_pos.0 as usize  ][end_pos.1 as usize  ] = ( game.player ,'q');
            game.board[start_pos.0 as usize][start_pos.1 as usize] = (' ',' ');
        } else {
            game.board[end_pos.0 as usize  ][end_pos.1 as usize  ] = game.board[start_pos.0 as usize][start_pos.1 as usize];
            game.board[start_pos.0 as usize][start_pos.1 as usize] = (' ',' ');
        }

        // MOVE WAS MADE

        // change the player
        std::mem::swap(&mut game.player, &mut game.opponent);

        // update info
        info( game );

        // checks for checks
        check_check( game );

        // check if move is legal, if not loads back up 
        let king_pos = ALL_POS.iter().find(|&p| game.board[p.0 as usize][p.1 as usize] == (game.opponent, 'k')).unwrap();
        if !game.pl_cover()[king_pos.0 as usize][king_pos.1 as usize].is_empty() {
            *game = save_game;
            return false;
        }

        // saving move history if needed
        if save {
            game.history.push(game.board.clone())
        }

        // check for wins and draws
        win_check( game );
        draw_check( game );
        no_material_check( game );

        return true;
    }
}


// Changes : game.mode
fn win_check(game: &mut Game) -> () {
    if !game.check {
        return;
    }

    let king_pos = ALL_POS.iter().find(|&p| game.board[p.0 as usize][p.1 as usize] == (game.player, 'k')).unwrap();

    if !game.legal[king_pos.0 as usize][king_pos.1 as usize].is_empty() {
        return;
    }
    for loc in ALL_POS {
        if game.board[loc.0 as usize][loc.1 as usize].0 != game.player {
            continue
        }
        for place in &game.legal[loc.0 as usize][loc.1 as usize] {

            let mut test_game = game.clone();
            test_game.board[place.0 as usize][place.1 as usize] = test_game.board[loc.0 as usize][loc.1 as usize];
            test_game.board[loc.0 as usize][loc.1 as usize] = (' ',' ');
            info( &mut test_game );

            if test_game.op_cover()[king_pos.0 as usize][king_pos.1 as usize].is_empty() {
                return;
            }
        }
    }
    game.mode = game.opponent;
}


// Changes : game.mode
fn draw_check(game: &mut Game) -> () {
    // 50 move rule
    if game.moves_amount > 50 {
        game.mode = 'd';
        return;
    }
    
    // stalemate
    if !game.check {
        for place in ALL_POS {
            if game.board[place.0 as usize][place.1 as usize].0 == game.player &&
            !game.legal[place.0 as usize][place.1 as usize].is_empty() {
                return;
            }
        }
        game.mode = 'd';
        return;
    }
}


// Changes : game.mode
fn no_material_check(game: &mut Game) -> () {

    let mut w_material: i8 = 0;
    let mut b_material: i8 = 0;

    for place in ALL_POS {
        match game.board[place.0 as usize][place.1 as usize] {
            ('w','b') | ('w','h') => w_material += 1,
            ('b','b') | ('b','h') => b_material += 1,
            ('w','k') | ('b','k') | (' ',' ') => (),
            _         =>  { return }
        }
    }
    if w_material == 0 && b_material <= 1 || w_material <= 1 && b_material == 0 {
        game.mode = 'd';
        return;
    }
}


// Changes : game.check
fn check_check(game: &mut Game) -> () {
    game.check = false;
    for place in ALL_POS {
        if game.board[place.0 as usize][place.1 as usize] == (game.player,'k') {
            if !game.op_cover()[place.0 as usize][place.1 as usize].is_empty() {
                game.check = true
            }
            return
        }
    }
}
