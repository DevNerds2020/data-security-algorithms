#[macro_use] extern crate rocket;

#[get("/rout?<value>")]
fn rout(value: &str) -> String {
    let len = value.len();
    println!("{}",value);
    len.to_string()
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![rout])
}
