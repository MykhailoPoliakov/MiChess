use super::*;


#[derive(Clone)]
pub struct Board( pub [Option<Piece>; 64] );



impl std::ops::Index<Pos> for Board {
    type Output = Option<Piece>;
    fn index(&self, pos: Pos) -> &Self::Output {
        &self.0[pos as usize]
    }
}

impl std::ops::IndexMut<Pos> for Board {
    fn index_mut(&mut self, pos: Pos) -> &mut Self::Output {
        &mut self.0[pos as usize]
    }
}

impl std::fmt::Display for Board {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for (i, square) in self.0.iter().enumerate() {
            match square {
                Some(piece) => write!(f, "{} ", piece)?,
                None => write!(f, "__ ")?,
            }
            if (i + 1) % 8 == 0 {
                writeln!(f)?;
            }
        }
        writeln!(f)?;
        Ok(())
    }
}
