// Color
#[derive(Copy, Clone, PartialEq, Debug)]
pub enum Color {
    White = 0,
    Black = 1
}

impl Color {
    pub fn opp(&self) -> Color {
        match self {
            Color::White => Color::Black,
            Color::Black => Color::White,
        }
        
    }
}


// Role
#[derive(Copy, Clone, PartialEq)]
pub enum Role {
    King,
    Queen,
    Rook,
    Bishop,
    Knight,
    Pawn,
}


// Piece
#[derive(Copy, Clone, PartialEq)]
pub struct Piece {
    pub color: Color, 
    pub role: Role,
}

