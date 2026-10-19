 mod app;

#[allow(unused_imports)]
use engine;

// for testing
pub fn timed<F, T>(f: F) -> T 
where F: FnOnce() -> T {
    let start = std::time::Instant::now();
    let result = f();
    println!("took: {:?}", start.elapsed());
    result
}



fn main() {
    app::run()
}
