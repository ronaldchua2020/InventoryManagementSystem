# import all the modules
from tkinter import *
from tkmacosx import Button
from PIL import ImageTk, Image
import mysql.connector
from mysql.connector import Error
import tkinter.messagebox
from configparser import ConfigParser

# Read the configuration file
config_object = ConfigParser()
config_object.read("config.ini")

# Get the user credentials
userinfo = config_object["USERINFO"]
serverinfo = config_object["SERVER CONFIG"]

conn = mysql.connector.connect(host=serverinfo["host"],
                               database=serverinfo["database"],
                               user=userinfo["user"],
                               password=userinfo["password"])
mycursor = conn.cursor()
mycursor.execute("SELECT Max(id) from inventory")
result = mycursor.fetchall()
for r in result:
    id = r[0]


class Database:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.heading = Label(master, text="Add in the database", font='arial 40 bold', fg='steel blue')
        self.heading.place(x=400, y=0)

        # Include background image

        # lables  for the window
        self.name_l = Label(master, text="Enter Product Name", font='arial 18 bold')
        self.name_l.place(x=0, y=70)

        self.quantity_l = Label(master, text="Enter Stocks", font='arial 18 bold')
        self.quantity_l.place(x=0, y=120)

        # enteries for window

        self.name_e = Entry(master, width=25, font='arial 18 bold')
        self.name_e.place(x=380, y=70)

        self.quantity_e = Entry(master, width=25, font='arial 18 bold')
        self.quantity_e.place(x=380, y=120)

        # button to add to the database
        self.btn_add = Button(master, text='Add to Management System', width=200, height=50, bg='blue', fg='white',
                              command=self.get_items)
        self.btn_add.place(x=470, y=220)

        # button to clear data

        self.btn_clear = Button(master, text="Clear All Fields", width=180, height=50, bg='red', fg='white',
                                command=self.clear_all)
        self.btn_clear.place(x=200, y=220)

        # button to exit the program
        self.btn_clear = Button(master, text="Exit", width=180, height=50, bg='red', fg='white',
                                command=root.quit)
        self.btn_clear.place(x=200, y=300)



        # text box for the log
        self.tbBox = Text(master, width=60, height=18)
        self.tbBox.config(font='bold')

        self.tbBox.place(x=800, y=70)
        self.tbBox.insert(END, "Current total number of books are : " + str(id))

        self.master.bind('<Return>', self.get_items)
        self.master.bind('<Up>', self.clear_all)

    def get_items(self, *args, **kwargs):
        # get from entries
        self.name = self.name_e.get()
        self.stock = self.quantity_e.get()

        # dynamic entries
        if self.name == '' or self.stock == '':
            tkinter.messagebox.showinfo("Error", "Please Fill all the entries.")
        else:
            mycursor.execute("INSERT INTO inventory (name,stock) VALUES(%s,%s)", [self.name, self.stock])
            conn.commit()
            # textbox insert
            self.tbBox.insert(END, "\n\nInserted " + str(self.name) + " into the database with the quantity of " + str(
                self.stock))
            tkinter.messagebox.showinfo("Success", "Successfully added to the book management system")

    def clear_all(self, *args, **kwargs):
        num = id + 1
        self.name_e.delete(0, END)
        self.quantity_e.delete(0, END)


root = Tk()
b = Database(root)
root.geometry("1366x768+0+0")
root.title("Add books into the Inventory Management System")
frame = Frame(root, width=200, height=200)
frame.pack()
frame.place(x=400, y=400)
img = ImageTk.PhotoImage(Image.open("images/books_blue_background.jpg"))
image_label = Label(frame, image=img)
image_label.pack()
root.mainloop()
