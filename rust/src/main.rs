mod game_class;
use game_class::Game;

mod state;
use state::State;


pub struct Interface {
    state: State,
    game: Game,
}

impl Interface {
    pub fn new() -> Self {
        Interface {
            state: State::new('w', false),
            game: Game::new(),
        }
    }

    pub fn init(&mut self) {
        self.state.info( &mut self.game, ' ');
    }

    pub fn play(&mut self, start_pos: (i8,i8), end_pos: (i8,i8) ) {
        self.state.play(&mut self.game, start_pos, end_pos);
    }

    pub fn bot_play(&mut self) {
        self.state.bot_play();
    }

    pub fn board(&self) -> [[(char,char);8];8] {
        println!("board");
        for row in self.game.board {
            for cell in row {
                print!("{} ", cell.0);
                print!("{} ", cell.1);
                print!(" ");
            }
            println!();
        }
        return self.game.board;
    } 
}



fn main() {
    
    let mut interface = Interface::new();

    interface.init();
    interface.play( (7,1),(5,0)); 
    interface.play( (0,1),(2,0)); 
    


    println!("w_cover");
    for row in &interface.game.w_cover {
        for cell in row {
            print!("{:?} ", cell);
        }
        println!();
    }

    println!("b_cover");
    for row in &interface.game.b_cover {
        for cell in row {
            print!("{:?} ", cell);
        }
        println!();
    }

    println!("legal");
    for row in &interface.game.legal {
        for cell in row {
            print!("{:?} ", cell);
        }
        println!();
    }

    interface.board();
    
        
}


