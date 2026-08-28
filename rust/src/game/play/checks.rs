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

            self.play(mv);

            if !self.cover_comb[self.player.opp() as usize].get(king_pos) {
                self.undo();
                return;
            }

            self.undo();
        }
        self.mode = GameMode::Finished(Some(self.player.opp()));
    }


    // Changes : self.mode
    pub(super) fn draw_check(&mut self) -> () {
        // 50 move rule
        if self.rule_50moves > 100 {
            self.mode = GameMode::Finished(None);
            return;
        }
        
        // stalemate
        if !self.check {
            for pos in ALL_POS {
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

        let mut w_material: i8 = 0;
        let mut b_material: i8 = 0;

        for place in ALL_POS {
            match self.board[place] {
                WB | WH => w_material += 1,
                BB | BH => b_material += 1,
                WK | BK | __ => (),
                _         =>  { return }
            }
        }
        if w_material == 0 && b_material <= 1 || w_material <= 1 && b_material == 0 {
            self.mode = GameMode::Finished(None);
            return;
        }
    }



}