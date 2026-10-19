use super::*;

impl App {
    pub(super) fn render_search(&self, ui: &mut egui::Ui, pos: egui::Pos2) -> () {
        let painter: &egui::Painter = ui.painter();

        

        if let Some(eval) = &self.game.search.eval(self.game.state.player) {
            painter.rect_filled(
                egui::Rect::from_min_size(pos,
                egui::vec2(self.square_size / 2.0, self.square_size * 8.0)),
                0.0, egui::Color32::WHITE,
            );

            match eval {
                Eval::Value(value) => {
                    painter.rect_filled(
                        egui::Rect::from_min_size(pos,
                        egui::vec2(self.square_size / 2.0, self.square_size / 2.0 + (self.square_size * 3.5) * (-value+1.0))),
                        0.0, egui::Color32::GRAY,
                    );
                    painter.text(
                        pos + egui::vec2( self.square_size * 0.05, self.square_size * 7.0),
                        egui::Align2::LEFT_TOP,
                        format!("{:.2}", value),
                        egui::FontId::new(16.0, egui::FontFamily::Proportional),
                        egui::Color32::BLACK,
                    );

                },
                Eval::Mate(value) => {
                    let length: f32;
                    let text: String;
                    if *value > 0 {
                        length = self.square_size / 4.0;
                        text = format!("w M{}", value);
                    } else {
                        length = self.square_size * 7.5;
                        text = format!("b M{}", -value);
                    }

                    painter.rect_filled(
                        egui::Rect::from_min_size(pos,
                        egui::vec2(self.square_size / 2.0, length)),
                        0.0, egui::Color32::GRAY,
                    );
                    painter.text(
                        pos + egui::vec2( 0.0, self.square_size * 7.0),
                        egui::Align2::LEFT_TOP,
                        text,
                        egui::FontId::new(16.0, egui::FontFamily::Proportional),
                        egui::Color32::BLACK,
                    );
                }
            }

            

        }


    }
}