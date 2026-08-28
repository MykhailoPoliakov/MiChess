use super::*;


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

impl std::fmt::Display for Board {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
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
