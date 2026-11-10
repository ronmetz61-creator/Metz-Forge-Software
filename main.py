# ============================================================================================================
# Metz Forge Software
# Manufacturing Capacity Planner & Resource Scheduling
#
# Author: Ronald Metz
#
# Purpose:
# This application allows users to create, save, load, 
# and manage manufacturing projects. Future versions will
# include resource scheduling, dashboards, and reporting.
# ============================================================================================================


# =============================================================================================================
# IMPORTS
# =============================================================================================================
# Import the Python libraries required for the Metz Forge Application

import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# ===========================================================================================================
# MAIN APPLICATION
# Creates the application window, functions, and user interface.
# ===========================================================================================================
def main() -> None:
    """
    Create the main Metz Forge applicationwindow.
    
    This function initializes the application,
    builds the graphical user interface(GUI),
    and starts the program.
    """
    # -----------------------------------------------------------------------------------------------------
    # APPLICATION WINDOW
    # Configure the main Metz Forge window. 
    # -----------------------------------------------------------------------------------------------------
    root = tk.Tk()
    root.title("Metz Forge")
    root.geometry("1000x650")
    root.minsize(800, 500)

    # Store projects.json in th esame folder as main.py
    data_file = Path(__file__).with_name("projects.json")

# ===============================================================================================================
# PROJECT FUNCTIONS
# Functions used to create and delete projects. 
# ===============================================================================================================
    def delete_project(project_number, project_row):
        """
        Delete and existing project.
        
        Remove the selected project from the JSON file
        and remove it from the application window after
        the user confirms the deletion.
        """
        # Ask user to confirm before deleting the project. 
        confirmed = messagebox.askyesno(
            "Delete Project",
            f"Delete project {project_number}?",
            parent=root,
        )
        if not confirmed:
            return
        # Load the current project except the selected project.
        try:
            with open(data_file, "r") as file:
                projects = json.load(file)
        except FileNotFoundError:
            projects = []
        
        # Keep every project except selected project.
        projects = [
            project
            for project in projects
            if project["project_number"] != project_number
        ]

        # Save the updated project list. 
        with open(data_file, "w") as file:
            json.dump(projects, file, indent=4)

        # Remove the project row from the application window. 
        project_row.destroy()

        # Display the empty-project message when no projects remain. 
        if not project_container.winfo_children():
            message.pack(pady=40)
    def open_project(project_number: str, customer_name: str) -> None:
        print(f"Opening project {project_number} - {customer_name}")

    def create_project_card(project_number: str, customer_name: str) -> None:
        """
        Display one project as a card in the project container.
        """
        project_card = ttk.LabelFrame(
            project_container,
            text="",
            padding=15,
        )
        project_card.pack(
            fill="x",
            padx=15,
            pady=10,
            ipadx=10,
            ipady=10,
        )

        title_label = ttk.Label(
            project_card,
            text=f"📂{project_number} - {customer_name}",
            font=("Segoe UI", 16, "bold"),
            foreground="#005A9E",
            cursor="hand2",
        )
        title_label.pack(anchor="w")
        title_label.bind(
            "<Button-1>",
            lambda event: open_project(project_number, customer_name),
        )

        status_label = ttk.Label(
            project_card, 
            text="Status:           New",
            font=("Segoe UI", 10),
        )
        status_label.pack(anchor="w", pady=(5, 2))

        priority_label = ttk.Label(
            project_card,
            text="Priority:          Normal",
            font=("Segoe UI", 10),
        )
        priority_label.pack(anchor="w", pady=(0, 10))

        button_frame = ttk.Frame(project_card)
        button_frame.pack(fill="x", pady=(10, 0))

        delete_button = ttk.Button(
            button_frame,
            text="Delete",
            command=lambda: delete_project(
                project_number,
                project_card,
            ),
        )
        delete_button.pack(side="left")

        edit_button = ttk.Button(
            button_frame,
            text="Edit",
        )
        edit_button.pack(side="left", padx=5)

    def new_project():
        """
        Create a new project.
        
        Prompt the user for a project number and customer 
        name, save the project to the JSON file, and 
        display the project in the application
        """
        # Ask the user for a project number.
        project_number = simpledialog.askstring(
            "New Project",
            "Enter the project number:",
            parent=root
        )

        if project_number is None:
            return

        
        # Ask the user for customer name. 
        customer_name = simpledialog.askstring(
            "New Project",
            "Enter customer name:",
            parent=root
        )

        if customer_name is None:
            return

        # Store the new project information in a dictionary. 
        new_project_data = {
            "project_number": project_number,
            "customer_name": customer_name,
            }

        # Load existing projects before adding the new project. 
        try:
            with open(data_file, "r") as file:
                projects = json.load(file)
        except FileNotFoundError:
            projects = []

        projects.append(new_project_data)

        # Save the updated project list to projects.json
        with open(data_file, "w") as file:
            json.dump(projects, file, indent=4)
        
        # Hide the empty-project message.
        message.pack_forget()

        # Displays the new project as a card.
        create_project_card(
            project_number,
            customer_name,
        )

#---------------------------------------------------------------------------------------------------------
# APPLICATION HEADER
# Display the Application title and subtitle.
# --------------------------------------------------------------------------------------------------------
    title = ttk.Label(
        root,
        text="METZ-FORGE SOFTWARE",
        font=("Segoe UI", 24, "bold"),
    )
    title.pack(pady=(30, 5))

    subtitle = ttk.Label(
        root,
        text="Manufacturing Capacity Planning",
        font=("Segoe UI", 24)
    )
    subtitle.pack()
# --------------------------------------------------------------------------------------------------------
# PROJECT SECTION
# Create frame that holds the button, message, and project list.
# --------------------------------------------------------------------------------------------------------
    project_frame = ttk.LabelFrame(
        root, 
        text="Projects", 
        padding=20,
    )
    project_frame.pack(
        fill="both", 
        expand=True, 
        padx=30, pady=30,
    )
    # ----------------------------------------------------------------------------------------------------
    # CREATE PROJECT BUTTON
    # Open the New Project dialogs when clicked.
    # ----------------------------------------------------------------------------------------------------
    new_project_button = tk.Button(
        project_frame,
        text= "CREATE NEW PROJECT",
        command=new_project,
        bg="#F9163C",
        fg="white",
        activebackground="#EA2D0C",
        activeforeground="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        padx=18,
        pady=8,
        cursor="hand2",
    )

    new_project_button.pack(
        anchor="ne",
        padx=10,
        pady=(0, 10),
    )
    # -------------------------------------------------------------------------------------------------
    # PROJECT DISPLAY AREA
    # Show the default message and create the container for project rows.
    # -------------------------------------------------------------------------------------------------
    message = ttk.Label(
        project_frame,
        text="No Projects have been created.",
        font=("Segoe UI", 11),
    )
    message.pack(pady=40)
    project_container = ttk.Frame(project_frame)
    project_container.pack(fill="x", padx=10, pady=10)

    # --------------------------------------------------------------------------------------------------
    # LOAD SAVED PROJECTS
    # Read projects.json and display each saved project when the application restarts.
    # --------------------------------------------------------------------------------------------------
    try:
        with open(data_file, "r") as file:
            saved_projects = json.load(file)
    except FileNotFoundError:
        saved_projects = []

    if saved_projects:
        message.pack_forget()

        for saved_project in saved_projects:
           project_number = saved_project["project_number"]
           customer_name = saved_project["customer_name"]

           create_project_card(
               project_number,
               customer_name,
           )

    # ---------------------------------------------------------------------------------------------------------
    # START APPLICATION
    # Keep the window open and respond to user actions.
    # ----------------------------------------------------------------------------------------------------------
    root.mainloop()

# ==============================================================================================================
# PROGRAM ENTRY POINT
# Run main() only when this title is started directly. 
# ==============================================================================================================
if __name__ == "__main__":
    main()

