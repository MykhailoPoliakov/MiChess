pub mod state;
pub use state::{State, Game, info};

// imports for making py library
use once_cell::sync::Lazy;
use std::sync::Mutex;
use pyo3::prelude::*;


// objects
static GAME: Lazy<Mutex<Game>> = Lazy::new(|| { Mutex::new(Game::new()) });
static STATE: Lazy<Mutex<State>> = Lazy::new(|| { Mutex::new(State::new()) });
static INIT: Lazy<Mutex<bool>> = Lazy::new(|| Mutex::new(false));



/// Initializes the game.
/// 
/// Without calling this function nothing will work.
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

/// Trys the given move, if it is legal, plays it and returns 'true', otherwise returns 'false'.
#[pyfunction]
fn play(start_pos: (i8,i8), end_pos: (i8,i8)) -> PyResult<bool> {
    let mut game = GAME.lock().unwrap();
    let mut state = STATE.lock().unwrap();
    let init = INIT.lock().unwrap(); 

    if game.mode != 'g' || *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    if !state.check_move( &game, &start_pos, &end_pos) {
        println!("Move was illigal because of check on king");
        return Ok(false);
    }
    if !state.movement( &mut game, &start_pos, &end_pos, true) {
        println!("Move was illigal");
        return Ok(false);
    } 
    return Ok(true);
}

/// Plays the best move. 
#[pyfunction]
fn autoplay() -> PyResult<()> {
    let mut game = GAME.lock().unwrap();
    let mut state = STATE.lock().unwrap();
    let init = INIT.lock().unwrap(); 


    if game.mode != 'g' || *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    state.bot_play( &mut game, 4 );
    Ok(())
}


/// Returns the board as [Vec<(str,str)>;8];8].
#[pyfunction]
fn board() -> PyResult<[[(char,char);8];8]> {
    let game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 

    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    Ok(game.board.clone())
}

/// Returns all the legal moves as [Vec<(int,int)>;8];8].
#[pyfunction]
fn legal() -> PyResult<[[Vec<(i8, i8)>; 8]; 8]> {
    let game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 
    
    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    Ok(game.legal.clone())
}


/// Returns choosen cover moves as [Vec<(int,int)>;8];8].
/// Args: 
///     'w' - for whtie cover moves.
///     'b' - for black cover moves.
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

/// Returns whose turn it is: 
///     'w' - for white.
///     'b' - for black.
#[pyfunction]
fn turn() -> PyResult<char> {
    let game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 

    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    Ok(game.player)
}

/// Returns game mode : 
///     'g' for active game.
///     'd' for draw. 
///     'w' for white pieces win.
///     'b' for black pieces win.
#[pyfunction]
fn mode() -> PyResult<char> {
    let game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 

    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    Ok(game.mode)
}


/// Returns board history as Vec<[[(str,str);8];8]>.
#[pyfunction]
fn history() -> PyResult<Vec<[[(char,char);8];8]>> {
    let game = GAME.lock().unwrap();
    let init = INIT.lock().unwrap(); 

    if *init == false { return Err(pyo3::exceptions::PyRuntimeError::new_err("Game is not running.")); }

    Ok(game.history.clone())
}



/// Chess game-engine
/// 
/// Call michess.init() to start the game.
/// Call michess.play(start_pos, end_pos) or michess.autoplay to make a move.
/// 
/// Get board : michess.board()
/// Get whose turn it is : michess.turn()
/// Get game mode : michess.mode()
/// 
/// Other getters : michess.legal(), michess.cover( side ), michess.history()
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
    m.add_function(wrap_pyfunction!(history, m)?)?;


    // return main info functions
    m.add_function(wrap_pyfunction!(turn, m)?)?;
    m.add_function(wrap_pyfunction!(mode, m)?)?;
    Ok(())
}
