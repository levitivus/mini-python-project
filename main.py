import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
from PIL import Image, ImageTk
import os


class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ustaad Hotel - Self-Service")
        self.root.geometry("800x600")
        self.root.configure(bg="#f8e8c1")  # Warm background color
        self.root.resizable(True, True)

        # Fullscreen toggle
        self.is_fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)

        # Show Welcome Popup
        self.show_welcome_popup()

        # Restaurant Menu with images
        self.menu = {
            "Margherita Pizza": ("pizza.jpg", 250),
            "BBQ Chicken Pizza": ("bbq_pizza.jpg", 350),
            "Veg Burger": ("veg_burger.jpg", 150),
            "Chicken Burger": ("chicken_burger.jpg", 180),
            "Pasta Alfredo": ("pasta.jpg", 220),
            "Grilled Sandwich": ("sandwich.jpg", 120),
            "Caesar Salad": ("salad.jpg", 160),
            "French Fries": ("fries.jpg", 100),
            "Chocolate Brownie": ("brownie.jpg", 140),
            "Coke (500ml)": ("coke.jpg", 50)
        }

        self.orders = {}  # Stores user orders {dish: (quantity, time_left)}
        self.order_status = "Order Not Placed"

        # UI Setup
        self.create_ui()

    def show_welcome_popup(self):
        """Displays a welcome message when the app starts."""
        messagebox.showinfo("Welcome", "Welcome To Ustaad Hotel!")

    def toggle_fullscreen(self, event=None):
        """Toggles between fullscreen and halfscreen."""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.root.attributes("-fullscreen", True)
        else:
            self.root.attributes("-fullscreen", False)
            self.root.geometry("800x600")

    def create_ui(self):
        """Creates the UI layout with enhanced design."""
        title_label = tk.Label(self.root, text="Ustaad Hotel - Self-Service", font=("Arial", 20, "bold"), bg="#f8e8c1",
                               fg="#8B0000")
        title_label.pack(pady=10)

        # Menu Frame
        frame_menu = tk.LabelFrame(self.root, text="🍽 Menu", font=("Arial", 12, "bold"), bg="#f8e8c1", fg="#8B0000",
                                   padx=10, pady=10)
        frame_menu.pack(pady=5, fill="both")

        self.menu_listbox = tk.Listbox(frame_menu, selectmode=tk.SINGLE, width=40, height=10, font=("Arial", 11),
                                       bg="#ffffff", fg="#333333")
        for dish in self.menu.keys():
            self.menu_listbox.insert(tk.END, dish)
        self.menu_listbox.pack(side=tk.LEFT, padx=5)
        self.menu_listbox.bind("<<ListboxSelect>>", self.show_food_image)

        self.qty_spinbox = tk.Spinbox(frame_menu, from_=1, to=10, width=5, font=("Arial", 11))
        self.qty_spinbox.pack(pady=5)

        add_button = ttk.Button(frame_menu, text="➕ Add to Order", command=self.add_to_order)
        add_button.pack(pady=5)

        # Image display for food
        self.image_label = tk.Label(self.root, bg="#f8e8c1")
        self.image_label.pack()

        # Order Summary
        frame_order = tk.LabelFrame(self.root, text="📜 Your Order", font=("Arial", 12, "bold"), bg="#f8e8c1",
                                    fg="#8B0000", padx=10, pady=10)
        frame_order.pack(pady=5, fill="both")

        self.order_text = tk.Text(frame_order, height=7, width=50, state="disabled", font=("Arial", 11), bg="#ffffff",
                                  fg="#333333")
        self.order_text.pack()

        # Order Status & Actions
        frame_actions = tk.Frame(self.root, bg="#f8e8c1")
        frame_actions.pack(pady=10)

        self.status_label = tk.Label(frame_actions, text=f"🟢 Status: {self.order_status}", font=("Arial", 12, "italic"),
                                     bg="#f8e8c1", fg="#8B0000")
        self.status_label.grid(row=0, column=0, padx=10)

        ttk.Button(frame_actions, text="📦 Place Order", command=self.place_order).grid(row=0, column=1, padx=5)
        ttk.Button(frame_actions, text="💳 Checkout", command=self.checkout).grid(row=0, column=2, padx=5)
        ttk.Button(frame_actions, text="❌ Cancel Order", command=self.cancel_order).grid(row=0, column=3, padx=5)

    def show_food_image(self, event):
        """Displays the image of the selected food item."""
        try:
            selected_index = self.menu_listbox.curselection()
            if not selected_index:
                return  # No selection, do nothing

            selected_dish = self.menu_listbox.get(selected_index)
            img_path = self.menu[selected_dish][0]

            if not os.path.exists(img_path):  # Ensure image exists
                messagebox.showwarning("Image Missing", f"Image for {selected_dish} not found: {img_path}")
                return

            img = Image.open(img_path)
            img = img.resize((200, 150), Image.LANCZOS)  # ✅ NEW
            self.food_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.food_image)
            self.image_label.image = self.food_image  # Prevent garbage collection
        except Exception as e:
            print(f"Error loading image: {e}")  # Debugging output

    def add_to_order(self):
        """Adds selected item to the order list."""
        try:
            selected_dish = self.menu_listbox.get(self.menu_listbox.curselection())
            quantity = int(self.qty_spinbox.get())

            if selected_dish in self.orders:
                self.orders[selected_dish] = (self.orders[selected_dish][0] + quantity, random.randint(180, 240))
            else:
                self.orders[selected_dish] = (quantity, random.randint(180, 240))

            self.update_order_display()
        except:
            messagebox.showwarning("Selection Error", "Please select a dish before adding.")

    def update_order_display(self):
        """Updates the order text box with the current order summary."""
        self.order_text.config(state="normal")
        self.order_text.delete(1.0, tk.END)
        for dish, (qty, time_left) in self.orders.items():
            self.order_text.insert(tk.END, f"✅ {dish} x {qty} (⏳ {time_left // 60}:{time_left % 60} min left)\n")

        self.order_text.config(state="disabled")

    def place_order(self):
        """Marks the order as placed."""
        if not self.orders:
            messagebox.showwarning("No Order", "Please add items before placing an order.")
            return

        self.order_status = "Order Placed ✅"
        self.status_label.config(text=f"🟢 Status: {self.order_status}")
        messagebox.showinfo("Order Confirmation", "Your order has been placed successfully!")

    def checkout(self):
        """Calculates total bill and displays it."""
        if not self.orders:
            messagebox.showwarning("No Order", "You have not placed any order yet.")
            return

        total_bill = sum(self.menu[dish][1] * qty for dish, (qty, _) in self.orders.items())

        messagebox.showinfo("Checkout", f"Your total bill is: Rs {total_bill}\nThank you for dining with us!")

        # Clear orders after checkout
        self.orders.clear()
        self.update_order_display()
        self.status_label.config(text="🟢 Status: Order Completed ✅")

    def cancel_order(self):
        """Allows order cancellation within 1 minute."""
        for dish, (_, time_left) in self.orders.items():
            if time_left >= 180:
                del self.orders[dish]
                messagebox.showinfo("Cancellation", f"Order for {dish} has been cancelled.")
                self.update_order_display()
                return

        messagebox.showwarning("Cannot Cancel", "Orders cannot be cancelled after 1 minute!")


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()
