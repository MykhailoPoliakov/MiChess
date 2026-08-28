use super::*;

impl Game { 
    pub(super) fn update_legal_moves(&mut self) {
        // clear 
        self.legal_moves.clear();
        // fill
        for pos in ALL_POS {
            if self.board[pos].is_some_and(|p| p.color == self.player) {
                let mut bits = self.legal[pos].0;
                while bits != 0 {
                    let bit = bits.trailing_zeros() as i8;
                    self.legal_moves.push((pos, (bit / 8, bit % 8)));
                    bits &= bits - 1;  // clear lowest set bit
                }
            }
        }
    }
}