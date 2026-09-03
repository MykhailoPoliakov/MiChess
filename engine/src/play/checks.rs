use super::*;


impl Game {
    // Changes : self.check
    pub(super) fn check_check(&mut self) -> () {
        let king_pos = self.king_pos[self.player as usize];
        self.check = self.cover_comb[self.player.opp() as usize].get(king_pos)
    }



    // Changes : self.mode
    pub(super) fn win_check(&mut self) -> () {
        if !self.check {
            return;
        }

        let king_pos = self.king_pos[self.player as usize];
        if !self.legal[king_pos].is_empty() {
            return;
        }

        let legal_moves = self.legal_moves.clone();
        for mv in legal_moves {

            if self.play(mv) {

                if !self.cover_comb[self.player.opp() as usize].get(king_pos) {
                    self.undo();
                    println!("win undo");
                    return;
                }

                self.undo();
                println!("win undo");
            }
        }
        self.mode = GameMode::Finished(Some(self.player.opp()));
    }


    // Changes : self.mode
    pub(super) fn stalemate_check(&mut self) -> () {
        // stalemate
        if !self.check {
            for pos in 0..64 {
                if self.board[pos].is_some_and(|p| p.color == self.player) &&
                !self.legal[pos].is_empty() {
                    return;
                }
            }
            self.mode = GameMode::Finished(None);
            return;
        }
    }


    // Changes : self.mode
    pub(super) fn no_material_check(&mut self) -> () {

        let mut w_material: u8 = 0;
        let mut b_material: u8 = 0;

        for pos in 0..64 {
            match self.board[pos] {
                WB | WH => w_material += 1,
                BB | BH => b_material += 1,
                WK | BK | __ => (),
                _         =>  { return; }
            }
        }
        if w_material == 0 && b_material <= 1 || w_material <= 1 && b_material == 0 {
            self.mode = GameMode::Finished(None);
            return;
        }
    }

    pub(super) fn rule_50_check(&mut self) {
        // reset
        if let Some(played) = self.played {
            if self.board[played.mv.1].is_some_and( |p| p.role == Role::Pawn) && played.captured.is_some() {
                self.rule_50moves = 0;
            }
        }
        // add move
        self.rule_50moves += 1;

        // if over the limit
        if self.rule_50moves >= 100 {
            self.mode = GameMode::Finished(None);
            return;
        }
    }

}