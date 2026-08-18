use super::*;


pub const WP: Option<Piece> = Some(Piece { color: Color::White, role: Role::Pawn   });
pub const WR: Option<Piece> = Some(Piece { color: Color::White, role: Role::Rook   });
pub const WH: Option<Piece> = Some(Piece { color: Color::White, role: Role::Knight });
pub const WB: Option<Piece> = Some(Piece { color: Color::White, role: Role::Bishop });
pub const WQ: Option<Piece> = Some(Piece { color: Color::White, role: Role::Queen  });
pub const WK: Option<Piece> = Some(Piece { color: Color::White, role: Role::King   });
pub const BP: Option<Piece> = Some(Piece { color: Color::Black, role: Role::Pawn   });
pub const BR: Option<Piece> = Some(Piece { color: Color::Black, role: Role::Rook   });
pub const BH: Option<Piece> = Some(Piece { color: Color::Black, role: Role::Knight });
pub const BB: Option<Piece> = Some(Piece { color: Color::Black, role: Role::Bishop });
pub const BQ: Option<Piece> = Some(Piece { color: Color::Black, role: Role::Queen  });
pub const BK: Option<Piece> = Some(Piece { color: Color::Black, role: Role::King   });
pub const __: Option<Piece> = None;




pub const ALL_POS: [Pos; 64] = [
    (0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7),
    (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7),
    (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7),
    (3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7),
    (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7),
    (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7),
    (6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7),
    (7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7),
];

