use super::*;

impl App {
    pub(super) fn render_search(&self, ui: &mut egui::Ui, pos: egui::Pos2) -> () {
        let painter: &egui::Painter = ui.painter();

        if let Some(result) = &self.game.search.result {
            painter.rect_filled(
                egui::Rect::from_min_size(pos,
                egui::vec2(self.square_size / 2.0, self.square_size * 8.0)),
                0.0, egui::Color32::WHITE,
            );

            match result.eval {
                Eval::Value(value) => {
                    painter.rect_filled(
                        egui::Rect::from_min_size(pos,
                        egui::vec2(self.square_size / 2.0, (self.square_size * 4.0) * (-value+1.0))),
                        0.0, egui::Color32::GRAY,
                    );

                },
                _ => {}
            }

            

        }


    }
}