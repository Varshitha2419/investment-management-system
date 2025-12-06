from tkinter import *
from tkinter import messagebox
import os
import dashboard

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x250")

        # Username
        Label(self.root, text="Username:", font=("times new roman", 14)).pack(pady=5)
        self.txt_user = Entry(self.root, font=("times new roman", 14))
        self.txt_user.pack(pady=5)

        # Password
        Label(self.root, text="Password:", font=("times new roman", 14)).pack(pady=5)
        self.txt_pass = Entry(self.root, show="*", font=("times new roman", 14))
        self.txt_pass.pack(pady=5)

        # Remember Me checkbox
        self.remember_var = IntVar()
        self.chk_remember = Checkbutton(self.root, text="Remember Me", variable=self.remember_var)
        self.chk_remember.pack(pady=5)

        # Login button
        btn_login = Button(self.root, text="Login", command=self.login, font=("times new roman", 14), bg="#4caf50", fg="white")
        btn_login.pack(pady=10)

        # Auto-fill if remembered
        self.load_remembered()

    def load_remembered(self):
        """Load saved username and password if Remember Me was checked"""
        if os.path.exists("remember.txt"):
            with open("remember.txt", "r") as f:
                data = f.read().splitlines()
                if len(data) == 2:
                    self.txt_user.insert(0, data[0])
                    self.txt_pass.insert(0, data[1])
                    self.remember_var.set(1)

    def login(self):
        username = self.txt_user.get()
        password = self.txt_pass.get()

        if username == "admin" and password == "admin123":
            messagebox.showinfo("Login Success", "Welcome to Inventory Management System")
            
            # Save credentials if Remember Me is checked
            if self.remember_var.get() == 1:
                with open("remember.txt", "w") as f:
                    f.write(username + "\n" + password)
            else:
                if os.path.exists("remember.txt"):
                    os.remove("remember.txt")

            self.root.destroy()
            root = Tk()
            dashboard.IMS(root)
            root.mainloop()

        else:
            messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()
