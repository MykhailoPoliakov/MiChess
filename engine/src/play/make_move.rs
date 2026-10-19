use super::*;

impl Game {
    // changes: state and cache.played and cache.dirty
    // makes move and swaps player, caches played move
    pub(super) fn make_move(&mut self, mv: Move) {
        let piece = self.state.board[mv.start].unwrap();
        
        // save played move
        self.history.push(PlayedMove {
            mv, 
            captured: if let MoveType::EnPassant(enpassant_pos) = mv.tp {self.state.board[enpassant_pos]} else {self.state.board[mv.end]}, 
            old_en_passant: self.state.en_passant,
            old_castle: self.state.castle,
            move_count: self.state.move_count
        });

        // reset en_passant
        self.state.en_passant = None;
        if piece.role == Role::Pawn && (mv.start.row() as i8 - mv.end.row() as i8).abs() == 2 {
            self.state.en_passant = Some(mv.start.col());
        }

        // cancel castle
        if piece.role == Role::Rook {
            match mv.start {
                0  => self.state.castle.set(Color::Black, 0, false),  
                7  => self.state.castle.set(Color::Black, 1, false),  
                56 => self.state.castle.set(Color::White, 0, false), 
                63 => self.state.castle.set(Color::White, 1, false),  
                _  => {}
            }
        }
        match mv.end {
            0  => self.state.castle.set(Color::Black, 0, false),  
            7  => self.state.castle.set(Color::Black, 1, false),  
            56 => self.state.castle.set(Color::White, 0, false), 
            63 => self.state.castle.set(Color::White, 1, false),  
            _  => {}
        }


        // play the move
        match mv.tp {
            MoveType::Basic => {
                self.state.board[mv.end] = self.state.board[mv.start];
            }
            MoveType::Promotion(role) => {
                self.state.board[mv.end] = Some(Piece{color: self.state.player, role});
            }
            MoveType::Castle(rook_mv) => {
                self.state.board[rook_mv.1] = self.state.board[rook_mv.0];
                self.state.board[rook_mv.0] = None;
                self.state.board[mv.end] = self.state.board[mv.start];
                self.state.castle.set_side(piece.color, false);
            }
            MoveType::EnPassant(enpassant_pos) => {
                self.state.board[enpassant_pos] = None;
                self.state.board[mv.end] = self.state.board[mv.start];
            }
        }
        self.state.board[mv.start] = None;


        // change the player
        self.state.player = self.state.player.opp();
    }
}