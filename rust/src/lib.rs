mod state;
pub use state::State;
pub use state::Game;

use once_cell::sync::Lazy;
use std::sync::Mutex;

use pyo3::prelude::*;


// objects
static GAME: Lazy<Mutex<Game>> = Lazy::new(|| { Mutex::new(Game::new()) });
static STATE: Lazy<Mutex<State>> = Lazy::new(|| { Mutex::new(State::new()) });
//static INIT: Lazy<Mutex<bool>> = Lazy::new(|| Mutex::new(false));


// main functions

#[pyfunction]
fn init() -> PyResult<()> {
    let mut game = GAME.lock().unwrap();
    let mut state = STATE.lock().unwrap();
    state.info( &mut game );
    state.history_push(&mut game);
    Ok(())
}

#[pyfunction]
fn play(start_pos: (i8,i8), end_pos: (i8,i8) ) {
    let mut game = GAME.lock().unwrap();
    let mut state = STATE.lock().unwrap();
    state.play( &mut game, start_pos, end_pos);
}

#[pyfunction]
fn autoplay() {
    let mut game = GAME.lock().unwrap();
    let mut state = STATE.lock().unwrap();
    state.bot_play( &mut game, 0 );
}

// getters

#[pyfunction]
fn board() -> PyResult<[[(char,char);8];8]> {
    let game = GAME.lock().unwrap();
    Ok(game.board.clone())
}

#[pyfunction]
fn legal() -> PyResult<[[Vec<(i8, i8)>; 8]; 8]> {
    let game = GAME.lock().unwrap();
    Ok(game.legal.clone())
}

#[pyfunction]
fn cover( side: char ) -> PyResult<[[Vec<(i8, i8)>; 8]; 8]> {
    let game = GAME.lock().unwrap();
    match side {
        'w' => Ok(game.w_cover.clone()),
         _  => Ok(game.b_cover.clone()),
    }
}

#[pyfunction]
fn turn() -> PyResult<char> {
    let game = GAME.lock().unwrap();
    Ok(game.player)
}

#[pyfunction]
fn mode() -> PyResult<char> {
    let game = GAME.lock().unwrap();
    Ok(game.mode)
}




#[pymodule]
fn michess(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(init, m)?)?;
    m.add_function(wrap_pyfunction!(play, m)?)?;
    m.add_function(wrap_pyfunction!(autoplay, m)?)?;

    m.add_function(wrap_pyfunction!(board, m)?)?;
    m.add_function(wrap_pyfunction!(legal, m)?)?;
    m.add_function(wrap_pyfunction!(cover, m)?)?;
    
    m.add_function(wrap_pyfunction!(turn, m)?)?;
    m.add_function(wrap_pyfunction!(mode, m)?)?;
    Ok(())
}
