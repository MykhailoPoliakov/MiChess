use super::Game;
use super::State;
use super::ALL_POS;

const PINF: i32 =  10_000_000;
const NINF: i32 = -10_000_000;

impl State {

    pub fn bot_play(&mut self, game: &mut Game, max_depth: i8) -> () {
        
        let init_player = game.player;
        let mut moves: Vec<(((i8,i8),(i8,i8)),i32)> = Vec::new(); 

        // for every legal move
        for start_pos in ALL_POS {
            if game.board[start_pos.0 as usize][start_pos.1 as usize].0 != game.player { 
                continue; 
            }
            for end_pos in ALL_POS {
                if !game.legal[start_pos.0 as usize][start_pos.1 as usize].contains( &end_pos ) { 
                    continue; 
                }

                let value: i32;

                let mut new_game = game.clone();
                println!("test move");
                self.movement(&mut new_game, &start_pos, &end_pos, false);
                

                let result = self.analyze_game(&new_game, init_player);
                if result.1 && 1 <= max_depth {
                    value = self.bot_recursion(game, 1, max_depth, init_player);
                } else {
                    value = result.0;
                }

                moves.push(((start_pos, end_pos), value))

              
            }
        }
        
        // making a move for bot
        println!(" bot moves : {moves:?}");
        let result = moves.iter().max_by_key(|x| x.1).unwrap().0;
        self.movement(game, &result.0, &result.1, true);
        println!(" bot move : {result:?}");
    }



    fn bot_recursion(&mut self, game: &mut Game, depth: i8, max_depth: i8, init_player: char) -> i32 {

        let mut values: Vec<i32> = Vec::new();

        for start_pos in ALL_POS {
            if game.board[start_pos.0 as usize][start_pos.1 as usize].0 != game.player { 
                continue; 
            }
            for end_pos in ALL_POS {
                if !game.legal[start_pos.0 as usize][start_pos.1 as usize].contains( &end_pos ) { 
                    continue; 
                }

                // next move
                let mut new_game = game.clone();
                self.movement(&mut new_game, &start_pos, &end_pos, false);

                let value: i32;

                if game.player == init_player {
                    let result = self.analyze_game(&new_game, init_player);
                    if result.1 && (depth+1) <= max_depth {
                        value = self.bot_recursion(game, depth + 1, max_depth, init_player);
                    } else {
                        value = result.0;
                    }

                } else {
                    value = self.bot_recursion(game, depth, max_depth, init_player);
                }
                
                values.push( value );
            }    
        }

        println!("depth : {depth} values : {values:?}");
        if game.player == init_player {
            return *values.iter().max().unwrap() / depth as i32;
        } else {
            return *values.iter().min().unwrap() / depth as i32;
        }
    }



    fn analyze_game(&mut self, game: &Game, init_player: char) -> (i32,bool) {
        let mut value = 0;
        let mut next: bool = false;

        // if game was stopped
        match game.mode {
            'd' => return (0, false),
            'w' => if init_player == 'w' { return ( PINF, false); } else { return ( NINF, false); },
            'b' => if init_player == 'b' { return ( PINF, false); } else { return ( NINF, false); },
             _  => (), 
        }
        // possition evaluation
        value += (self.player_worth( &game.board, init_player) - self.player_worth( &game.board, self.opponent(init_player))) * 1000;

        // check
        if game.check {
            value += 100;
            next = true
        }

        // attacking the king

        // if possible to take

        // if need to protect




        






        return (value, next);
    }

    fn player_worth(&self, board: &[[(char,char);8];8], player: char) -> i32 {
        let mut value: i32 = 0;

        for place in ALL_POS {
            if board[place.0 as usize][place.1 as usize].0 == player {
                value += self.piece_worth(board[place.0 as usize][place.1 as usize]);
            }
        }   

        return value;
    }

    fn piece_worth(&self, piece: (char,char)) -> i32 {
        match piece.1 {
            'p' => return 1,
            'b'|'h' => return 3,
            'r' => return 5,
            'q' => return 9,
            'k' => return 100,
             _  => return 0,
        }
    }
}