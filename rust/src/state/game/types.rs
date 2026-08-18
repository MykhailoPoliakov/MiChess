use std::fmt;

pub type Pos = (i8,i8);
pub type Move = (Pos, Pos);



#[derive(Copy, Clone, PartialEq, Eq, Hash, Debug)]
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



#[derive(Clone)]
pub struct Board(
    pub [[Option<Piece>; 8]; 8]
);



impl std::ops::Index<Pos> for Board {
    type Output = Option<Piece>;
    fn index(&self, pos: Pos) -> &Self::Output {
        &self.0[pos.0 as usize][pos.1 as usize]
    }
}

impl std::ops::IndexMut<Pos> for Board {
    fn index_mut(&mut self, pos: Pos) -> &mut Self::Output {
        &mut self.0[pos.0 as usize][pos.1 as usize]
    }
}

impl fmt::Display for Board {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for row in &self.0 {
            for cell in row {
                match cell {
                    Some(piece) => write!(f, "{} ", piece)?,
                    None => write!(f, "__ ")?,
                }
            }
            writeln!(f)?;
        }
        Ok(())
    }
}



#[derive(Clone)]
pub struct Grid(pub [[Vec<(i8,i8)>;8];8]);

impl Grid {
    pub fn new() -> Self {
        Grid(std::array::from_fn(|_| std::array::from_fn(|_| Vec::new())))
    }

    pub fn clean(&mut self) {
        for row in self.0.iter_mut() {
            for cell in row.iter_mut() {
                cell.clear();
            }
        }
    }

    pub fn print(&self, name: &str) {
        println!("\n{}:", name);
        for row in self.0.iter() {
            for cell in row.iter() {
                print!("{:2} ", cell.len());
            }
            println!();
        }
        println!();
    }
}

impl std::ops::Index<Pos> for Grid {
    type Output = Vec<Pos>;
    fn index(&self, pos: Pos) -> &Self::Output {
        &self.0[pos.0 as usize][pos.1 as usize]
    }
}

impl std::ops::IndexMut<Pos> for Grid {
    fn index_mut(&mut self, pos: Pos) -> &mut Self::Output {
        &mut self.0[pos.0 as usize][pos.1 as usize]
    }
}




