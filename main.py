import tkinter as Tk
from tkinter import Label, Button, Frame, Entry, ttk
import json

class mainDraw:
    def __init__(self) -> None:
        self.root = Tk.Tk()
        self.root.geometry('400x600')
        self.root.title('The Funny App')

        # Configure ttk style
        style = ttk.Style()
        style.theme_use('clam')

        self.panel_frame = Frame(self.root)
        self.panel_frame.grid(row=0, column=0, rowspan=3, columnspan=3, padx=10, pady=10)

        # Create two buttons
        self.button1 = ttk.Button(self.root, text="Add", command=self.actionAdd)
        self.button2 = ttk.Button(self.root, text="Remove", command=self.actionRemove)

        # Place the buttons at the bottom, spanning across the window
        self.button1.grid(row=4, column=0, padx=5, pady=5, sticky='ew')
        self.button2.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

        # Configure column weights to ensure buttons span across the window
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Display saved data
        self.display_saved_data()

    def display_saved_data(self):
        for widget in self.panel_frame.winfo_children():
            widget.destroy()

        try:
            with open("saved.json", "r") as file:
                saved_data = json.load(file)
        except FileNotFoundError:
            saved_data = []

        if saved_data == []:
            addLabel = Label(self.panel_frame, text='Add a new entry by pressing the Add button', font=("Helvetica", 12, "bold"))
            addLabel.grid(row=1, column=0, sticky='n')

        row = 0
        for entry in saved_data:
            title, description = entry
            entry_frame = Frame(self.panel_frame, bd=2, relief="groove", padx=5, pady=5)
            entry_frame.grid(row=row, column=0, pady=5, sticky='ew')

            title_label = Label(entry_frame, text=f"{title}", font=("Helvetica", 14, "bold"))
            title_label.grid(row=0, column=0, sticky='w')

            desc_label = Label(entry_frame, text=f"{description}", font=("Helvetica", 12))
            desc_label.grid(row=1, column=0, sticky='w')

            row += 1

    def actionAdd(self):
        # Create a new top-level window (popup window)
        self.x = 400
        self.y = 250
        popup = Tk.Toplevel(self.root)
        popup.geometry(f'{self.x}x{self.y}')
        popup.title('Popup Window')

        # Add a label with text
        label = Label(popup, text="Enter your text:", font=("Helvetica", 12))
        label.grid(row=0, column=0, columnspan=2, pady=5)

        # Add a title textbox
        title_label = Label(popup, text="Title", font=("Helvetica", 10))
        title_label.grid(row=1, column=0, pady=5, padx=5, sticky='w')
        self.title = Entry(popup, font=("Helvetica", 10))
        self.title.grid(row=1, column=1, pady=5, padx=5, sticky='we')

        # Add description textbox
        desc_label = Label(popup, text="Description", font=("Helvetica", 10))
        desc_label.grid(row=2, column=0, pady=5, padx=5, sticky='w')
        self.desc = Entry(popup, font=("Helvetica", 10))
        self.desc.grid(row=2, column=1, pady=5, padx=5, sticky='we')

        # Add a button to save the input and close the popup
        save_button = ttk.Button(popup, text="Save", command=lambda: self.save_input(popup))
        save_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Add a button to close the popup window
        close_button = ttk.Button(popup, text="Close", command=popup.destroy)
        close_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Configure column weights to ensure entry fields span across the window
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_columnconfigure(1, weight=1)

    def save_to_json(self, title, description):
        try:
            with open("saved.json", "r") as file:
                saved_data = json.load(file)
        except FileNotFoundError:
            saved_data = []

        saved_data.append([title, description])

        with open("saved.json", "w") as file:
            json.dump(saved_data, file)

    def save_input(self, popup):
        # Get the text from the textbox
        title = self.title.get()
        description = self.desc.get()

        # Save to file
        self.save_to_json(title, description)

        # Update display with the new data
        self.display_saved_data()

        # Close the popup window
        popup.destroy()

    def actionRemove(self):
        try:
            with open("saved.json", "r") as file:
                saved_data = json.load(file)
        except FileNotFoundError:
            saved_data = []
        
        self.x = 400
        savedLen = len(saved_data)
        if savedLen > 3:
            self.y = 300 + 80*(savedLen - 3)
        else: 
            self.y = 300

        popup = Tk.Toplevel(self.root)
        popup.geometry(f'{self.x}x{self.y}')
        popup.title('Removing Window')

        label = Label(popup, text="Choose which one to delete:")
        label.grid(row=0, column=0, columnspan=2, pady=5)

        def remove_entry(index):
            del saved_data[index]
            with open("saved.json", "w") as file:
                json.dump(saved_data, file)
            # Update the display after removing
            self.display_saved_data()
            # Close the popup after removing
            popup.destroy()

        row = 1
        for index, entry in enumerate(saved_data):
            title, description = entry
            entry_frame = Frame(popup, bd=2, relief="groove", padx=5, pady=5)
            entry_frame.grid(row=row, column=0, columnspan=10, pady=5, sticky='ew')

            title_label = Label(entry_frame, text=f"{title}", font=("Helvetica", 13, "bold"))
            title_label.grid(row=0, column=0, sticky='w')

            remove_button = ttk.Button(popup, text="Remove", command=lambda idx=index: remove_entry(idx))
            remove_button.grid(row=row, column=7, padx=5, pady=5, sticky='e')

            row += 1

        # Add a button to close the popup window
        close_button = ttk.Button(popup, text="Close", command=popup.destroy)
        close_button.grid(row=row, column=0, columnspan=2, pady=5)
if __name__ == "__main__":
    app = mainDraw()
    app.root.mainloop()