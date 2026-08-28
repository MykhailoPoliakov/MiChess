use super::*;

mod cover_comb;
mod legal_moves;
mod pieces;

// constants of how pieces move
const ROOK_MOVES: [Pos; 4] = [(1, 0), (-1, 0), (0, -1), (0, 1)];
const BISHOP_MOVES: [Pos; 4] = [(1, -1), (-1, 1), (-1, -1), (1, 1)];
const KNIGHT_MOVES: [Pos; 8] = [(1, -2), (-1, 2), (-1, -2), (1, 2), (2, -1), (-2, 1), (-2, -1), (2, 1)];
const KING_MOVES: [Pos; 8] = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, -1), (-1, 1), (-1, -1), (1, 1)];


// Analyses the board, saves all the game.legal moves and covers for exact board position.
// Changes: game.game.legal , game.w_cover , game.b_cover

impl Game {
    pub fn update(&mut self) -> () {

        // for every dirty piece
        for pos in self.dirty.clone().iter_pos() {

            // cleaning
            self.cover[pos] = BitBoard::new();
            self.legal[pos] = BitBoard::new();

            // matching piece
            if let Some(piece) = self.board[pos] {
                match piece.role {
                    Role::Pawn => {
                        self.update_pawn(piece, pos);
                    }
                    Role::Knight => {
                        self.update_knight(piece, pos);
                    }
                    Role::Bishop => {
                        self.update_piece(piece, pos, &BISHOP_MOVES);
                    }
                    Role::Rook => {
                        self.update_piece(piece, pos, &ROOK_MOVES);
                    }
                    Role::Queen => {
                        self.update_piece(piece, pos, &KING_MOVES);
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
            self.update_king_legal(king_pos);
        }

        self.update_legal_moves();
    }
}



fn valid_i8(int: i8) -> bool { 
    if int >= 0 && int < 8 { true } else { false } 
}

fn valid(pos: Pos) -> bool {
    if pos.0 >= 0 && pos.0 < 8 && pos.1 >= 0 && pos.1 < 8{ true } else { false }
}


