use super::Game;
use super::State;
use super::ALL_POS;


impl State {
    
    pub fn play(&mut self, game: &mut Game, start_pos: (i8,i8), end_pos: (i8,i8) ) -> () {
        if self.check_move( game, &start_pos, &end_pos) {
            self.movement( game, &start_pos, &end_pos, true);
        } else {
            println!("Move was illigal on surface level")
        }
    }


    pub fn movement(&mut self, game: &mut Game, start_pos: &(i8,i8), end_pos: &(i8,i8), save: bool) -> () {
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
        self.info( game );

        // checks for checks
        self.check_check( game );

        // check if move is legal, if not loads back up 
        if !self.check_move_deep( game ) {
            *game = save_game;
            println!("This move is illigal");
            return;
        }   

        // saving move history if needed
        if save {
            game.history.push(game.board.clone())
        }

        // check for wins and draws
        self.win_check( game );
        self.draw_check( game );
    }



    fn win_check(&mut self, game: &mut Game) -> () {
        if !game.check {
            return;
        }
        let king_pos = ALL_POS.iter().find(|&p| game.board[p.0 as usize][p.1 as usize] == (game.opponent, 'k')).unwrap();

        if game.legal[king_pos.0 as usize][king_pos.1 as usize] != [] {
            return;
        }
        println!("win check activates info");
        for loc in ALL_POS {
            for place in &game.legal[loc.0 as usize][loc.1 as usize] {

                let mut test_game = game.clone();
                test_game.board[place.0 as usize][place.1 as usize] = test_game.board[loc.0 as usize][loc.1 as usize];
                test_game.board[loc.0 as usize][loc.1 as usize] = (' ',' ');
                self.info( &mut test_game );

                if test_game.op_cover()[king_pos.0 as usize][king_pos.1 as usize].is_empty() {
                    return;
                }
            }
        }
        game.mode = game.opponent;
    }



    fn draw_check(&mut self, game: &mut Game) -> () {
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

        // not enought material
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



    fn check_check(&mut self, game: &mut Game) -> () {
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

        

    pub fn check_move_deep(&mut self, game: &mut Game ) -> bool {
        for place in ALL_POS {
            if game.board[place.0 as usize][place.1 as usize] == (game.player,'k') {
                if !game.op_cover()[place.0 as usize][place.1 as usize].is_empty() {
                    println!("Does nor pass the deep check.");
                    return false;
                }
            }
        }
        return true;
    }



    pub fn check_move(&mut self, game: &mut Game, start_pos: &(i8,i8), end_pos: &(i8,i8)) -> bool {
        // checks for not legal moves
        if game.board[start_pos.0 as usize][start_pos.1 as usize].0 != game.player {
            return false;
        };
        if !game.legal[start_pos.0 as usize][start_pos.1 as usize].contains( end_pos ) {
            return false;
        }
        return true;
    }
}