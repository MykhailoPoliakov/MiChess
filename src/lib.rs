mod core;
use core::Game;
mod api;
use api::{get_py_state, PyState};

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
fn play(start_pos: u8, end_pos: u8) -> PyResult<bool> {
    let init = INIT.lock().unwrap(); 
    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("run init()")); }

    let mut game = GAME.lock().unwrap();
    return Ok(game.play((start_pos, end_pos)));
}


/// Plays the best move. 
#[pyfunction]
fn autoplay() -> PyResult<()> {
    let init = INIT.lock().unwrap(); 
    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("run init()")); }

    let mut game = GAME.lock().unwrap();
    game.autoplay();
    Ok(())
}


/// Returns game info
#[pyfunction]
fn state() -> PyResult<PyState> {
    let init = INIT.lock().unwrap(); 
    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("run init()")); }

    let game = GAME.lock().unwrap();
    Ok(get_py_state(&game))
}



/// Chess game-engine
#[pymodule]
fn michess(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // control functions
    m.add_function(wrap_pyfunction!(init, m)?)?;
    m.add_function(wrap_pyfunction!(play, m)?)?;
    m.add_function(wrap_pyfunction!(autoplay, m)?)?;

    // get info
    m.add_function(wrap_pyfunction!(state, m)?)?;
    Ok(())
}
