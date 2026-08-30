use crate::core::*;

use pyo3::prelude::*;

#[pyclass(from_py_object)]
#[derive(Clone)]
pub struct PyState {
     #[pyo3(get)]
    pub board_history: Vec<Vec<Option<PyPiece>>>,
     #[pyo3(get)]
    pub player: PyColor,
     #[pyo3(get)]
    pub mode: PyGameMode,
     #[pyo3(get)]
    pub legal: Vec<u64>,
     #[pyo3(get)]
    pub played: Vec<Move>,
}




#[pyclass(from_py_object)]
#[derive(Clone, PartialEq)]
pub enum PyColor {
    White,
    Black,
}


#[pyclass(from_py_object)]
#[derive(Clone, PartialEq)]
pub enum PyRole {
    King,
    Queen,
    Rook,
    Bishop,
    Knight,
    Pawn,
}


#[pyclass(from_py_object)]
#[derive(Clone)]
pub struct PyPiece {
    #[pyo3(get)]
    pub color: PyColor,
    #[pyo3(get)]
    pub role: PyRole,
}


#[pyclass(from_py_object)]
#[derive(Clone, PartialEq)]
pub enum PyGameMode {
    Active,
    Draw,
    WinWhite,
    WinBlack,
}


pub fn get_py_state(game: &Game) -> PyState {
    let player = match game.player {Color::Black => PyColor::Black, Color::White => PyColor::White};
    
    let legal = game.legal.0.iter().map(|bb| bb.0).collect();
    
    let mut played = Vec::new();
    if let Some(played_move) = game.played {
        played.push(played_move.mv);
        match played_move.tp {
            MoveType::Castle(mv) => played.push(mv),
            _ => {},
        }
    }
    
    let mode: PyGameMode;
    match game.mode {
        GameMode::Active => mode = PyGameMode::Active,
        GameMode::Finished(result) => {
            match result {
                None => mode = PyGameMode::Draw,
                Some(Color::White) => mode = PyGameMode::WinWhite,
                Some(Color::Black) => mode = PyGameMode::WinBlack,
            }
        }
    }

    let mut board_history= Vec::new();
    for log in &game.history {
        board_history.push(board_to_pyboard(&log.board));
    }
    board_history.push(board_to_pyboard(&game.board));



    PyState {
        player,
        legal,
        played,
        mode,
        board_history,
    }
}


fn board_to_pyboard(board: &Board) -> Vec<Option<PyPiece>> {
    board.0.iter().map(|sq| sq.map(|p| PyPiece {
        color: match p.color {
            Color::White => PyColor::White,
            Color::Black => PyColor::Black,
        },
        role: match p.role {
            Role::King   => PyRole::King,
            Role::Queen  => PyRole::Queen,
            Role::Rook   => PyRole::Rook,
            Role::Bishop => PyRole::Bishop,
            Role::Knight => PyRole::Knight,
            Role::Pawn   => PyRole::Pawn,
        },
    })).collect()
}