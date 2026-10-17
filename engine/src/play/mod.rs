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


    pub fn run(&mut self, moves: &str) {
        let mut count: i32 = 0;

        for str_mv in moves.split_whitespace() {
            let mv = str_to_move(str_mv);

            if self.validate(mv).is_err() {
                panic!("Move {} wasn't walidated at index: {}", str_mv, count);
            }
            self.play(mv); 
            count += 1;
        }
    }

    
    pub fn unrun(&mut self, amount: i32) {
        for _ in 0..amount {
            self.undo(); 
        }
    }
}





