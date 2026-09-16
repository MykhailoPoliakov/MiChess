use super::*;

const MATE_VALUE: [i32; 2] =  [1_000_000, -1_000_000];


impl Game {
    pub fn analyze(&mut self, ctx: &mut Contex) -> i32 {
        if let Some(value) = status(&self.state.mode, ctx.depth) {
            return value;
        }

        if ctx.depth > 2 && !self.should_go_deeper(ctx.depth, 4) {
            return self.eval();
        }

        let mut best: i32  = if self.state.player == Color::White {i32::MIN} else {i32::MAX};
        
        for mv in self.cache.legal_moves.clone() {

            self.play(mv);
            ctx.depth += 1;

            ctx.iterated += 1;

            let value: i32;
            // go deeper if needed
            value = self.analyze(ctx);

            // save move info
            match self.state.player.opp() {
                Color::White => { if best < value {best = value} },
                Color::Black => { if best > value {best = value} },
            }
            self.undo();
            ctx.depth -= 1;
            
        }

        best
    }
}




// check if self is runnig or it is finished
fn status(mode: &GameMode, depth: i8) -> Option<i32> {
    match mode {
        &GameMode::Active => None,
        &GameMode::Finished(None) => Some(0),
        &GameMode::Finished(Some(color)) => Some(MATE_VALUE[color as usize] - (depth/2) as i32),
    }
}



impl Game {
    fn should_go_deeper(&self, depth: i8, real_max_depth: i8) -> bool {
        if depth > real_max_depth {
            return false;
        }

        if let Some(played) = self.played {
            // capture
            if played.captured.is_some() {
                return true;
            }
            // promotion
            if played.tp == MoveType::Promotion {
                return true;
            }
        }
        // check
        if self.cache.check {
            return true;
        }
        return false
    }
}
