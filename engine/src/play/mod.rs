use super::*;

mod mode_checks;
mod make_move;


impl Game {
    // makes a move, returns bool
    pub fn play(&mut self, mv: Move) {
        
        // save history
        self.history.push(self.save());

        // play move
        self.make_move(mv);

        // update cache
        self.update();

        // update transformer
        // self.transformer.play(&NNUE, &self.state.board, self.cache.king_pos, self.played.mv.unwrap());
        
        // check for wins and draws
        self.mode_check();
    }


    pub fn validate(&self, mv: Move) -> Result<(), MoveError> {
        if self.state.mode != GameMode::Active {
            return Err(MoveError::WrongMode);
        }
        if !self.state.board[mv.0].is_some_and(|p| p.color == self.state.player) {
            return Err(MoveError::NoPiece);
        }
        if !self.cache.legal_moves.contains(&mv) {
            return Err(MoveError::IlligalMove);
        }
        Ok(())
    }
}





