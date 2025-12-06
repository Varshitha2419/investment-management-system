from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import time
import os

class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1366x768+0+0")
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print = 0

        # ========== Title ==========
        title = Label(self.root, text="Inventory Management System", font=("times new roman", 30, "bold"), bg="#033054", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=60)

        logout_btn = Button(self.root, text="Logout", command=self.logout, font=("times new roman", 15, "bold"), bg="yellow", fg="black", cursor="hand2")
        logout_btn.place(x=1220, y=10, height=40, width=120)

        # ======== Date and Time =========
        self.lbl_clock = Label(self.root, text=f"Welcome to Inventory Management System\t\t Date: {time.strftime('%d-%m-%Y')}\t Time: {time.strftime('%H:%M:%S')}", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=60, relwidth=1, height=30)
        self.update_time()

        # ======== Product Frame =========
        productFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        productFrame1.place(x=10, y=100, width=410, height=550)

        pTitle = Label(productFrame1, text="All Products", font=("goudy old style", 20, "bold"), bg="#262626", fg="white")
        pTitle.pack(side=TOP, fill=X)

        # ===== Search Bar =====
        self.var_search = StringVar()
        lbl_search = Label(productFrame1, text="Search Product | By Name", font=("times new roman", 15, "bold"), bg="white", fg="green")
        lbl_search.place(x=5, y=60)

        txt_search = Entry(productFrame1, textvariable=self.var_search, font=("times new roman", 15), bg="lightyellow")
        txt_search.place(x=5, y=90, width=180, height=28)

        btn_search = Button(productFrame1, text="Search", command=self.search, font=("times new roman", 15), bg="#2196f3", fg="white", cursor="hand2")
        btn_search.place(x=190, y=90, width=100, height=28)

        btn_show_all = Button(productFrame1, text="Show All", command=self.show, font=("times new roman", 15), bg="#083531", fg="white", cursor="hand2")
        btn_show_all.place(x=300, y=90, width=100, height=28)

        # ===== Product Table =====
        productFrame2 = Frame(productFrame1, bd=3, relief=RIDGE)
        productFrame2.place(x=5, y=130, width=398, height=385)

        scrolly = Scrollbar(productFrame2, orient=VERTICAL)
        scrollx = Scrollbar(productFrame2, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(productFrame2, columns=("pid", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid", text="P ID")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("qty", text="Quant")
        self.ProductTable.heading("status", text="Status")
        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width=40)
        self.ProductTable.column("name", width=100)
        self.ProductTable.column("price", width=60)
        self.ProductTable.column("qty", width=60)
        self.ProductTable.column("status", width=80)
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        lbl_note = Label(productFrame1, text="Note: 'Enter 0 Quantity to remove product from the Cart'", font=("goudy old style", 12), bg="white", fg="red")
        lbl_note.pack(side=BOTTOM, fill=X)

        # ======== Customer Frame ========
        customerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        customerFrame.place(x=420, y=100, width=530, height=70)
        cTitle = Label(customerFrame, text="Customer Details", font=("goudy old style", 15, "bold"), bg="lightgray")
        cTitle.pack(side=TOP, fill=X)

        lbl_name = Label(customerFrame, text="Name", font=("times new roman", 13), bg="white")
        lbl_name.place(x=5, y=35)
        txt_name = Entry(customerFrame, textvariable=StringVar(), font=("times new roman", 13), bg="lightyellow")
        txt_name.place(x=60, y=35, width=180)

        lbl_contact = Label(customerFrame, text="Contact No.", font=("times new roman", 13), bg="white")
        lbl_contact.place(x=260, y=35)
        txt_contact = Entry(customerFrame, textvariable=StringVar(), font=("times new roman", 13), bg="lightyellow")
        txt_contact.place(x=360, y=35, width=150)

        # ======== Cart Frame ========
        cartFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        cartFrame.place(x=420, y=180, width=530, height=360)
        self.var_qty = StringVar()

        lbl_p_name = Label(cartFrame, text="Product Name", font=("times new roman", 15, "bold"), bg="white")
        lbl_p_name.place(x=5, y=5)
        self.var_p_name = StringVar()
        txt_p_name = Entry(cartFrame, textvariable=self.var_p_name, font=("times new roman", 15), bg="lightgray", state="readonly")
        txt_p_name.place(x=150, y=5, width=150)

        lbl_price = Label(cartFrame, text="Price per Qty", font=("times new roman", 15, "bold"), bg="white")
        lbl_price.place(x=5, y=45)
        self.var_price = StringVar()
        txt_price = Entry(cartFrame, textvariable=self.var_price, font=("times new roman", 15), bg="lightgray", state="readonly")
        txt_price.place(x=150, y=45, width=150)

        lbl_qty = Label(cartFrame, text="Quantity", font=("times new roman", 15, "bold"), bg="white")
        lbl_qty.place(x=5, y=85)
        txt_qty = Entry(cartFrame, textvariable=self.var_qty, font=("times new roman", 15), bg="lightyellow")
        txt_qty.place(x=150, y=85, width=150)

        btn_clear = Button(cartFrame, text="Clear", command=self.clear_cart, font=("times new roman", 15, "bold"), bg="lightgray")
        btn_clear.place(x=320, y=85, width=80, height=28)

        btn_add = Button(cartFrame, text="Add | Update", command=self.add_update_cart, font=("times new roman", 15, "bold"), bg="#2196f3", fg="white")
        btn_add.place(x=410, y=85, width=100, height=28)

        self.cartTable = ttk.Treeview(cartFrame, columns=("pid", "name", "price", "qty"), show="headings")
        self.cartTable.heading("pid", text="P ID")
        self.cartTable.heading("name", text="Name")
        self.cartTable.heading("price", text="Price")
        self.cartTable.heading("qty", text="Qty")
        self.cartTable.pack(fill=BOTH, expand=1)

        # ======== Bill Frame ========
        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billFrame.place(x=960, y=100, width=400, height=460)
        bTitle = Label(billFrame, text="Customer Bill Area", font=("goudy old style", 20, "bold"), bg="#262626", fg="white")
        bTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set, font=("Courier New", 11))
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # ======== Bill Menu Buttons ========
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(x=960, y=560, width=400, height=130)

        self.lbl_amnt = Label(billMenuFrame, text="Bill Amount\n0", font=("times new roman", 15, "bold"), bg="#3f51b5", fg="white")
        self.lbl_amnt.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(billMenuFrame, text="Discount\n[5%]", font=("times new roman", 15, "bold"), bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay = Label(billMenuFrame, text="Net Pay\n0", font=("times new roman", 15, "bold"), bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=150, height=70)

        btn_print = Button(billMenuFrame, text="Print", command=self.print_bill, font=("times new roman", 15, "bold"), bg="#4caf50", fg="white")
        btn_print.place(x=2, y=80, width=100, height=40)

        btn_clear_all = Button(billMenuFrame, text="Clear All", command=self.clear_all, font=("times new roman", 15, "bold"), bg="#f44336", fg="white")
        btn_clear_all.place(x=110, y=80, width=120, height=40)

        btn_generate = Button(billMenuFrame, text="Generate Bill", command=self.generate_bill, font=("times new roman", 15, "bold"), bg="#009688", fg="white")
        btn_generate.place(x=240, y=80, width=150, height=40)

    # ==============================================
    def update_time(self):
        now = time.strftime("%H:%M:%S")
        date = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {date}\t Time: {now}")
        self.root.after(1000, self.update_time)

    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = self.ProductTable.item(f)
        row = content["values"]
        self.var_p_name.set(row[1])
        self.var_price.set(row[2])

    def add_update_cart(self):
        pid = self.ProductTable.item(self.ProductTable.focus())["values"][0]
        pname = self.var_p_name.get()
        price = float(self.var_price.get())
        qty = int(self.var_qty.get())

        if qty == 0:
            self.cart_list = [item for item in self.cart_list if item[0] != pid]
        else:
            found = False
            for item in self.cart_list:
                if item[0] == pid:
                    item[3] = qty
                    found = True
                    break
            if not found:
                self.cart_list.append([pid, pname, price, qty])

        self.show_cart()

    def show_cart(self):
        for i in self.cartTable.get_children():
            self.cartTable.delete(i)
        for item in self.cart_list:
            self.cartTable.insert("", END, values=item)

    def bill_top(self):
        self.txt_bill_area.delete("1.0", END)
        self.txt_bill_area.insert(END, "\tXYZ-Inventory")
        self.txt_bill_area.insert(END, "\n Phone No. 9899459288 , Delhi-110053")
        self.txt_bill_area.insert(END, f"\n{'='*42}")
        self.txt_bill_area.insert(END, "\nCustomer Bill")
        self.txt_bill_area.insert(END, f"\n{'='*42}\n")
        self.txt_bill_area.insert(END, "Product Name         Qty     Price\n")
        self.txt_bill_area.insert(END, f"{'-'*42}\n")

    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                price_each = float(row[2])
                qty_sold = int(row[3])
                line_total = price_each * qty_sold

                self.txt_bill_area.insert(END, f"{name:20}{qty_sold:>5}   Rs.{line_total:>8.2f}\n")

                cur.execute("SELECT qty FROM product WHERE pid=?", (pid,))
                stock_row = cur.fetchone()
                if stock_row:
                    current_stock = int(stock_row[0])
                    new_stock = current_stock - qty_sold
                    status = "Active" if new_stock > 0 else "Inactive"
                    cur.execute("UPDATE product SET qty=?, status=? WHERE pid=?", (new_stock, status, pid))
                    con.commit()
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def bill_bottom(self):
        total = sum(float(row[2]) * int(row[3]) for row in self.cart_list)
        discount = total * 0.05
        net_pay = total - discount

        self.lbl_amnt.config(text=f"Bill Amount\nRs.{total:.2f}")
        self.lbl_net_pay.config(text=f"Net Pay\nRs.{net_pay:.2f}")

        self.txt_bill_area.insert(END, f"{'-'*42}\n")
        self.txt_bill_area.insert(END, f"Bill Amount\t\tRs.{total:.2f}\n")
        self.txt_bill_area.insert(END, f"Discount [5%]\t\tRs.{discount:.2f}\n")
        self.txt_bill_area.insert(END, f"Net Pay\t\tRs.{net_pay:.2f}\n")
        self.txt_bill_area.insert(END, f"{'='*42}\n")

    def generate_bill(self):
        if not self.cart_list:
            messagebox.showerror("Error", "Cart is empty!", parent=self.root)
            return
        self.bill_top()
        self.bill_middle()
        self.bill_bottom()

    def print_bill(self):
        messagebox.showinfo("Print", "Printing Bill...")

    def clear_cart(self):
        self.var_p_name.set("")
        self.var_price.set("")
        self.var_qty.set("")

    def clear_all(self):
        self.cart_list.clear()
        self.show_cart()
        self.txt_bill_area.delete("1.0", END)
        self.lbl_amnt.config(text="Bill Amount\n0")
        self.lbl_net_pay.config(text="Net Pay\n0")

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert("", END, values=row)
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name LIKE ?", ('%' + self.var_search.get() + '%',))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert("", END, values=row)
                else:
                    messagebox.showinfo("Info", "No record found", parent=self.root)
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def logout(self):
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
