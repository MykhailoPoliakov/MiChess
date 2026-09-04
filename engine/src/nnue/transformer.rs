use super::*;

type FeatureVector = [f32; 128];


// holds second layer info and updates it dinamically
pub struct Transformer (pub FeatureVector, pub FeatureVector);

impl Transformer {
    pub fn new(nnue: &Nnue, game: &Game) -> Self {
        let mut transformer = Transformer(nnue.feature_bias, nnue.feature_bias);

        for pos in 0..64 {
            if let Some(piece) = game.board[pos] {
                // for every piece
                transformer.add(nnue, get_features(piece, pos, game.king_pos));
            }
        }
        transformer
    }

    pub fn play(&mut self, nnue: &Nnue, game: &Game, played: PlayedMove) -> () {
        let played_piece = game.board[played.mv.1].unwrap();
        // if king move
        if played_piece.role == Role::King {
            *self = Transformer::new(nnue, game);
            return
        }
        // if captured
        if let Some(captured) = played.captured {
            self.remove(nnue, get_features(captured, played.mv.1, game.king_pos));
        }
        // if promotion
        if played.tp == MoveType::Promotion {
            let pawn = Piece { color: played_piece.color, role: Role::Pawn };
            self.remove(nnue, get_features(pawn, played.mv.0, game.king_pos));
            self.add(nnue, get_features(played_piece, played.mv.1, game.king_pos));
            return
        }
        // basic move
        self.remove(nnue, get_features(played_piece, played.mv.0, game.king_pos));
        self.add(nnue, get_features(played_piece, played.mv.1, game.king_pos));

    }





    pub fn undo(&mut self, nnue: &Nnue, game: &Game, unplayed: PlayedMove) -> () {
        let unplayed_piece = game.board[unplayed.mv.0].unwrap();
        // if king unmove
        if unplayed_piece.role == Role::King {
            *self = Transformer::new(nnue, game);
            return
        }
        // if captured
        if let Some(uncaptured) = unplayed.captured {
            self.add(nnue, get_features(uncaptured, unplayed.mv.1, game.king_pos));
        }
        // if promotion
        if unplayed.tp == MoveType::Promotion {
            let queen = Piece { color: unplayed_piece.color, role: Role::Queen };
            self.add(nnue, get_features(unplayed_piece, unplayed.mv.0, game.king_pos));
            self.remove(nnue, get_features(queen, unplayed.mv.1, game.king_pos));
            return
        }
        // basic move
        self.add(nnue, get_features(unplayed_piece, unplayed.mv.0, game.king_pos));
        self.remove(nnue, get_features(unplayed_piece, unplayed.mv.1, game.king_pos));
    }








    // add a feature
    fn add(&mut self, nnue: &Nnue, features: [usize;2]) -> () {
        // get weights
        let white = &nnue.feature_weights[features[0]];
        let black = &nnue.feature_weights[features[1]];

        for i in 0..128 {
            self.0[i] += white[i];
            self.1[i] += black[i];
        }
    }

    // remove a feature
    fn remove(&mut self, nnue: &Nnue, features: [usize;2]) -> () {
       // get weights
        let white = &nnue.feature_weights[features[0]];
        let black = &nnue.feature_weights[features[1]];

        for i in 0..128 {
            self.0[i] -= white[i];
            self.1[i] -= black[i];
        }
    }
}




// converts piece position to usize integer
fn get_features(piece: Piece, pos: Pos, king_pos: [Pos;2]) -> [usize;2] {
    let white_king_pos_index: usize = (king_pos[0] as usize)*64*12;
    let black_king_pos_index: usize = (king_pos[1] as usize)*64*12;

    let pos_index = pos as usize *12;
    let piece_index = piece.color as usize + piece.role as usize * 2;

    return [
        white_king_pos_index + pos_index + piece_index,
        black_king_pos_index + pos_index + piece_index,
    ]
}