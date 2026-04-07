use super::Game;
use super::State;
use super::ALL_POS;


impl State {
    
    pub fn play(&mut self, game: &mut Game, start_pos: (i8,i8), end_pos: (i8,i8) ) -> () {
        if self.check_move( game, &start_pos, &end_pos) {
            self.movement( game, &start_pos, &end_pos);
        } else {
            println!("Move was illigal on surface level")
        }
    }


    pub fn movement(&mut self, game: &mut Game, start_pos: &(i8,i8), end_pos: &(i8,i8)) ->  bool {

        // saving for back_up
        let save_game = game.clone();
        
        // make move
        println!("move was made");
        game.board[end_pos.0 as usize][end_pos.1 as usize] = game.board[start_pos.0 as usize][start_pos.1 as usize];
        game.board[start_pos.0 as usize][start_pos.1 as usize] = (' ',' ');

        // change the player
        self.player_change( game );

        // update info
        self.info( game , ' ');

        // checks for checks
        self.check_check( game );

        // check if move is legal, if not loads back up 
        if !self.check_move_deep( game ) {
            *game = save_game;
            println!("This move is illigal");
            return false; 
        }   
        // check for wins and draws
        self.win_check( game );
        self.draw_check( game );
        return true;
    }


    fn win_check(&mut self, game: &mut Game) -> () {

        if !game.check {
            return;
        }

        let king_pos = ALL_POS.iter().find(|&p| game.board[p.0 as usize][p.1 as usize] == (game.opponent, 'k')).unwrap();

        if game.legal[king_pos.0 as usize][king_pos.1 as usize] != [] {
            return;
        }

        for loc in ALL_POS {
            for place in &game.legal[loc.0 as usize][loc.1 as usize] {

                let mut test_game = game.clone();
                test_game.board[place.0 as usize][place.1 as usize] = test_game.board[loc.0 as usize][loc.1 as usize];
                test_game.board[loc.0 as usize][loc.1 as usize] = (' ',' ');
                self.info( &mut test_game , 'c');

                if test_game.op_cover()[king_pos.0 as usize][king_pos.1 as usize] == [] {
                    return;
                }
            }
        }

        game.mode = game.opponent;
        return;
    }

    fn draw_check(&mut self, game: &mut Game) -> () {


        // 50 move rule
        if game.moves_amount > 50 {
            game.mode = 'd';
            return;
        }

        // not enought material



        // stalemate
        if !game.check {
            for place in ALL_POS {
                if game.board[place.0 as usize][place.1 as usize].0 == game.player &&
                game.legal[place.0 as usize][place.1 as usize] != [] {
                    return;
                }
            }
            game.mode = 'd';
            return;
        }
    }


    fn check_check(&mut self, game: &mut Game) -> () {
        game.check = false;
        for place in ALL_POS {
            if game.board[place.0 as usize][place.1 as usize] == (game.opponent,'k') {
                if true {
                    game.check = true
                }
                return
            }
        }
    }


    fn player_change(&mut self, game: &mut Game) -> () {
        // changes the player
        std::mem::swap(&mut game.player, &mut game.opponent)
    }

    

    pub fn check_move_deep(&mut self, game: &mut Game ) -> bool {
        for place in ALL_POS {
            if game.board[place.0 as usize][place.1 as usize] == (game.player,'k') {
                if game.op_cover()[place.0 as usize][place.1 as usize] != [] {
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
            println!("1.1, {}" ,game.player);
            println!("1.2, {}" ,game.board[start_pos.0 as usize][start_pos.1 as usize].0);

            return false;
        };
        if !game.legal[start_pos.0 as usize][start_pos.1 as usize].contains( end_pos ) {
            println!("2.1 {:?}", game.legal[start_pos.0 as usize][start_pos.1 as usize]);
            println!("2.2 {:?}", end_pos);

            return false;
        }
        return true;
    }

}