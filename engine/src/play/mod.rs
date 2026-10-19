use super::*;

mod mode_checks;
mod make_move;
mod undo_move;


impl Game {
    pub fn safeplay(&mut self, smv: (u8,u8), role: Option<Role>) -> Result<(), MoveError> {
        if self.state.mode != GameMode::Active {
            return Err(MoveError::WrongMode);
        }
        if !self.state.board[smv.0].is_some_and(|p| p.color == self.state.player) {
            return Err(MoveError::NoPiece);
        }
        if !self.cache.legal_moves.iter().any(|mv| mv.start == smv.0 && mv.end == smv.1) {
            return Err(MoveError::IlligalMove);
        }

  
        let mv = if let Some(role) = role {
            *self.cache.legal_moves.iter().find(|m| m.start == smv.0 && m.end == smv.1 && m.tp == MoveType::Promotion(role)).unwrap()
        } else {
            let m =*self.cache.legal_moves.iter().find(|m| m.start == smv.0 && m.end == smv.1).unwrap();
            if let MoveType::Promotion(_) = m.tp {
                return Err(MoveError::NoPromotionPiece);
            }
            m
        };
        
        self.play(mv);

        return Ok(());
        
    }


    pub fn play(&mut self, mv: Move) {
        
        // play move
        self.make_move(mv);

        // update cache
        self.update();
        
        // check for wins and draws
        self.mode_check();
    }

    
    pub fn undo(&mut self) -> bool {
        // check if history is not empty and pop last
        if self.history.is_empty() {
            return false;
        };

        // undo state
        self.undo_move();

        // update cache with current played
        self.update();

        // undo played
        self.history.pop();

        return true;        
    }


    pub fn run(&mut self, moves: &str) {
        let mut count: i32 = 0;

        for str_mv in moves.split_whitespace() {
            let (smv, role) = str_to_safemove(str_mv);

            if self.safeplay(smv, role).is_err() {
                panic!("Move {} wasn't walidated at index: {}", str_mv, count);
            }
            count += 1;
        }
    }


    pub fn unrun(&mut self, amount: i32) {
        for _ in 0..amount {
            self.undo(); 
        }
    }
}





