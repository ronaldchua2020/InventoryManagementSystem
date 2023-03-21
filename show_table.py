# import all the modules
import tkinter as tk
from tkinter import ttk, LEFT, RIGHT, CENTER, BOTTOM

import tkmacosx
from tkmacosx import Button
import mysql.connector
from configparser import ConfigParser

def view():
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

    mycursor.execute("SELECT * from inventory ")
    results = mycursor.fetchall()

    for row in results:
        print(row)
        tree.insert("", tk.END, values=row)

    conn.close()


def clear_all():
    for i in tree.get_children():
        tree.delete(i)


root = tk.Tk()
root.geometry("1366x768")
root.title("Show All Books in Inventory Management System")
tree = ttk.Treeview(root, column=("c1", "c2", "c3"), show='headings')
vertical_scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview())
vertical_scrollbar.pack(side='right', fill='y')
tree.configure(yscrollcommand=vertical_scrollbar.set)
tree.column("#1", anchor=tk.CENTER)

tree.heading("#1", text="ID")

tree.column("#2", anchor=tk.CENTER)

tree.heading("#2", text="Book")

tree.column("#3", anchor=tk.CENTER )

tree.heading("#3", text="Quantity")
tree.pack()

button = Button(root, text="Display data", width=200, height=50, command=view)

button.pack(side=LEFT, padx=100, pady=100)

# button for clearing data
button = Button(root, text="Clear data", width=200, height=50, command=clear_all)

button.pack(side=LEFT, padx=100, pady=100)

# button for closing
exit_button = Button(root, text="Exit", width=200, height=50, command=root.quit)

exit_button.pack(side=RIGHT, padx=100, pady=100)

root.mainloop()
