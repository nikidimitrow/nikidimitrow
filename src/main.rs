use std::io;
use rand::Rng;

fn main() {
    println!("Guess the number");
    let secret_number = rand::thread_rng().gen_range(1..=100);

    print!("Secret number is: {}", secret_number);

    print!("Please, input your guess: ");

    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    print!("You gess is: {}", guess);
}
