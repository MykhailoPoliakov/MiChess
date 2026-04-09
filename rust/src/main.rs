mod state;
use state::Interface;


fn main() {
    
    let mut interface = Interface::new();

    interface.init();
    interface.play( (7,1),(5,0)); 
    interface.bot_play();

    interface.cover_moves();
    interface.legal_moves();
    interface.board();
    
}


