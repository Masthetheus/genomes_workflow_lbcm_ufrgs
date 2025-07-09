import sys
import importlib
import os

TOOLS_DIR = os.path.join(os.path.dirname(__file__), 'tools')

# List all scripts in the tools directory that are Python files and not __init__
tool_scripts = [f[:-3] for f in os.listdir(TOOLS_DIR) if f.endswith('.py') and f != '__init__.py']

def print_menu():
    print("Available tools:")
    for idx, script in enumerate(tool_scripts, 1):
        print(f"{idx}. {script}")
    print("0. Exit")

def main():
    while True:
        print_menu()
        try:
            choice = int(input("Select a tool to run: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if choice == 0:
            print("Exiting.")
            break
        if 1 <= choice <= len(tool_scripts):
            script_name = tool_scripts[choice - 1]
            try:
                module = importlib.import_module(f'tools.{script_name}')
                if hasattr(module, 'main'):
                    module.main()
                else:
                    print(f"{script_name} does not have a main() function.")
            except Exception as e:
                print(f"Error running {script_name}: {e}")
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
