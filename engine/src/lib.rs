mod model;
pub use model::*;

mod play;
mod update;
mod search;
mod display;







// for testing
pub fn timed<F, T>(f: F) -> T 
where F: FnOnce() -> T {
    let start = std::time::Instant::now();
    let result = f();
    println!("took: {:?}", start.elapsed());
    result
}
