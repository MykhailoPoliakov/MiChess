use super::*;

impl Game {
    // changes: state and cache.played and cache.dirty
    // makes move and swaps player, caches played move
    pub(super) fn make_move(&mut self, mv: Move) {
        let (start_pos, end_pos) = mv;
        
        // creating played move
        let mut played = PlayedMove {
            mv, tp: MoveType::Basic, captured: self.state.board[end_pos], 
            old_en_passant: self.state.en_passant,
            old_castle: self.state.castle,
        };

        // clear en passant
        self.state.en_passant = None;

        let piece = self.state.board[start_pos].unwrap();
        match piece.role {
            Role::Pawn => {
                // play en passant
                if Some(end_pos.col()) == played.old_en_passant {
                    let op_pawn_pos = start_pos.row()*8 + end_pos.col();
                    if self.state.board[op_pawn_pos] == Some(Piece{color: self.state.player.opp(), role: Role::Pawn}) {
                        // save move data
                        played.captured = self.state.board[op_pawn_pos];
                        played.tp = MoveType::EnPassant;
                        // capture opp pawn
                        self.state.board[op_pawn_pos] = None;
                    }
                }

                // set en passant
                if (start_pos.row() as i8 - end_pos.row() as i8).abs() == 2 {
                    self.state.en_passant = Some(start_pos.col());
                }
            },
            Role::Rook => {
                // cancel castle
                match start_pos {
                    0  => self.state.castle[1][0] = false,  
                    7  => self.state.castle[1][1] = false,  
                    56 => self.state.castle[0][0] = false, 
                    63 => self.state.castle[0][1] = false,  
                    _  => {}
                }
            },
            Role::King => {
                // make castle
                let row = match piece.color {Color::White => 7, Color::Black => 0};
                if start_pos.row() == row && end_pos.row() == row && start_pos.col() == 4 {
                    match end_pos.col() {
                        2 => { 
                            self.state.board[row*8 + 3] = Some(Piece{color: self.state.player, role: Role::Rook}); 
                            self.state.board[row*8 + 0] = None;
                            // save move data
                            played.tp = MoveType::Castle((row*8 + 0, row*8 + 3));
                        },
                        6 => { 
                            self.state.board[row*8 + 5] = Some(Piece{color: self.state.player, role: Role::Rook}); 
                            self.state.board[row*8 + 7] = None;
                            // save move data
                            played.tp = MoveType::Castle((row*8 + 7, row*8 + 5));
                        },
                        _  => {},
                    }
                }
                // cancel castle
                self.state.castle[piece.color as usize] = [false, false];
            },
            _ => {}
        }

        // if rook was captured cancel capture
        match end_pos {
            0  => self.state.castle[1][0] = false,  
            7  => self.state.castle[1][1] = false,  
            56 => self.state.castle[0][0] = false, 
            63 => self.state.castle[0][1] = false,  
            _  => {}
        }


        // possible promotion or basic move
        if piece.role == Role::Pawn && (end_pos < 8 || end_pos >= 56) {
            self.state.board[end_pos] = Some(Piece{color: self.state.player, role: Role::Queen});
            self.state.board[start_pos] = None;
            played.tp = MoveType::Promotion;
        } else {
            self.state.board[end_pos] = Some(piece);
            self.state.board[start_pos] = None;
        }


        // change the player
        self.state.player = self.state.player.opp();

        // update played
        self.played = Some(played);
    }
}