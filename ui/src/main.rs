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



fn main() -> () { 

    // let mut sum = 0;
    // for i in LIST {
    //     sum += i;
    // }
    // println!("{}", sum);

    app::run();
}
