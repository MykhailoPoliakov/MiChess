use super::*;

mod fill_dirty;
mod checks;


impl Game {
    // makes a move, returns bool
    pub fn play(&mut self, mv: Move) -> bool {
        let (start_pos, end_pos ) = mv;
        // checks if the move is legal
        if self.mode != GameMode::Active {
            println!("Move failed : wrong mode");
            return false;
        }
        if !self.board[start_pos].is_some_and(|p| p.color == self.player) {
            println!("Move failed : wrong start pos");
            return false;
        }
        if !self.legal[start_pos].get(end_pos) {
            println!("Move failed : wrong end pos");
            return false;
        };


        
        // get dirty moves
        self.get_dirty(mv);
        
        // saving history
        self.history.push(self.save());

        // MAKING THE MOVE

        // en passant
        let en_passant_copy = self.en_passant;
        self.en_passant = None;

        // saving played move
        let mut played = PlayedMove { mv, tp: MoveType::Basic, captured: self.board[end_pos]};

        let piece = self.board[start_pos].unwrap();
        match piece.role {
            Role::Pawn => {
                // play en passant
                if self.board[(start_pos.0, end_pos.1)] == Some(Piece{color: self.player.opp(), role: Role::Pawn}) &&
                Some(end_pos.1) == en_passant_copy {
                    self.board[(start_pos.0, end_pos.1)] = None;
                    played.captured = self.board[(start_pos.0, end_pos.1)];
                    played.tp = MoveType::EnPassant;
                }
                // create en passant possibility
                if (start_pos.0 - end_pos.0).abs() == 2 {
                    self.en_passant = Some(start_pos.1);
                }
            },
            Role::Rook => {
                // cancel castle
                match start_pos.1 {
                    0 => self.castle[piece.color as usize][0] = false,
                    7 => self.castle[piece.color as usize][1] = false,
                    _     => {},
                }
            },
            Role::King => {
                // make castle
                match mv {
                    ((7,4),(7,2)) => { 
                        self.board[(7,3)] = Some(Piece{color: self.player, role: Role::Rook}); 
                        self.board[(7,0)] = None;
                        played.tp = MoveType::Castle(((7,3), (7,0)));
                    },
                    ((7,4),(7,6)) => { 
                        self.board[(7,5)] = Some(Piece{color: self.player, role: Role::Rook}); 
                        self.board[(7,7)] = None;
                        played.tp = MoveType::Castle(((7,5), (7,7)));
                    },
                    ((0,4),(0,2)) => { 
                        self.board[(0,3)] = Some(Piece{color: self.player, role: Role::Rook}); 
                        self.board[(0,0)] = None; 
                        played.tp = MoveType::Castle(((0,3), (0,0)));
                    },
                    ((0,4),(0,6)) => { 
                        self.board[(0,5)] = Some(Piece{color: self.player, role: Role::Rook}); 
                        self.board[(0,7)] = None; 
                        played.tp = MoveType::Castle(((0,5), (0,7)));
                    },
                    _  => {},
                }
                // cancel castle
                self.castle[piece.color as usize] = [false,false];
            },
            _ => {}
        }

        // 50 move rule
        if self.board[end_pos].is_some() || piece.role == Role::Pawn {
            self.rule_50moves = 0;
        } else {
            self.rule_50moves += 1;
        }


        // possible promotion or basic move
        if piece.role == Role::Pawn && [0,7].contains(&end_pos.0) {
            self.board[end_pos] = Some(Piece{color: self.player, role: Role::Queen});
            self.board[start_pos] = None;
            played.tp = MoveType::Promotion;
        } else {
            self.board[end_pos] = Some(piece);
            self.board[start_pos] = None;
        }

        // saving played move
        self.played = Some(played);

        // change the player
        self.player = self.player.opp();
        // update info
        self.update();

        // check if move is legal, if not loads back up 
        let king_pos: Pos = self.king_pos[self.player.opp() as usize];
        if self.cover_comb[self.player as usize].get(king_pos) {
            self.undo();
            println!("Move failed : king in danger");
            return false;
        }
        
        // check for wins and draws
        self.check_check();
        self.win_check();
        self.draw_check();
        self.no_material_check();

        return true;
    }
}


    

