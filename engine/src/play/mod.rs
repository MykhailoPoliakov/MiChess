use super::*;

mod mode_checks;
mod make_move;


impl Game {
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


    // makes a move, returns bool
    pub fn play(&mut self, mv: Move) {
        
        // save history
        self.history.push( GameLog {
            state: self.state.clone(),
            played: self.played,
        });

        // play move
        self.make_move(mv);

        // update cache
        self.update();
        
        // check for wins and draws
        self.mode_check();
    }

    
    pub fn undo(&mut self) -> bool {
        // check if history is not empty and pop last
        let Some(log) = self.history.pop() else {
            return false;
        };

        // undo state
        self.state = log.state;
        
        // update cache with current played
        self.update();

        // undo played
        self.played = log.played;

        return true;        
    }
}





