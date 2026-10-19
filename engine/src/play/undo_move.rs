use super::*;

impl Game {
    pub(super) fn undo_move(&mut self) {
        let played = self.history.last().unwrap();

        // undo state
        self.state.castle = played.old_castle;
        self.state.en_passant = played.old_en_passant;
        self.state.move_count = played.move_count;
        self.state.mode = GameMode::Active;
        self.state.player = self.state.player.opp();
        
        // undo the move
        match played.mv.tp {
            MoveType::Basic => {
                self.state.board[played.mv.start] = self.state.board[played.mv.end];
                self.state.board[played.mv.end] = played.captured;
            }
            MoveType::Promotion(_) => {
                self.state.board[played.mv.start] = Some(Piece{color: self.state.player, role: Role::Pawn});
                self.state.board[played.mv.end] = played.captured;
            }
            MoveType::Castle(rook_mv) => {
                self.state.board[rook_mv.0] = self.state.board[rook_mv.1];
                self.state.board[rook_mv.1] = None;
                self.state.board[played.mv.start] = self.state.board[played.mv.end];
                self.state.board[played.mv.end] = None;
            }
            MoveType::EnPassant(enpassant_pos) => {
                self.state.board[enpassant_pos] = played.captured;
                self.state.board[played.mv.start] = self.state.board[played.mv.end];
                self.state.board[played.mv.end] = None;
            }
        }
    }
}