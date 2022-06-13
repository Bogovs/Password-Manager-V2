function generate_password() {
   eel.password_gen();
}


eel.expose(insert);
function insert(password) {
   let pass_field = document.getElementById("password");
   pass_field.value = password;
}


function save_data() {
   let web_site = document.getElementById("website").value;
   let login = document.getElementById("login").value;
   let pass = document.getElementById("password").value;
   eel.save(web_site, login, pass);
}


eel.expose(show_notification);
function show_notification(message) {
   let notification_field = document.getElementById("notification");
   notification_field.innerHTML = message;
}


function show_list() {
   eel.show_list();
}


eel.expose(get_list);
function get_list(table) {
   let list_field = document.getElementById("list");
   list_field.innerHTML = table;
}


eel.expose(get_decrypt_field);
function get_decrypt_field(field) {
   let decrypt_field = document.getElementById("decrypt");
   decrypt_field.innerHTML = field;
}


function decrypt() {
   let encrypted_password = document.getElementById("decrypt_filed").value;
   eel.decrypt(encrypted_password);
}


function login() {
   let login_input_field = document.getElementById("login_input").value;
   eel.login(login_input_field);
}


eel.expose(enter_program);
function enter_program(body) {
   let working_space = document.getElementById("main");
   working_space.innerHTML = body;
}
