use super::*;


impl Game {
    pub(super) fn get_dirty(&mut self) -> () {
        // if not first move
        if let Some(played) = self.played {
            self.dirty = BitBoard::new();

            // update move
            self.dirty.set(played.mv.1);
            self.get_dirty_for_pos(played.mv.0);
            self.get_dirty_for_pos(played.mv.1);

            match played.tp {
                MoveType::EnPassant => {
                    // update captured pawn
                    self.get_dirty_for_pos(played.mv.0.row()*8 + played.mv.1.col());  
                },
                MoveType::Castle(rook_mv) => {
                    self.dirty.set(rook_mv.1);
                    self.get_dirty_for_pos(rook_mv.0);
                    self.get_dirty_for_pos(rook_mv.1);
                },
                _ => {}
            }
        } else {
            self.dirty.set_all();
        }
    }


    fn get_dirty_for_pos(&mut self, given_pos: Pos) -> () {
        // all who attacks the square
        for pos in 0..64 {
            if self.cover[pos].get(given_pos) {
                self.dirty.set(pos);
            }
        }

        // pawns in range of their legal moves
        for row_offset in [1, 2, -1, -2] {
            let pos: i8 = given_pos as i8 + row_offset*8;
            if pos >= 0 && pos < 64 {
                if self.board[pos as u8].is_some_and(|p| p.role == Role::Pawn) {
                    self.dirty.set(pos as u8);
                }
            }
        }
    }
}