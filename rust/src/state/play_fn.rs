use super::game::*;


impl Game {
    // makes a move, returns bool
    pub fn play(&mut self, mv: Move) -> bool {
        let (start_pos, end_pos ) = mv;
        // checks if the move is legal
        if self.mode != GameMode::Active {
            return false;
        }
        if !self.board[start_pos].is_some_and(|p| p.color == self.player) {
            return false;
        }
        if !self.legal[start_pos].contains( &end_pos ) {
            return false;
        };

        
        // saving for back_up
        let log: GameLog = self.save();

        // MAKING THE MOVE

        // en passant
        self.en_passant = None;


        let piece = self.board[start_pos].unwrap();
        match piece.role {
            Role::Pawn => {
                // play en passant
                if self.board[(start_pos.0, end_pos.1)] == Some(Piece{color: self.player.opp(), role: Role::Pawn}) &&
                Some(end_pos.1) == log.en_passant {
                    self.board[(start_pos.0, end_pos.1)] = None;
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
                        self.board[(7,0)] = None 
                    },
                    ((7,4),(7,6)) => { 
                        self.board[(7,5)] = Some(Piece{color: self.player, role: Role::Rook}); 
                        self.board[(7,7)] = None 
                    },
                    ((0,4),(0,2)) => { 
                        self.board[(0,3)] = Some(Piece{color: self.player, role: Role::Rook}); 
                        self.board[(0,0)] = None 
                    },
                    ((0,4),(0,6)) => { 
                        self.board[(0,5)] = Some(Piece{color: self.player, role: Role::Rook}); 
                        self.board[(0,7)] = None 
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
        } else {
            self.board[end_pos] = Some(piece);
            self.board[start_pos] = None;
        }

        // change the player
        self.player = self.player.opp();
        // update info
        self.update();


        // check if move is legal, if not loads back up 
        let king_pos: Pos = self.king_pos[self.player.opp() as usize];
        if !self.cover(self.player)[king_pos].is_empty() {
            self.undo();
            return false;
        }

        
        // check for wins and draws
        self.check_check();
        self.win_check();
        self.draw_check();
        self.no_material_check();


        // saving move history
        self.history.push(log);

        return true;
    }



    // Changes : self.check
    fn check_check(&mut self) -> () {
        let king_pos = self.king_pos[self.player as usize];
        self.check = !self.cover(self.player.opp())[king_pos].is_empty()
    }



    // Changes : self.mode
    fn win_check(&mut self) -> () {
        if !self.check {
            return;
        }

        let king_pos = self.king_pos[self.player as usize];
        if !self.legal[king_pos].is_empty() {
            return;
        }

        let log = self.save();

        let legal_moves = self.moves[self.player as usize].clone();
        for mv in legal_moves {

            self.board[mv.1] = self.board[mv.0];
            self.board[mv.0] = None;
            self.update();

            if self.cover(self.player.opp())[king_pos].is_empty() {
                self.load(log);
                self.update();
                return;
            }

            self.load(log.clone());
        }
        self.mode = GameMode::Finished(Some(self.player.opp()));
    }


    // Changes : self.mode
    fn draw_check(&mut self) -> () {
        // 50 move rule
        if self.rule_50moves > 100 {
            self.mode = GameMode::Finished(None);
            return;
        }
        
        // stalemate
        if !self.check {
            for pos in ALL_POS {
                if self.board[pos].is_some_and(|p| p.color == self.player) &&
                !self.legal[pos].is_empty() {
                    return;
                }
            }
            self.mode = GameMode::Finished(None);
            return;
        }
    }


    // Changes : self.mode
    fn no_material_check(&mut self) -> () {

        let mut w_material: i8 = 0;
        let mut b_material: i8 = 0;

        for place in ALL_POS {
            match self.board[place] {
                WB | WH => w_material += 1,
                BB | BH => b_material += 1,
                WK | BK | __ => (),
                _         =>  { return }
            }
        }
        if w_material == 0 && b_material <= 1 || w_material <= 1 && b_material == 0 {
            self.mode = GameMode::Finished(None);
            return;
        }
    }

}
