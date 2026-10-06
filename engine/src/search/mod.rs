use super::*;

mod analyze;
mod eval;
mod choose_move;


pub struct Contex {
    pub init_player: Color,
    pub depth: i8,
    pub iterated: i32,
}


impl Game {
    pub fn start_search(&mut self) {
        self.search = SearchInfo::new();
        let total = self.cache.legal_moves.len() as f32;
        
        let mut ctx = Contex { init_player: self.state.player, depth: 1, iterated: 0};
        
        let mut moves: Vec<(Move, i32)> = Vec::new(); 

        

        // playing all legal moves and getting move value
        for mv in self.cache.legal_moves.clone() {
            
            self.play(mv);
            ctx.iterated = 0;

            let value = self.analyze(&mut ctx);
            
            self.search.status = SearchStatus::InProgress(moves.len() as f32 / total);
            self.search.info.push((mv, Eval::from_value(value), ctx.iterated));
            
            moves.push((mv, value));
            self.undo();
        }


        self.search.status = SearchStatus::Finished;
        self.search.mv = Some(self.choose_move(&mut moves));
        self.search.eval = Some(Eval::from_value(match self.state.player {
            Color::White => moves.iter().map(|x| x.1).max().unwrap(),
            Color::Black => moves.iter().map(|x| x.1).min().unwrap(),
        }));
    }
}




