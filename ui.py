import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import requests

class DepartmentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Department Management System developed by Hamayoun")

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window size and position
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

        self.departments = []

        # Create and set up GUI components with styling
        self.label = tk.Label(root, text="Departments of IUB", font=("Helvetica", 16, "bold"), fg="#333333")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(root, bg="#f0f0f0", selectbackground="#cce5ff", font=("Helvetica", 12))
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.add_button = tk.Button(root, text="Add Department", command=self.add_department, bg="#4caf50", fg="white", font=("Helvetica", 12))
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Department", command=self.delete_department, bg="#f44336", fg="white", font=("Helvetica", 12))
        self.delete_button.pack(pady=5)

        self.clear_button = tk.Button(root, text="Clear Screen", command=self.clear_screen, bg="#ff9800", fg="white", font=("Helvetica", 12))
        self.clear_button.pack(pady=5)

        self.view_button = tk.Button(root, text="View Departments", command=self.get_departments_from_api, bg="#2196f3", fg="white", font=("Helvetica", 12))
        self.view_button.pack(pady=5)

    def add_department(self):
        department_name = simpledialog.askstring("Input", "Enter department name:")
        if department_name:
            self.add_department_to_api(department_name)

    def add_department_to_api(self, department_name):
        data = {'name': department_name}
        response = requests.post('http://127.0.0.1:5000/departments', json=data)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Department added successfully!")
            self.get_departments_from_api()
        else:
            messagebox.showerror("Error", "Failed to add department")

    def delete_department(self):
        self.delete_department_in_api()

    def delete_department_in_api(self):
        if self.departments:
            department_id = self.departments[-1]['_id']  # Assuming you store _id in the response
            response = requests.delete(f'http://127.0.0.1:5000/departments/{department_id}')
            if response.status_code == 200:
                messagebox.showinfo("Success", "Last entered department deleted successfully!")
                self.get_departments_from_api()
            else:
                messagebox.showerror("Error", "Failed to delete department")
        else:
            messagebox.showwarning("Warning", "No departments to delete.")

    def clear_screen(self):
        self.departments = []
        self.view_departments()

    def view_departments(self):
        self.listbox.delete(0, tk.END)
        for department in self.departments:
            self.listbox.insert(tk.END, department['name'])

    def get_departments_from_api(self):
        response = requests.get('http://127.0.0.1:5000/departments')
        if response.status_code == 200:
            self.departments = response.json()['departments']
            self.view_departments()
        else:
            messagebox.showerror("Error", "Failed to fetch departments from API")

if __name__ == "__main__":
    root = tk.Tk()
    app = DepartmentManagementSystem(root)
    root.mainloop()
