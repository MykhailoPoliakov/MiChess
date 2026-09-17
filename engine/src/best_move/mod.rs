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
    pub fn best_move(&mut self) -> Move {
        // clone for safety
        let game = &mut self.clone(); 
        
        let mut ctx = Contex { init_player: game.state.player, depth: 1, iterated: 0};
        
        let mut moves: Vec<(Move, i32)> = Vec::new(); 

        // playing all legal moves and getting move value
        for mv in game.cache.legal_moves.clone() {
            
            game.play(mv);
            ctx.iterated = 0;
            
            let value = game.analyze(&mut ctx);

            println!("Move: {:?}, Value: {:?}, Iteratrions done : {}", move_to_str(mv), value, ctx.iterated);

            moves.push((mv, value));
            game.undo();
        }

        // make move
        // let mv = moves.iter()
        //     .max_by_key(|(_, value)| {if self.state.player == Color::White { *value} else {-*value} })
        //     .map(|(mv, _)| *mv)
        //     .unwrap();
        let mv = self.choose_move(&mut moves);

        // console ouput
        println!("\n---Bot makes move!---\nchosen move: {}\n", move_to_str(mv));
        mv
    }
}




