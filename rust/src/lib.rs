pub mod state;
pub use state::{State, Game, info};

use once_cell::sync::Lazy;
use std::sync::Mutex;

use pyo3::prelude::*;


// objects
static GAME: Lazy<Mutex<Game>> = Lazy::new(|| { Mutex::new(Game::new()) });
static STATE: Lazy<Mutex<State>> = Lazy::new(|| { Mutex::new(State::new()) });
static INIT: Lazy<Mutex<bool>> = Lazy::new(|| Mutex::new(false));


// main functions

#[pyfunction]
fn init() -> PyResult<()> {
    let mut game = GAME.lock().unwrap();
    let mut state = STATE.lock().unwrap();
    let mut init = INIT.lock().unwrap();
    
    *game = Game::new();  
    *state = State::new();

    info( &mut game );
    
    if game.mode != 'g' { return Err(pyo3::exceptions::PyRuntimeError::new_err("Board is invalid.")); }
    *init = true;

    state.history_push(&mut game);
    Ok(())
}


#[pyfunction]
fn play(start_pos: (i8,i8), end_pos: (i8,i8)) -> PyResult<()> {
    let mut game = GAME.lock().unwrap();
    let mut state = STATE.lock().unwrap();
    let init = INIT.lock().unwrap(); 

    if game.mode != 'g' || *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    state.play( &mut game, start_pos, end_pos);
    Ok(())
}

#[pyfunction]
fn autoplay() -> PyResult<()> {
    let mut game = GAME.lock().unwrap();
    let mut state = STATE.lock().unwrap();
    let init = INIT.lock().unwrap(); 


    if game.mode != 'g' || *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    state.bot_play( &mut game, 0 );
    Ok(())
}

// getters

#[pyfunction]
fn board() -> PyResult<[[(char,char);8];8]> {
    let game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 

    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    Ok(game.board.clone())
}

#[pyfunction]
fn legal() -> PyResult<[[Vec<(i8, i8)>; 8]; 8]> {
    let game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 
    
    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    Ok(game.legal.clone())
}

#[pyfunction]
fn cover( side: char ) -> PyResult<[[Vec<(i8, i8)>; 8]; 8]> {
    let game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 

    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    match side {
        'w' => Ok(game.w_cover.clone()),
         _  => Ok(game.b_cover.clone()),
    }
}

#[pyfunction]
fn turn() -> PyResult<char> {
    let game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 

    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    Ok(game.player)
}

#[pyfunction]
fn mode() -> PyResult<char> {
    let game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 

    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    Ok(game.mode)
}




#[pymodule]
fn michess(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // control functions
    m.add_function(wrap_pyfunction!(init, m)?)?;
    m.add_function(wrap_pyfunction!(play, m)?)?;
    m.add_function(wrap_pyfunction!(autoplay, m)?)?;

    // return game info functions
    m.add_function(wrap_pyfunction!(board, m)?)?;
    m.add_function(wrap_pyfunction!(legal, m)?)?;
    m.add_function(wrap_pyfunction!(cover, m)?)?;

    // return main info functions
    m.add_function(wrap_pyfunction!(turn, m)?)?;
    m.add_function(wrap_pyfunction!(mode, m)?)?;
    Ok(())
}
