mod game;
use game::Game;

// imports for making py library
use once_cell::sync::Lazy;
use std::sync::Mutex;
use pyo3::prelude::*;


// objects
static GAME: Lazy<Mutex<Game>> = Lazy::new(|| { Mutex::new(Game::new()) });
static INIT: Lazy<Mutex<bool>> = Lazy::new(|| Mutex::new(false));



/// Initializes the game.
#[pyfunction]
fn init() -> PyResult<()> {
    let mut game = GAME.lock().unwrap();
    let mut init = INIT.lock().unwrap();
    
    *game = Game::new();  
    *init = true;

    Ok(())
}

/// Trys the given move, if it is legal, plays it and returns 'true', otherwise returns 'false'.
#[pyfunction]
fn play(start_pos: (i8,i8), end_pos: (i8,i8)) -> PyResult<bool> {
    let mut game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 
    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("run init()")); }

    if game.play((start_pos, end_pos)) {
        return Ok(false);
    } 
    return Ok(true);
}

/// Plays the best move. 
#[pyfunction]
fn autoplay() -> PyResult<()> {
    let mut game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 
    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("run init()")); }

    game.autoplay();
    Ok(())
}


/// Returns game info
#[pyfunction]
fn get_state() -> PyResult<()> {
    Ok(())
}



/// Chess game-engine
/// 
/// Call michess.init() to start the game.
/// Call michess.play(start_pos, end_pos) or michess.autoplay to make a move.
/// 
#[pymodule]
fn michess(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // control functions
    m.add_function(wrap_pyfunction!(init, m)?)?;
    m.add_function(wrap_pyfunction!(play, m)?)?;
    m.add_function(wrap_pyfunction!(autoplay, m)?)?;

    // return game info functions
    m.add_function(wrap_pyfunction!(get_state, m)?)?;
    Ok(())
}
