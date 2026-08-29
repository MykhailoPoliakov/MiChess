use super::*;

impl Game {
    pub(super) fn update_pawn(&mut self, piece: Piece, pos: Pos, enemy_pieces: BitBoard) -> () {

        let direction: i8 = match piece.color { Color::White => -1, Color::Black =>  1 };

        // cover
        let attacks = PAWN_ATTACKS[piece.color as usize][pos];
        self.cover[pos].0 |= attacks.0;

        // one move ahead
        let target = (pos as i8 + direction*8) as u8;
        if self.board[target].is_none() {
            self.legal[pos].set(target);

            // two moves ahead
            if match piece.color { Color::White => pos >= 48, Color::Black => pos < 16 } {
                let target = (pos as i8 + direction*8*2) as u8;
                if self.board[target].is_none() {
                    self.legal[pos].set(target);
                }
            }
        }

        // capture
        let attacks = PAWN_ATTACKS[piece.color as usize][pos];
        self.legal[pos].0 |= attacks.0 & enemy_pieces.0;

        // en passant
        if let Some(ep_col) = self.en_passant {
            if match piece.color {Color::White => (pos / 8) as i8 == 3, Color::Black => (pos / 8) as i8 == 4} {
                let target = match piece.color { Color::White => 2*8, Color::Black => 5*8 } + ep_col as u8;
                if PAWN_ATTACKS[piece.color as usize][pos].get(target) {
                    self.legal[pos].set(target);
                }
            }
        }
    }



    pub(super) fn update_knight(&mut self, pos: Pos, friendly_pieces: BitBoard) -> () {
        let attacks = KNIGHT_ATTACKS[pos];
        self.cover[pos].0 |= attacks.0;
        self.legal[pos].0 |= attacks.0 & !friendly_pieces.0;
    }



    pub(super) fn update_rook(&mut self, pos: Pos, pieces: [BitBoard;2], color: Color) -> () {
        for dir in 0..4 {
            for &end_pos in &ROOK_RAYS[pos as usize][dir] {
                if end_pos == 64 {break ;} // if out of bounds
                self.cover[pos].set(end_pos);
                if pieces[color as usize].get(end_pos) { break; };
                self.legal[pos].set(end_pos);
                if pieces[color.opp() as usize].get(end_pos) { break; };
            }
        } 
    }



    pub(super) fn update_bishop(&mut self, pos: Pos, pieces: [BitBoard;2], color: Color) -> () {
        for dir in 0..4 {
            for &end_pos in &BISHOP_RAYS[pos as usize][dir] {
                if end_pos == 64 {break ;} // if out of bounds
                self.cover[pos].set(end_pos);
                if pieces[color as usize].get(end_pos) { break; };
                self.legal[pos].set(end_pos);
                if pieces[color.opp() as usize].get(end_pos) { break; };
            }
        } 
    }



    pub(super) fn update_king_cover(&mut self, pos: Pos) -> () {
        let attacks = KING_ATTACKS[pos];
        self.cover[pos].0 |= attacks.0;
    }


    
    pub(super) fn update_king_legal(&mut self, king_pos: Pos, friendly_pieces: BitBoard) -> () {
        // get variables
        let color = self.board[king_pos].unwrap().color;
        let op_cover = self.cover_comb[color.opp() as usize];
        
        // set all legal moves
        let attacks = KING_ATTACKS[king_pos];
        self.legal[king_pos].0 |= attacks.0 & !friendly_pieces.0 & !op_cover.0;

        // castle
        let row: u8 = (match color { Color::White => 7, Color::Black => 0 }) *8;
        if king_pos == row+4 {
            // left
            if self.castle[color as usize][0] {
                if  self.board[row+3].is_none() && !op_cover.get(row+3) &&
                    self.board[row+2].is_none() && !op_cover.get(row+2) &&
                    self.board[row+1].is_none() && !op_cover.get(row+1) &&
                    self.board[row+0] == Some(Piece{ color, role: Role::Rook}) {
                        self.legal[king_pos].set(row+2);
                }
            } 
            // right
            if self.castle[color as usize][1] {
                if  self.board[row+5].is_none() && !op_cover.get(row+5) &&
                    self.board[row+6].is_none() && !op_cover.get(row+6) &&
                    self.board[row+7] == Some(Piece{ color, role: Role::Rook}) {
                        self.legal[king_pos].set(row+6);
                }
            }
        }
    }
}

