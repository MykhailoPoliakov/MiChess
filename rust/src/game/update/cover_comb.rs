use super::*;

impl Game {
    pub(super) fn update_cover_comb(&mut self) -> () {
        self.cover_comb = [BitBoard::new(), BitBoard::new()];

        for pos in ALL_POS {
            if let Some(piece) = self.board[pos] {
                self.cover_comb[piece.color as usize] |= self.cover[pos];
            }
        }
    }
}