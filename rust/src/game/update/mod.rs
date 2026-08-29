use super::*;

mod cover_comb;
mod legal_moves;
mod pieces;
mod constants;
use constants::*;

// Analyses the board, saves all the game.legal moves and covers for exact board position.
// Changes: game.game.legal , game.w_cover , game.b_cover

impl Game {
    pub fn update(&mut self, dirty: BitBoard) -> () {
        // get pieces location BitBoards
        let pieces = board_to_bitboards(&self.board);

        // for every dirty piece
        for pos in dirty.iter_pos() {

            // cleaning
            self.cover[pos] = BitBoard::new();
            self.legal[pos] = BitBoard::new();

            // matching piece
            if let Some(piece) = self.board[pos] {
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
                        // fill piece pos for legal
                        self.king_pos[piece.color as usize] = pos;
                    }
                }
            }
        }

        // update cover comb 
        self.update_cover_comb();

        // king legal updated last
        for king_pos in self.king_pos {
            self.update_king_legal(king_pos, pieces[self.board[king_pos].unwrap().color as usize]);
        }

        self.update_legal_moves();
    }
}




fn board_to_bitboards(board: &Board) -> [BitBoard;2] {
    let mut white = BitBoard::new();
    let mut black = BitBoard::new();
    
    for (i, square) in board.0.iter().enumerate() {
        if let Some(piece) = square {
            match piece.color {
                Color::White => white.0 |= 1u64 << i,
                Color::Black => black.0 |= 1u64 << i,
            }
        }
    }
    [white, black]
}