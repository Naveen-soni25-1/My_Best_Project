import json

 #load file
 # Function to load tasks from a file
def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []  # If file doesn't exist or is empty, start fresh

# Create a List for tasks
tasks = []

# Load tasks when the program starts
load_tasks()
 
# saving task in file 
def save_task():
    with open("tasks.json","w") as file:
        json.dump(tasks,file)

# Let's greet user 
print("Hello there,\nnice to see you today!".title())
print("Enter [Quit] To Exit:\n")

# Function to force user input
def get_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("User input is necessary.")

# Show user the menu
def menu():
    """Print a simple menu for user"""
    print("\n[ENTER OPTION NUMBER]")
    print("---MENU---")
    menu_options = ['Add Task', 'Show Tasks', 'Delete Task', 'Mark Complete']
    for i, option in enumerate(menu_options, 1):
        print(f"{i}: {option}")
    return get_input("“Select Option:” ")

# Function to add task
def add_task():
    """Add tasks provided by user"""
    print("\nYou can add tasks now:".title())
    print("Enter [done] When Finished:")
    while True:
        task = input("Task: ").strip()
        if task.lower() == 'done':
            print("Exiting...")
            return  
        tasks.append({"task": task, "completed": False})
        save_task()
        print(f"Task '{task}' added and saved!")

# Function to show tasks
def show_task():
    """Show tasks in a formatted way"""
    print("\n---[TASKS]---")
    if not tasks:
        print("No tasks available.".title())
        return
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["completed"] else "×"
        print(f"{i}. {task['task']} [{status}]")

# Function to delete task
def delete_task():
    """Delete a task that is not needed"""
    if not tasks:
        print("No tasks available.".title())
        return
    show_task()
    while True:
        try:
            ask_1 = get_input("Enter Task Number to Delete: ")
            if ask_1.lower() == 'done':
                print("Exiting...")
                return
            ask_1 = int(ask_1)
            if 1 <= ask_1 <= len(tasks):
                removed_task = tasks.pop(ask_1 - 1)
                save_task()
                print(f"Deleted task: {removed_task['task']}")
                show_task()
            else:
                print("Invalid task number. Try again.")
        except ValueError:
            print("Enter a valid number.")

# Function to mark task as complete
def mark_complete():
    """Mark a task as complete"""
    if not tasks:
        print("No tasks available.".title())
        return
    show_task()
    while True:
        try:
            ask_2 = get_input("Enter Task Number to Mark Complete: ")
            if ask_2.lower() == 'done':
                print("Exiting...")
                return
            ask_2 = int(ask_2)
            if 1 <= ask_2 <= len(tasks):
                tasks[ask_2 - 1]["completed"] = True
                save_task()
                print(f"Marked '{tasks[ask_2 - 1]['task']}' as complete!")
                return
            else:
                print("Invalid task number. Try again.")
        except ValueError:
            print("Enter a valid number.")

# Main program loop
while True:
    menu_option = menu()
    if menu_option.lower() == 'quit':
        print("Ok Bye, Exiting the program")
        break
    try:
        menu_option = int(menu_option)
        if menu_option == 1:
            add_task()
        elif menu_option == 2:
            show_task()
        elif menu_option == 3:
            delete_task()
        elif menu_option == 4:
            mark_complete()
        else:
            print("Invalid option. Try again.")
    except ValueError:
        print("Enter a valid number.")  
