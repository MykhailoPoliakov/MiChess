use super::*;

impl Game {
    pub(super) fn update_pawn(&mut self, piece: Piece, pos: Pos) -> () {
        
        let direction: i8 = match piece.color { Color::White => -1, Color::Black =>  1 };

        if !valid_i8(pos.0 + direction) {
            return;
        }

        // cover
        for side in [1 as i8,-1 as i8] {
            let target = (pos.0 + direction, pos.1 + side);
            if valid_i8(target.1) {
                self.cover[pos].set(target);
            }
        }


        // one move ahead
        let target: Pos = (pos.0 + direction, pos.1);
        if self.board[target].is_none() {
            self.legal[pos].set(target);
            // two moves ahead
            let target: Pos = (pos.0 + direction*2, pos.1);
            if valid_i8(target.0) && self.board[target].is_none() &&
            match piece.color { Color::White => pos.0 == 6, Color::Black => pos.0 == 1 } {
                self.legal[pos].set(target);
            }
        }

        // capture
        for side in [1 as i8,-1 as i8] {
            let target: Pos = (pos.0 + direction, pos.1 + side);

            if valid_i8(target.1) &&
            self.board[target].is_some_and(|p| p.color == piece.color.opp()) {
                self.legal[pos].set(target);
            }
        }

        // en passant
        if match piece.color { Color::White => pos.0 == 3, Color::Black => pos.0 == 4 } {
            for side in [1 as i8,-1 as i8] {
                let target = (pos.0 + direction, pos.1 + side);

                if valid_i8(target.1) &&
                self.board[target].is_some_and(|p| p.color == piece.color.opp()) &&
                self.en_passant == Some(target.1) {
                    self.legal[pos].set(target);
                }
            }
        }
    }



    pub(super) fn update_knight(&mut self, piece: Piece, pos: Pos) -> () {
        for num in KNIGHT_MOVES {
            let target: Pos = (pos.0 + num.0, pos.1 + num.1);
            if valid(target) {
                // cover
                self.cover[pos].set(target);
                // legal
                if !self.board[target].is_some_and(|p| p.color == piece.color) {
                    self.legal[pos].set(target);
                }
            }
        }
    }



    pub(super) fn update_piece(&mut self, piece: Piece, pos: Pos, piece_moves: &[Pos]) -> () {
        for direction in piece_moves {
            for i in 1..8 {
                let target = (pos.0 + i*direction.0, pos.1 + i*direction.1);
                if valid(target) {
                    // cover 
                    self.cover[pos].set(target);
                    if self.board[target].is_some_and(|p| p.color == piece.color) {
                        break
                    }
                    // legal
                    self.legal[pos].set(target);
                    if self.board[target].is_some_and(|p| p.color == piece.color.opp() && p.role != Role::King) {
                        break
                    }
                }
            } 
        }
    }



    pub(super) fn update_king_cover(&mut self, pos: Pos) -> () {
        for num in KING_MOVES {
            let target = (pos.0 + num.0,pos.1 + num.1);
            if valid(target) {
                self.cover[pos].set(target);
            }
        }
    }


    
    pub(super) fn update_king_legal(&mut self, king_pos: Pos) -> () {
        // get variables
        let piece = self.board[king_pos].unwrap();
        let op_cover = self.cover_comb[piece.color.opp() as usize];
        
        // check all moves
        for num in KING_MOVES {
            let target = (king_pos.0 + num.0,king_pos.1 + num.1);
            if valid(target) {
                if !self.board[target].is_some_and(|p| p.color == piece.color) && 
                !op_cover.get(target) {
                    self.legal[king_pos].set(target);
                }
            }
        }

        // castle
        let row: i8 = match piece.color { Color::White => 7, Color::Black => 0 };

        if king_pos == (row, 4) {
            // left
            if self.castle[piece.color as usize][0] {
                if self.board[(row, 3)].is_none() && !op_cover.get((row, 3)) &&
                    self.board[(row, 2)].is_none() && !op_cover.get((row, 2)) &&
                    self.board[(row, 1)].is_none() && !op_cover.get((row, 1)) &&
                    self.board[(row, 0)] == Some(Piece{color: piece.color.clone(), role: Role::Rook}) {
                        self.legal[king_pos].set((row, 2));
                }
            } 
            // right
            if self.castle[piece.color as usize][1] {
                if self.board[(row, 5)].is_none() && !op_cover.get((row, 5)) &&
                    self.board[(row, 6)].is_none() && !op_cover.get((row, 6)) &&
                    self.board[(row, 7)] == Some(Piece{color: piece.color.clone(), role: Role::Rook}) {
                        self.legal[king_pos].set((row, 6));
                }
            }
        }
    }



}

