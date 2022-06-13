import eel
import sqlite3
from cryptography.fernet import Fernet
import pyperclip
from random import randint, choice, shuffle

body = """
    <div id="center">
        <div id="img_align">
            <img src="logo2.png" width="162" height="200">
        </div>
        <div id="notification"></div>
        <br>
        <input id="website" type="text" placeholder="wedsite" required="">
        <br>
        <input id="login" type="email" placeholder="login" required="">
        <br>
        <input id="password" type="password" placeholder="password" required="">

        <br>
        <div id="gen_align">
            <button id="gen" onclick="generate_password()">Generate</button>
        </div>
        <br>
        <button id="save" onclick="save_data()">Save</button>
        <br>
        <div id="show_list_align">
            <button id="show_list" onclick="show_list()">Show_list</button>
        </div>
        <br>
        <div id="decrypt"></div>
        <br>
    </div>
    <div id="list_align">
        <div id="list"></div>
    </div>
"""


@eel.expose
def password_gen():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    pyperclip.copy(password)
    eel.insert(password)


def encrypt(password):
    key = b'fernet key in bytes'
    cipher = Fernet(key)

    password_as_bytes = str.encode(password)  # Convert string with password into bytes
    secured_password_bytes = cipher.encrypt(password_as_bytes)  # Ciphering our bytes password and get result also in bytes
    return secured_password_bytes.decode()  # Returning ciphered bytes password and convert it into string


@eel.expose
def decrypt(password):
    key = b'fernet key in bytes'
    cipher = Fernet(key)

    password_as_bytes = str.encode(password)  # Convert string with ciphered password into bytes
    decrypted_password_bytes = cipher.decrypt(password_as_bytes)  # Decrypting our bytes secured password and get result also in bytes
    pyperclip.copy(decrypted_password_bytes.decode())  # Returning decrypted bytes password and convert it into string


def enter_decrypt(password):
    key = b'fernet key in bytes'
    cipher = Fernet(key)

    password_as_bytes = str.encode(password)  # Convert string with ciphered password into bytes
    decrypted_password_bytes = cipher.decrypt(password_as_bytes)  # Decrypting our bytes secured password and get result also in bytes
    return decrypted_password_bytes.decode()


@eel.expose
def save(web_site, login, password):

    website = web_site.lower()
    email = login
    password = password
    enc_password = encrypt(password)

    connect = sqlite3.connect('info.db')
    cursor = connect.cursor()

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        eel.show_notification("You have the empty field")
    else:
        try:
            cursor.execute("INSERT INTO data VALUES (?, ?, ?)", (website, email, enc_password))
            connect.commit()
            eel.show_notification("Done!")
        except Exception as ex:
            eel.show_notification("This site is already exist")


@eel.expose
def show_list():
    connect = sqlite3.connect('info.db')
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT * FROM data")

        data = []
        while True:
            row = cursor.fetchone()
            if row == None:
                break

            temp_data = [row[0], row[1], row[2]]
            data.append(temp_data)

        # Create the html table
        table = "<table>\n"

        # Create the table's column headers
        table += "  <tr>\n"
        table += "    <th>Website</th>\n"
        table += "    <th>Login</th>\n"
        table += "    <th>Password</th>\n"
        table += "  </tr>\n"

        # Create the table's row data
        for line in data[1:]:
            table += "  <tr>\n"
            for column in line:
                table += "    <td>{0}</td>\n".format(column.strip())
            table += "  </tr>\n"

        table += "</table>"

        eel.get_decrypt_field('<input id="decrypt_filed" type="text" placeholder="encrypted password" required="">\n <button id="decrypt_btn" onclick="decrypt()">Decrypt and copy</button>')
        eel.get_list(table)

    except IndexError:
        eel.show_notification("Empty database")


@eel.expose
def login(input_password):

    connect = sqlite3.connect('info.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS data(
        website TEXT PRIMARY KEY,
        login TEXT,
        password TEXT
    )""")
    connect.commit()

    cursor.execute("SELECT * FROM data WHERE website = 'userlogpas'")
    password = cursor.fetchall()

    try:
        if input_password == enter_decrypt(password[0][2]):
            eel.enter_program(body)
        else:
            eel.show_notification("Wrong password")
    except IndexError:
        print(input_password)
        cursor.execute("INSERT INTO data VALUES (?, ?, ?)", ('userlogpas', 'login', encrypt(input_password)))
        connect.commit()
        eel.show_notification("User created")


eel.init("Interface")
eel.start("main.html", mode="chrome", block="False", position=(685, 180), size=(550, 700))
