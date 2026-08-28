use super::*;


impl Game {
    pub(super) fn get_dirty(&mut self, mv: Move) -> () {
        let (start_pos, end_pos) = mv;
        // clean
        self.dirty = BitBoard::new();

        // update moved piece
        self.dirty.set(end_pos);

        // update pieces that were changed
        for pos in ALL_POS {
            if self.cover[pos].get(start_pos) || self.cover[pos].get(end_pos) {
                self.dirty.set(pos);
            }
        }

        // en passant case
        for side in [-1, 1] {
            let target = (start_pos.0 , start_pos.1  + side);
            if valid(target)  {
                if self.board[target].is_some_and(|p| p.role == Role::Pawn) && !self.dirty.contains(target) {
                    self.dirty.set(target);
                }
            }
        }

        // update close pawns
        for side in [-2,-1,1,2] {
            // start pos
            let target = (start_pos.0 + side, start_pos.1);
            if valid(target)  {
                if self.board[target].is_some_and(|p| p.role == Role::Pawn) && !self.dirty.contains(target) {
                    self.dirty.set(target);
                }
            }
            // end pos
            let target = (end_pos.0 + side, end_pos.1);
            if valid(target)  {
                if self.board[target].is_some_and(|p| p.role == Role::Pawn) && !self.dirty.contains(target) {
                    self.dirty.set(target);
                }
            }
        }
    }
}





fn valid(pos: Pos) -> bool {
    if pos.0 >= 0 && pos.0 < 8 && pos.1 >= 0 && pos.1 < 8{
        true
    } else {
        false
    }
}