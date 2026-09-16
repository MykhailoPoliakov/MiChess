use super::*;


impl Game {
    pub(super) fn mode_check(&mut self) -> () {
        self.stalemate_and_win_check();
        self.no_material_check();
        self.rule_50_check();
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
        if let Some(played) = self.played {
            if self.state.board[played.mv.1].is_some_and( |p| p.role == Role::Pawn) || 
            played.captured.is_some() ||
            played.tp != MoveType::Basic {
                self.state.rule_50moves = 0;
            }
        }
        // add move
        self.state.rule_50moves += 1;

        // if over the limit
        if self.state.rule_50moves >= 100 {
            self.state.mode = GameMode::Finished(None);
            return;
        }
    }

}