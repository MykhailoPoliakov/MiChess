use super::*;


const WEIGHTS: [[f32; 128]; 10] = [
    [0.1; 128],
    [0.2; 128],
    [0.3; 128],
    [0.4; 128],
    [0.5; 128],
    [0.6; 128],
    [0.7; 128],
    [0.8; 128],
    [0.9; 128],
    [1.0; 128],
];



type FeatureVector = [f32; 128];





// temporary holder of already done calculations on first hidden layer
pub struct Transformer (FeatureVector, FeatureVector);

impl Transformer {
    pub fn new(game: &Game, bias: FeatureVector) -> Self {
        let mut transformer = Transformer(bias, bias);

        for pos in 0..64 {
            if let Some(piece) = game.board[pos] {
                // for every piece
                let features = get_features(piece, pos, game.king_pos);
                transformer.add(features);
            }
        }
        transformer
    }

    pub fn play(&mut self, mv: Move, game: &Game) -> () {
        if game.board[mv.1].unwrap().role == Role::King {
            return
        }

        // self.add(get_features(piece, pos, game.king_pos));

    }

    // add a feature
    fn add(&mut self, features: [usize;2]) -> () {
        // get weights
        let white_feature_vec = &WEIGHTS[features[0]];
        let black_feature_vec = &WEIGHTS[features[1]];

        for i in 0..128 {
            self.0[i] += white_feature_vec[i];
            self.1[i] += black_feature_vec[i];
        }
    }

    // remove a feature
    fn remove(&mut self, features: [usize;2]) -> () {
       // get weights
        let white_feature_vec = &WEIGHTS[features[0]];
        let black_feature_vec = &WEIGHTS[features[1]];

        for i in 0..128 {
            self.0[i] -= white_feature_vec[i];
            self.1[i] -= black_feature_vec[i];
        }
    }
}



fn get_features(piece: Piece, pos: Pos, king_pos: [Pos;2]) -> [usize;2] {
    let pos_index: usize = (pos as usize + (pos as usize *8) ) *12;

    let white_king_pos_index: usize = ((king_pos[0] as usize + (king_pos[0] as usize *8)) *12) *64;
    let black_king_pos_index: usize = ((king_pos[1] as usize + (king_pos[1] as usize *8)) *12) *64;

    return [piece.color as usize + (piece.role as usize)*2 + pos_index + white_king_pos_index,
        piece.color as usize + (piece.role as usize)*2 + pos_index + black_king_pos_index]
}




pub struct Nnue {
    feature_weights: Vec<i16>,
    feature_bias: Vec<i16>,

    hidden0_weights: Vec<i16>,
    hidden0_bias: Vec<i16>,

    hidden1_weights: Vec<i16>,
    hidden1_bias: Vec<i16>,

    output_weights: Vec<i16>,
    output_bias: i32,
}


