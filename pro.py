import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

# CSV file name
csv_file = 'billing_data.csv'

# Initialize main window
root = tk.Tk()
root.title("XYZ Store Billing System")
root.geometry("800x600")
root.config(bg="lightyellow")

# --------- Functions ---------
items = []

def add_item():
    try:
        name = item_name.get()
        qty = int(quantity.get())
        price = float(price_per_unit.get())
        total = qty * price
        items.append([name, qty, price, total])
        
        update_items_display()
        item_name.delete(0, tk.END)
        quantity.delete(0, tk.END)
        price_per_unit.delete(0, tk.END)
    except:
        messagebox.showerror("Error", "Invalid item data")

def update_items_display():
    item_listbox.delete(0, tk.END)
    subtotal = 0
    for item in items:
        item_listbox.insert(tk.END, f"{item[0]:<15}{item[1]:<10}{item[2]:<15}{item[3]:<10}")
        subtotal += item[3]
    gst_amount = round(subtotal * 0.18, 2)
    total_amount = round(subtotal + gst_amount, 2)
    try:
        paid_amt = float(paid.get())
    except:
        paid_amt = 0
    balance_amt = round(paid_amt - total_amount, 2)
    
    subtotal_var.set(f"{subtotal:.2f}")
    gst_var.set(f"{gst_amount:.2f}")
    total_var.set(f"{total_amount:.2f}")
    balance_var.set(f"{balance_amt:.2f}")

def generate_bill():
    if not items:
        messagebox.showwarning("Empty", "No items added!")
        return

    data = [
        ["Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ["Customer Name", customer_name.get()],
        ["Phone", phone.get()],
        ["Email", email.get()],
        [],
        ["Item", "Quantity", "Price/unit", "Total"]
    ]
    data += items
    data += [
        [],
        ["Subtotal", subtotal_var.get()],
        ["GST", gst_var.get()],
        ["Total", total_var.get()],
        ["Paid", paid.get()],
        ["Balance", balance_var.get()]
    ]
    
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        writer.writerow([])  # extra empty row

    messagebox.showinfo("Success", "Bill saved successfully!")

def clear_all():
    customer_name.delete(0, tk.END)
    phone.delete(0, tk.END)
    email.delete(0, tk.END)
    paid.delete(0, tk.END)
    item_name.delete(0, tk.END)
    quantity.delete(0, tk.END)
    price_per_unit.delete(0, tk.END)
    item_listbox.delete(0, tk.END)
    items.clear()
    subtotal_var.set("")
    gst_var.set("")
    total_var.set("")
    balance_var.set("")

# --------- UI Layout ---------

# Title
tk.Label(root, text="XYZ Store Billing System", font=("Arial", 20, "bold"), bg="lightyellow").pack(pady=10)

# Customer details
frame1 = tk.Frame(root, bg="lightyellow")
frame1.pack()

tk.Label(frame1, text="Customer Name:", bg="lightyellow").grid(row=0, column=0, padx=5, sticky='e')
customer_name = tk.Entry(frame1)
customer_name.grid(row=0, column=1, padx=5)

tk.Label(frame1, text="Phone:", bg="lightyellow").grid(row=0, column=2, padx=5, sticky='e')
phone = tk.Entry(frame1)
phone.grid(row=0, column=3, padx=5)

tk.Label(frame1, text="Email:", bg="lightyellow").grid(row=1, column=0, padx=5, sticky='e')
email = tk.Entry(frame1)
email.grid(row=1, column=1, padx=5)

# Item details
frame2 = tk.Frame(root, bg="lightyellow")
frame2.pack(pady=10)

tk.Label(frame2, text="Item Name:", bg="lightyellow").grid(row=0, column=0, padx=5, sticky='e')
item_name = tk.Entry(frame2)
item_name.grid(row=0, column=1, padx=5)

tk.Label(frame2, text="Quantity:", bg="lightyellow").grid(row=0, column=2, padx=5, sticky='e')
quantity = tk.Entry(frame2)
quantity.grid(row=0, column=3, padx=5)

tk.Label(frame2, text="Price per unit:", bg="lightyellow").grid(row=0, column=4, padx=5, sticky='e')
price_per_unit = tk.Entry(frame2)
price_per_unit.grid(row=0, column=5, padx=5)

tk.Button(frame2, text="Add Item", command=add_item, bg="lightblue").grid(row=0, column=6, padx=5)

# Item list
tk.Label(root, text="Items Added:", font=("Arial", 12, "bold"), bg="lightyellow").pack()
item_listbox = tk.Listbox(root, width=80)
item_listbox.pack()

# Billing summary
frame3 = tk.Frame(root, bg="lightyellow")
frame3.pack(pady=10)

subtotal_var = tk.StringVar()
gst_var = tk.StringVar()
total_var = tk.StringVar()
balance_var = tk.StringVar()

tk.Label(frame3, text="Subtotal: ₹", bg="lightyellow").grid(row=0, column=0, sticky='e')
tk.Label(frame3, textvariable=subtotal_var, bg="lightyellow").grid(row=0, column=1, sticky='w')

tk.Label(frame3, text="GST (18%): ₹", bg="lightyellow").grid(row=0, column=2, sticky='e')
tk.Label(frame3, textvariable=gst_var, bg="lightyellow").grid(row=0, column=3, sticky='w')

tk.Label(frame3, text="Total: ₹", bg="lightyellow").grid(row=1, column=0, sticky='e')
tk.Label(frame3, textvariable=total_var, bg="lightyellow").grid(row=1, column=1, sticky='w')

tk.Label(frame3, text="Paid: ₹", bg="lightyellow").grid(row=1, column=2, sticky='e')
paid = tk.Entry(frame3)
paid.grid(row=1, column=3)

tk.Label(frame3, text="Balance: ₹", bg="lightyellow").grid(row=2, column=0, sticky='e')
tk.Label(frame3, textvariable=balance_var, bg="lightyellow").grid(row=2, column=1, sticky='w')

# Buttons
frame4 = tk.Frame(root, bg="lightyellow")
frame4.pack(pady=10)

tk.Button(frame4, text="Generate Bill", command=generate_bill, bg="lightgreen", width=15).grid(row=0, column=0, padx=10)
tk.Button(frame4, text="Clear", command=clear_all, bg="orange", width=15).grid(row=0, column=1, padx=10)
tk.Button(frame4, text="Exit", command=root.quit, bg="red", fg="white", width=15).grid(row=0, column=2, padx=10)

root.mainloop()
