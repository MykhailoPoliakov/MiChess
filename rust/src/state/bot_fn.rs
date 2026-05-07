use super::Game;
use super::State;
use super::ALL_POS;

//use rand::prelude::*;

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
                
                // make next move
                let mut new_game = game.clone();
                if self.movement(&mut new_game, &start_pos, &end_pos, false) == false {
                    continue;
                }
                
                let value: i32;
                let result = self.analyze_game(&mut new_game, init_player);
                if result.1 && 1 <= max_depth {
                    value = self.bot_recursion(game, 1, max_depth, init_player);
                } else {
                    value = result.0;
                }

                moves.push(((start_pos, end_pos), value))

              
            }
        }
        
        // making a move for bot
        let result = moves.iter().max_by_key(|x| x.1).unwrap().0;
        self.movement(game, &result.0, &result.1, true);

        // for testing
        println!(" bot makes move");
        println!(" bot moves : {moves:?}");
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
                    let result = self.analyze_game(&mut new_game, init_player);
                    if result.1 && (depth+1) <= max_depth {
                        println!("start recursion : depth : {depth}, player : player");
                        value = self.bot_recursion(game, depth + 1, max_depth, init_player);
                    } else {
                        println!("end station, depth : {depth}, player : player");
                        value = result.0;
                    }

                } else {
                    println!("start recursion : depth : {depth}, player : opponent");
                    value = self.bot_recursion(game, depth, max_depth, init_player);
                }
                
                values.push( value );
            }    
        }

        
        if game.player == init_player {
            return *values.iter().max().unwrap();
        } else {
            return *values.iter().min().unwrap();
        }
    }



    fn analyze_game(&mut self, game: &mut Game, init_player: char) -> (i32,bool) {
        let mut value = 0;
        let mut next: bool = false;

        let op_king_pos = ALL_POS.iter().find(|&p| game.board[p.0 as usize][p.1 as usize] == (game.opponent, 'k')).unwrap();
        let pl_king_pos = ALL_POS.iter().find(|&p| game.board[p.0 as usize][p.1 as usize] == (game.player, 'k')).unwrap();

        // if game was stopped
        match game.mode {
            'd' => return (0, false),
            'w' => if init_player == 'w' { return ( PINF, false); } else { return ( NINF, false); },
            'b' => if init_player == 'b' { return ( PINF, false); } else { return ( NINF, false); },
             _  => (), 
        }
        // material
        value += (self.player_worth( &game.board, init_player) - self.player_worth( &game.board, self.opponent(init_player))) * 1000;

        // check
        if game.check {
            value += 100;
            next = true;
        }

        // potential material
        for place in ALL_POS {

            let worth = self.piece_worth( game.board[place.0 as usize][place.1 as usize] );

            // if pieces are hanging
            if !game.pl_cover()[place.0 as usize][place.1 as usize].is_empty() && game.board[place.0 as usize][place.1 as usize].0 == game.opponent {
                value -= 10;
                // if it is not protected
                if game.op_cover()[place.0 as usize][place.1 as usize].is_empty() {
                    value -= worth * 1000;
                    next = true;
                } else {
                // if it is weak protected
                    if game.pl_cover()[place.0 as usize][place.1 as usize].len() > game.op_cover()[place.0 as usize][place.1 as usize].len() {
                        value -= worth * 1000;
                        next = true;
                    }
                }
            }                
            
            // moving closer to king
            if game.board[place.0 as usize][place.1 as usize].0 == game.opponent {
                value += (7 - ((place.0 - pl_king_pos.0) as i32).abs()) * worth;
                value += (7 - ((place.1 - pl_king_pos.1) as i32).abs()) * worth;
            }
            if game.board[place.0 as usize][place.1 as usize].0 == game.player {
                value -= (7 - ((place.0 - op_king_pos.0) as i32).abs()) * worth;
                value -= (7 - ((place.1 - op_king_pos.1) as i32).abs()) * worth;
            }

        
        }

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