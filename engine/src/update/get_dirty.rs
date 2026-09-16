use super::*;


impl Game {
    pub(super) fn get_dirty(&self) -> BitBoard {
        // if not first move
        if let Some(played) = self.played {
            let mut dirty = BitBoard::new();

            // update move
            self.mark_dirty(played.mv.0, &mut dirty);
            self.mark_dirty(played.mv.1, &mut dirty);

            // all 3 and 4 rank pawn in case of en passant
            for pos in 24..40 {
                if self.state.board[pos].is_some_and(|p| p.role == Role::Pawn) {
                    dirty.set(pos);
                }
            }

            match played.tp {
                // update captured pawn
                MoveType::EnPassant => {
                    self.mark_dirty(played.mv.0.row()*8 + played.mv.1.col(), &mut dirty);  
                },
                // update rook
                MoveType::Castle(rook_mv) => {
                    self.mark_dirty(rook_mv.0, &mut dirty);
                    self.mark_dirty(rook_mv.1, &mut dirty);
                },
                _ => {}
            }
            dirty
        } else {
            BitBoard(u64::MAX)
        }
    }



    fn mark_dirty(&self, given_pos: Pos, dirty: &mut BitBoard) -> () {
        // self pos
        dirty.set(given_pos);

        // all who attacks the square
        for pos in COMBINED_DIRTY[given_pos].iter_pos() {
            if self.cache.cover[pos].get(given_pos) {
                dirty.set(pos);
            }
        }
        // pawns in range of their legal moves
        for pos in PAWN_DIRTY[given_pos].iter_pos() {
            if self.state.board[pos as u8].is_some_and(|p| p.role == Role::Pawn) {
                dirty.set(pos);
            }
        }
    }
}