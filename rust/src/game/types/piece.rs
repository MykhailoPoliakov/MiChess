use std::fmt;

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

impl fmt::Display for Color {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Color::White => write!(f, "W"),
            Color::Black => write!(f, "B"),
        }
    }
}



// Role

#[derive(Copy, Clone, PartialEq, Debug)]
pub enum Role {
    King,
    Queen,
    Rook,
    Bishop,
    Knight,
    Pawn,
}

impl fmt::Display for Role {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Role::Pawn   => write!(f, "P"),
            Role::Knight => write!(f, "H"),
            Role::Bishop => write!(f, "B"),
            Role::Rook   => write!(f, "R"),
            Role::Queen  => write!(f, "Q"),
            Role::King   => write!(f, "K"),
        }
    }
}



// Piece

#[derive(Copy, Clone, PartialEq, Debug)]
pub struct Piece {
    pub color: Color, 
    pub role: Role,
}


impl fmt::Display for Piece {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}{}", self.color, self.role)
    }
}

