use super::*;

mod cover_comb;
mod legal_moves;
mod pieces;
mod constants;
use constants::*;
mod get_dirty;

// Analyses the board, saves all cached data
// Changes: game.cache

impl Game {
    pub fn update(&mut self) -> () {
        // get pieces location BitBoards
        let pieces = board_to_bitboards(&self.state.board);

        // for every dirty piece
        //for pos in 0..64 {
        for pos in self.get_dirty().clone().iter_pos() {

            // cleaning
            self.cache.cover[pos] = BitBoard::new();
            self.cache.legal[pos] = BitBoard::new();

            // matching piece
            if let Some(piece) = self.state.board[pos] {
                match piece.role {
                    Role::Pawn => {
                        self.update_pawn(piece, pos, pieces[piece.color.opp() as usize]);
                    }
                    Role::Knight => {
                        self.update_knight(pos, pieces[piece.color as usize]);
                    }
                    Role::Bishop => {
                        self.update_bishop(pos, pieces , piece.color);
                    }
                    Role::Rook => {
                        self.update_rook(pos, pieces , piece.color);
                    }
                    Role::Queen => {
                        self.update_bishop(pos, pieces , piece.color);
                        self.update_rook(pos, pieces , piece.color);
                    }
                    Role::King => {
                        self.update_king_cover(pos);
                        self.cache.king_pos[piece.color as usize] = pos;
                    }
                }
            }
        }

        // update cover comb 
        self.update_cover_comb();

        // dirty king legal updated last and fill king pos 
        self.update_king_legal(self.cache.king_pos[0], pieces[0]);
        self.update_king_legal(self.cache.king_pos[1], pieces[1]);

        // save legal moves and check status
        self.update_legal_moves(pieces);
        self.cache.check = self.cache.cover_comb[self.state.player.opp() as usize].get(self.cache.king_pos[self.state.player as usize]);
    }


}




fn board_to_bitboards(board: &Board) -> [BitBoard; 2] {
    let mut result = [BitBoard(0); 2];
    let mut i: u64 = 0;
    for square in &board.0 {
        if let Some(piece) = square {
            result[piece.color as usize].0 |= 1u64 << i;
        }
        i += 1;
    }
    result
}

