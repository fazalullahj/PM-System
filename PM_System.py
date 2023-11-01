from customtkinter import *
import mysql.connector as mysql
from tkinter import messagebox
from tkinter import ttk

root = CTk()
root.title("Parking Management System")
set_default_color_theme("color.json")
set_appearance_mode("light")
Heading = CTkFont(family="Arial Black", size=34, weight="bold")
Bfont = CTkFont(family="Arial", size=19, weight="bold")

Standard = CTkFont(family="Verdana", size=19, weight="normal")
root.geometry("450x450")


def auth():
    global con, cursor
    try:
        password = auth_entry.get()
        con = mysql.connect(host="localhost", user="root", password=password)
        cursor = con.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS pmsystem;")
        cursor.execute("USE pmsystem;")

        # all tables creation-->
        # user details
        cursor.execute(
            "create table if not exists user_details(uname varchar(25) primary key, password varchar(25));"
        )
        cursor.execute(
            "create table if not exists parkinginfo(pID int(20) , carID varchar(20) primary key, price float(10,2), entry_time datetime , exit_time datetime);"
        )
        cursor.execute(
            "create table if not exists history(ID int(20) primary key,pID int(20) , carID varchar(20), price float(10,2), entry_time datetime , exit_time datetime ); "
        )
        if con.is_connected():
            auth_frame.destroy()
            sign_frame.pack(expand=True, fill="both", padx=20, pady=20)
            sign_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
            return con, cursor
    except Exception as e:
        if (
            str(e)
            == "1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)"
        ):
            messagebox.showerror(
                "Failed Authentication", "Wrong password for Mysql! Try Again"
            )
        else:
            print(e)
            messagebox.showerror("Error", f"Unexpected Error. \n Error:{e}")


currentUser = ""


def sign_in():
    cursor.execute("select * from user_details;")
    if len(cursor.fetchall()) == 0:
        messagebox.showerror("Error", "No users registered. Register first!")
    else:
        global currentRole, currentUser
        sign_frame.destroy()
        sign_in_frame.pack(expand=True, fill="both", padx=20, pady=20)
        sign_in_frame.place(in_=root, anchor="center", relx=0.5, rely=0.5)
        uname_label = CTkLabel(master=sign_in_frame, text="Username", font=Standard)
        password_label = CTkLabel(master=sign_in_frame, text="Password", font=Standard)
        uname_label.pack(pady=3)
        uname_entry = CTkEntry(master=sign_in_frame, font=Standard)
        uname_entry.pack()
        password_label.pack()
        password_entry = CTkEntry(master=sign_in_frame, show="•", font=Standard)
        password_entry.pack()

        def submit():
            uname = uname_entry.get()
            password = password_entry.get()
            try:
                cursor.execute(f"select * from user_details where uname='{uname}'")
                row = cursor.fetchone()
                if row is not None and password == row[1]:
                    global currentUser
                    currentUser = uname
                    sign_in_label = CTkLabel(
                        master=menu_frame,
                        text=f"Signed in as {currentUser.capitalize()} ",
                        font=Standard,
                    )
                    sign_in_label.pack()
                    menu_frame.pack(expand=True, fill="both", padx=20, pady=20)
                    menu_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
                    sign_in_frame.destroy()
                    start_btn.pack(pady=5)
                    end_btn.pack(pady=5)
                    view_btn.pack(pady=5)
            except Exception as e:
                print(e)
                print("Error!")
                quit()

        sign_in_submit = CTkButton(
            master=sign_in_frame, text="Submit", command=submit, font=Bfont
        )
        sign_in_submit.pack(pady=10)


def sign_up():
    global currentUser
    sign_frame.destroy()
    sign_up_frame.pack(expand=True, fill="both", padx=20, pady=20)
    sign_up_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
    uname_label = CTkLabel(master=sign_up_frame, text="New Username", font=Standard)
    password_label = CTkLabel(master=sign_up_frame, text="Password", font=Standard)
    uname_label.pack()
    uname_entry = CTkEntry(master=sign_up_frame, font=Standard)
    uname_entry.pack(pady=5)
    password_label.pack()
    password_entry = CTkEntry(master=sign_up_frame, show="•", font=Standard)
    password_entry.pack(pady=10)

    def submit():
        uname = uname_entry.get()
        password = password_entry.get()
        try:
            if uname != "" and password != "":
                cursor.execute(
                    f"INSERT INTO user_details (uname,password) VALUES ('{uname}','{password}');"
                )
                con.commit()

                currentUser = uname

                sign_up_frame.destroy()
                sign_in()
        except Exception as e:
            messagebox.showerror("Error", f"Username not available \n {e}")

    sign_up_submit = CTkButton(sign_up_frame, text="Submit", command=submit, font=Bfont)
    sign_up_submit.pack(pady=20)


def start():
    start_win = CTk()
    start_win.geometry("300x300")
    start_win.title("Start")

    start_frame = CTkFrame(master=start_win, fg_color="transparent")
    start_frame.pack(expand=True, fill="both", padx=20, pady=20)
    start_frame.place(in_=start_win, anchor="c", relx=0.5, rely=0.5)
    carID_entry = CTkEntry(master=start_frame, font=Standard)
    price_entry = CTkEntry(master=start_frame, font=Standard)
    carID_label = CTkLabel(master=start_frame, text="Vehicle ID", font=Standard)
    price_label = CTkLabel(master=start_frame, text="Price per hour : 2 AED", font=Standard)
    start_btn.configure(state="disabled")
    carID_label.pack()
    carID_entry.pack()
    price_label.pack()

    def submit():
        cursor.execute("select * from parkinginfo")
        if len(cursor.fetchall()) == 0:
            pID = 1
        else:
            cursor.execute("select pID from parkinginfo order by pID desc limit 1;")
            pID = int(cursor.fetchall()[0][0]) + 1
        carID = carID_entry.get()
        price = 2
        try:
            cursor.execute(
                f"insert into parkinginfo(pID,carID,price,entry_time) values({pID}, '{carID}',{price}, NOW());"
            )

            con.commit()
            messagebox.showinfo(
                "Successful",
                f"Started Parking for Vehicle : {carID} at parking spot: {pID}",
            )
        except Exception as e:
            messagebox.showerror("Error", "Vehicle already entered.")

    start_button = CTkButton(
        master=start_frame, text="Start", command=submit, font=Bfont
    )
    start_button.pack(pady=5)
    start_win.mainloop()
def view():
    query = "SELECT * FROM history;"
    cursor.execute(query)
    allhistorys = cursor.fetchall()
    column_names = ["ID","Plot No.","Vehicle ID", "Price","Entry Time","Exit time"]
    if len(allhistorys) == 0:
        messagebox.showerror("Error", "No history available")
    else:
        data_view = CTk()
        data_view.title("View history")
        data_view.geometry("700x300")
        tree = ttk.Treeview(master=data_view, columns=column_names, show="headings")

        for col in column_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for history in allhistorys:
            tree.insert("", "end", values=history)

        scrollbar = ttk.Scrollbar(data_view, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(fill="both", expand=True)
        if len(allhistorys) > 20:
            scrollbar.pack(side="right", fill="y")

        data_view.mainloop()

def end():
    end_win = CTk()
    end_win.title("End")
    end_win.geometry("650x350")
    end_frame = CTkFrame(master=end_win, fg_color="transparent")

    ID_label = CTkLabel(master=end_frame, text="Vehicle ID:", font=Standard)
    ID_label.pack()

    cursor.execute("SELECT carID FROM parkinginfo")
    allIDs = [row[0] for row in cursor.fetchall()]
    ID_var = StringVar(master=end_frame, value="Select Vehicle ID")
    ID_menu = CTkOptionMenu(master=end_frame, values=allIDs, variable=ID_var)
    ID_menu.pack(pady=10)
    output_frame = CTkFrame(master=end_frame, fg_color="transparent")
    end_label = CTkLabel(master=output_frame, text="", font=("Verdana", 16))
    cost_label = CTkLabel(
        master=output_frame, text=f"", font=("Arial Black", 24, "bold")
    )
    end_label.pack(pady=5)
    cost_label.pack()

    def submit():
        carID = ID_var.get()
        cursor.execute(
            f"select entry_time,exit_time,price from parkinginfo where carID = '{carID}'"
        )

        try:
            entry_time, exit_time, price = cursor.fetchone()
            cursor.execute(
                f'update parkinginfo set exit_time = NOW() where carID = "{carID}";'
            )
            con.commit()
            cursor.execute(
                f"select entry_time,exit_time,price from parkinginfo where carID = '{carID}'"
            )
            entry_time, exit_time, price = cursor.fetchone()
            output_frame.configure(
                fg_color="#F0E4CE",
                corner_radius=22,
                border_width=2,
                border_color="#E2C5A8",
            )
            end_label.configure(
                text=f"The vehicle with ID: {carID} \n entered at : {entry_time} and \nexited at : {exit_time}.\n",
                font=Standard,
            )
            end_label.pack()
            time_difference = exit_time - entry_time
            from datetime import datetime

            hours = time_difference.total_seconds() / 3600.0
            cost = price * round(hours)

            cost_label.configure(text=f"Cost : {cost} AED")
            try:
                cursor.execute("select max(ID) from history")
                key = cursor.fetchone()[0] + 1
            except Exception as e:
                print(e)
                key = 1
            cursor.execute(f"select pID,carID,price,entry_time from parkinginfo where carID = '{carID}'")
            row = cursor.fetchone()
            pID,carID,price,entry_time,= row[0],row[1],row[2],row[3]
            
            cursor.execute(f"insert into history values({key},{pID},'{carID}',{price},'{entry_time}',NOW())")
            con.commit()
            cursor.execute(f"DELETE from parkinginfo where carID = '{carID}'")
            con.commit()
            return
        except Exception as e:
            messagebox.showerror("Error", f"Not found \n{e}")

    end_button = CTkButton(master=end_frame, text="End", command=submit, font=Bfont)
    end_button.pack(pady=5)
    output_frame.pack(ipadx=20, ipady=12, expand=True, fill="y")
    end_frame.pack(expand=True, fill="both", padx=20, pady=20)
    end_frame.place(in_=end_win, anchor="c", relx=0.5, rely=0.5)
    end_win.mainloop()


auth_frame = CTkFrame(master=root, fg_color="transparent")
auth_frame.pack(expand=True, fill="both", padx=20, pady=50)
auth_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
auth_label = CTkLabel(
    master=auth_frame, text="MySQL Password", font=Standard, padx=10, pady=10
)
auth_label.pack()
auth_entry = CTkEntry(master=auth_frame, show="•", font=("Verdana", 20))
auth_entry.pack()
auth_button = CTkButton(
    master=auth_frame,
    text="Submit",
    command=auth,
    font=Standard,
    corner_radius=180,
)
auth_button.pack(pady=20, padx=5, ipadx=2, ipady=5)
auth_frame.pack()

sign_frame = CTkFrame(master=root, width=300, height=300, fg_color="transparent")
sign_in_btn = CTkButton(master=sign_frame, text="Sign in", command=sign_in, font=("Arial", 25, "bold"))
sign_in_btn.pack(pady=10, padx=30)
sign_up_btn = CTkButton(master=sign_frame, text="Sign up", command=sign_up, font=("Arial", 25, "bold"))
sign_up_btn.pack(pady=10, padx=30)

# sign IN
sign_in_frame = CTkFrame(master=root, fg_color="transparent")
sign_in_h1 = CTkLabel(master=sign_in_frame, text="Sign in", font=Heading)
sign_in_h1.pack()

# sign UP
sign_up_frame = CTkFrame(master=root, fg_color="transparent")
sign_up_h1 = CTkLabel(master=sign_up_frame, text="Sign up", font=Heading)
sign_up_h1.pack()

# menu
menu_frame = CTkFrame(master=root, fg_color="transparent")
end_btn = CTkButton(master=menu_frame, text="End Parking Time", command=end, font=("Arial", 25, "bold"))
start_btn = CTkButton(
    master=menu_frame, text="Start Parking Time", command=start,font=("Arial", 25, "bold")
)
view_btn = CTkButton(
    master=menu_frame, text="View History", command=view,font=("Arial", 25, "bold")
)
root.mainloop()
