from customtkinter import *
import mysql.connector as mysql
from tkinter import messagebox
from tkinter import ttk

root = CTk()
root.title("Parking Management System")
set_default_color_theme("green")
set_appearance_mode("light")
Heading = CTkFont(family="Arial Black", size=28, weight="bold")
Bfont = CTkFont(family="Arial", size=16, weight="bold")
Standard = CTkFont(family="Arial", size=15, weight="bold")
root.geometry('450x450')

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
        # product
        cursor.execute(
            "create table if not exists parkinginfo(pID int(20) , carID int(15) primary key, price float(10,2), entry_time datetime , exit_time datetime);"
        )
        if con.is_connected():
            auth_frame.destroy()
            sign_frame.pack(expand=True, fill="both", padx=20, pady=20)
            sign_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
            return con, cursor
    except Exception as e:
        if str(e) == "1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)":
            messagebox.showerror("Failed Authentication","Wrong password for Mysql! Try Again")
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
                        text=f"Signed in ⁛ {currentUser.capitalize()} ⁛",
                        font=Standard,
                    )
                    sign_in_label.pack()
                    menu_frame.pack(expand=True, fill="both", padx=20, pady=20)
                    menu_frame.place(in_=root, anchor="c", relx=0.5, rely=0.5)
                    sign_in_frame.destroy()
                    start_btn.pack(pady=5)
                    end_btn.pack(pady=5)
            except Exception as e:
                print(e)
                print("Error!")
                quit()

        sign_in_submit = CTkButton(
            master=sign_in_frame, text="Submit", command=submit, font=Standard
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
            if (
                uname != ""
                and password != ""
            ):
                cursor.execute(
                    f"INSERT INTO user_details (uname,password) VALUES ('{uname}','{password}');"
                )
                con.commit()
                
                currentUser = uname

                sign_up_frame.destroy()
                sign_in()
        except Exception as e:
            messagebox.showerror("Error", f"Username not available \n {e}")

    sign_up_submit = CTkButton(sign_up_frame, text="Submit", command=submit)
    sign_up_submit.pack(pady=20)

def start():
    start_win = CTk()
    start_win.geometry("200x300")
    start_win.title("Start")

    start_frame = CTkFrame(master = start_win, fg_color = "transparent")
    start_frame.pack(expand=True, fill="both", padx=20, pady=20)
    start_frame.place(in_=start_win, anchor="c", relx=0.5, rely=0.5)
    carID_entry = CTkEntry(master = start_frame,font = Standard)
    price_entry = CTkEntry(master = start_frame,font = Standard)
    carID_label = CTkLabel(master = start_frame,text = "Vehicle ID",font = Standard)
    price_label = CTkLabel(master = start_frame,text = "Price per hour",font = Standard)
    carID_label.pack()
    carID_entry.pack()
    price_label.pack()
    price_entry.pack()
    def submit():
        
        cursor.execute("select * from parkinginfo")
        if len(cursor.fetchall()) == 0:
            pID = 1
        else:    
            cursor.execute("select pID from parkinginfo order by pID desc limit 1;")
            pID = int(cursor.fetchall()[0][0]) + 1
        carID = carID_entry.get()
        price = float(price_entry.get())
        try:
            cursor.execute(f"insert into parkinginfo(pID,carID,price,entry_time) values({pID}, {carID},{price}, NOW());")
            
            con.commit()
            messagebox.showinfo("Successful",f"Started Parking for Vehicle : {carID}")
        except Exception as e:
            messagebox.showerror("Error","Vehicle already entered.")
        

    start_button = CTkButton(master = start_frame,text = 'Start',command = submit, font = Bfont)
    start_button.pack(pady =5)
    start_win.mainloop()
def end():
    end_win = CTk()
    end_win.title("End")
    end_win.geometry("650x250")
    end_frame = CTkFrame(master = end_win, fg_color = "transparent")
    end_frame.pack(expand=True, fill="both", padx=20, pady=20)
    end_frame.place(in_=end_win, anchor="c", relx=0.5, rely=0.5)
    carID_entry = CTkEntry(master = end_frame,font = Standard)
    carID_label = CTkLabel(master = end_frame,text = "Vehicle ID",font = Standard)
    carID_label.pack()
    carID_entry.pack()
    def submit():
        carID = carID_entry.get()
        cursor.execute(f"select entry_time,exit_time,price from parkinginfo where carID = {carID}")
        entry_time,exit_time,price = cursor.fetchone()
        if exit_time is not None:
            messagebox.showerror("Already Exited",f"This vehicle has exited at {exit_time}")
        else: 
            try:
                cursor.execute(f'update parkinginfo set exit_time = NOW() where carID = {carID};')
                con.commit()
                cursor.execute(f"select entry_time,exit_time,price from parkinginfo where carID = {carID}")
                entry_time,exit_time,price = cursor.fetchone()

                end_label = CTkLabel(master = end_frame, text = f"The vehicle with ID: {carID} entered at {entry_time} and exited at : {exit_time}.",font = Standard)
                end_label.pack()
                time_difference = exit_time - entry_time
                from datetime import datetime
                hours = time_difference.total_seconds() / 3600.0
                cost = round((float(price)*hours),2)
            
                messagebox.showinfo("Success", "Exited")
                cost_label = CTkLabel(master = end_frame, text = f"Cost - {cost} AED",font=Bfont).pack()
            except Exception as e:
                messagebox.showerror("Error", "Not found")

    end_button = CTkButton(master = end_frame,text = 'End',command = submit, font = Bfont)
    end_button.pack(pady =5)
    
    
    end_win.mainloop()


auth_frame = CTkFrame(master=root, height=300, width=350, fg_color="transparent")
auth_frame.pack(expand=True, fill="y", padx=20, pady=50)
auth_frame.place(in_=root, anchor="center")
auth_label = CTkLabel(
    master=auth_frame, text="MySQL Password", font=Standard, padx=10, pady=10
)
auth_label.pack()
auth_entry = CTkEntry(master=auth_frame, show="•", font=("Arial", 20))
auth_entry.pack()
auth_button = CTkButton(
    master=auth_frame,
    text="Authenticate",
    command=auth,
    font=Standard,
    corner_radius=180,
)
auth_button.pack(pady=20, padx=5)
auth_frame.pack()

sign_frame = CTkFrame(master=root, width=300, height=300, fg_color="transparent")
sign_in_btn = CTkButton(master=sign_frame, text="Sign in", command=sign_in, font=Bfont)
sign_in_btn.pack(pady=10, padx=30)
sign_up_btn = CTkButton(master=sign_frame, text="Sign up", command=sign_up, font=Bfont)
sign_up_btn.pack(pady=10, padx=30)

# sign IN
sign_in_frame = CTkFrame(master=root, fg_color="transparent")
sign_in_h1 = CTkLabel(master=sign_in_frame, text="Sign in", font=Heading)
sign_in_h1.pack()

# sign UP
sign_up_frame = CTkFrame(master=root, fg_color="transparent")
sign_up_h1 = CTkLabel(master=sign_up_frame, text="Sign up", font=Heading)
sign_up_h1.pack()

#menu 
menu_frame = CTkFrame(master=root, fg_color="transparent")
end_btn = CTkButton(master=menu_frame, text="End Parking Time", command=end, font=Bfont)
start_btn = CTkButton(master=menu_frame, text="Start Parking Time", command=start, font=Bfont)
root.mainloop()
