use super::*;


impl Game {
    pub(super) fn mode_check(&mut self) -> () {
        self.stalemate_and_win_check();
        self.no_material_check();
        self.rule_50_check();
        self.repeating_moves_check();
    }


    fn stalemate_and_win_check(&mut self) -> () {
        if self.cache.legal_moves.is_empty() {
            match self.cache.check {
                true  => self.state.mode = GameMode::Finished(Some(self.state.player.opp())),
                false => self.state.mode = GameMode::Finished(None),
            }
        }
    }


    fn no_material_check(&mut self) -> () {

        let mut w_material: u8 = 0;
        let mut b_material: u8 = 0;

        for pos in 0..64 {
            match self.state.board[pos] {
                WB | WH => w_material += 1,
                BB | BH => b_material += 1,
                WK | BK | __ => (),
                _         =>  { return; }
            }
        }
        if w_material == 0 && b_material <= 1 || w_material <= 1 && b_material == 0 {
            self.state.mode = GameMode::Finished(None);
            return;
        }
    }

    fn rule_50_check(&mut self) {
        // reset
        if let Some(played) = self.history.last() {
            if self.state.board[played.mv.end].is_some_and( |p| p.role == Role::Pawn) || 
            played.captured.is_some() ||
            played.mv.tp != MoveType::Basic {
                self.state.move_count = 0;
            }
        }
        // add move
        self.state.move_count += 1;

        // if over the limit
        if self.state.move_count >= 100 {
            self.state.mode = GameMode::Finished(None);
            return;
        }
    }

    fn repeating_moves_check(&mut self) {
        if self.history.len() < 12 {
            return;
        }

        let last_played = self.history.last().unwrap();
        let op_last_played = &self.history[self.history.len() - 2];
        
        let mut count: [i32; 2] = [0,0];

        for played in self.history.iter().rev().take(12) {
            if last_played == played {
                count[0] += 1;
            } 
            if op_last_played == played {
                count[1] += 1;
            }
        }

        if count[0] >= 3 && count[1] >= 3 {
            self.state.mode = GameMode::Finished(None);
        }

    }

}