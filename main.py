from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_input.delete(0, END)  # this will clear the password field on every new password generation
    # Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for char in range(randint(8, 10))]
    password_symbols = [choice(symbols) for sym in range(randint(2, 4))]
    password_numbers = [choice(numbers) for num in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers  # join all the list into single list
    shuffle(password_list)  # this will shuffle the password list

    password = "".join(password_list)  # this will take all the char from the list and make a string
    password_input.insert(0, password)  # this will fill the password field with generated password
    pyperclip.copy(password)  # this will copy the generated password

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    # collect all user data into respective variable
    web_data = web_input.get()
    email_data = email_input.get()
    password_data = password_input.get()
    new_data = {
        web_data: {
            "email": email_data,
            "password": password_data
        }
    }

    # checking all the required field is empty or not
    if len(web_data) < 1 or len(email_data) < 1 or len(password_data) < 1:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")

    else:
        # showing all the user data and waiting for user confirmation
        is_ok = messagebox.askokcancel(title=web_data,
                                       message=f"These are the details entered \nEmail: {email_data}\nPassword: "
        
                                               f"{password_data}\nIs it ok to Save ?")
        # if user ok with their data then save into a file
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
                    # Updating the old data with new data
                    data.update(new_data)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                with open("data.json", "w") as data_file:
                    # Save the new data into data_file
                    json.dump(data, data_file, indent=4)
            finally:
                web_input.delete(0, END)
                password_input.delete(0, END)
                web_input.focus()
                messagebox.showinfo(title="Saved", message="Your data is Successfully Saved")


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = web_input.get()
    try:
        with open("data.json", "r") as data_file:
            # Reading data
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found!!!")
    finally:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\n\nPassword: {password}")
        else:
            messagebox.showwarning(title="Error", message=f"No details for {website} exists")

        web_input.delete(0, END)
        password_input.delete(0, END)
        web_input.focus()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=30, padx=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="D:\Python\password-manager\logo2.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0, pady=10)

# website label
web_label = Label(text="Website:")
web_label.grid(column=0, row=1)
web_label.config(pady=8)

# Search button
search_btn = Button(text="Search")
search_btn.grid(column=2, row=1)
search_btn.config(padx=8, relief=RIDGE, command=find_password)

# email label
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
email_label.config(pady=10)

# password label
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_label.config(pady=10)

# Website Entry
web_input = Entry(width=36)
web_input.focus()
web_input.grid(column=1, row=1)

# Email Entry
email_input = Entry(width=49)
email_input.insert(0, "devsambhav50@gmail.com")
email_input.grid(column=1, row=2, columnspan=2)

# password box
password_input = Entry(width=36)
password_input.grid(column=1, row=3)

# generate button
generate_button = Button(text="Generate")
generate_button.config(command=generate_password)
generate_button.grid(row=3, column=2)
generate_button.config(padx=5, relief=RIDGE)

# add button
add_button = Button(text="Add", width=41)
add_button.config(command=save_password)
add_button.grid(column=1, row=4, columnspan=2)
add_button.config(pady=5, padx=5, relief=RIDGE)

window.mainloop()

