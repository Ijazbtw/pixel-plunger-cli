import os
import sys
import json
import subprocess
import time

art = """\033[38;2;158;255;61m
     _         _         _                     
 ___|_|_ _ ___| |___ ___| |_ _ ___ ___ ___ ___ 
| . | |_'_| -_| |___| . | | | |   | . | -_|  _|
|  _|_|_,_|___|_|   |  _|_|___|_|_|_  |___|_|  
|_|                 |_|           |___|        
\033[0m"""


# Default path for the config file
config_file = 'app_config.json'
#---------------------------------------------------------------------------------------#
#---------------------------------CONFIG MODULE-----------------------------------------#
#---------------------------------------------------------------------------------------#

def load_config():
    """Load the app configuration from the config file."""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save the app configuration to the config file."""
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

def clear_app_data():
    """Clear app data by removing the config file."""
    if os.path.exists(config_file):
        os.remove(config_file)
        print("\033[92mApp data cleared successfully!\033[0m")
    else:
        print("\033[91mNo app data found to clear.\033[0m")

#-----------------------------------------------------------------------------------------#
#---------------------------------    ANIMATION      -------------------------------------#
#-----------------------------------------------------------------------------------------#
def show_spinner():
    """Display a spinning animation for visual feedback."""
    spinner = ['\\', '|', '/', '-']
    for _ in range(1):  # Spin only once
        for symbol in spinner:
            sys.stdout.write(f"\r\033[36mRunning {symbol}...\033[0m")  # Blue color for text
            sys.stdout.flush()  # Force the output to be displayed immediately
            time.sleep(0.2)

#-----------------------------------------------------------------------------------------#
#----------------------------------    RENDER      ---------------------------------------#
#-----------------------------------------------------------------------------------------#

def render_blend_file(config):
    """Render the .blend file using Blender."""
    # Get Blender executable path from config
    blender_executable = config.get("blender_executable")

    # Path to the render script (adjust this according to your needs)
    render_script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "render_script.py")

    if not os.path.exists(render_script_path):
        print("\033[91mError: Render script not found.\033[0m")
        return

    # Build the command to run Blender in the background
    command = [
        blender_executable,        # Blender executable
        "--background",            # Run Blender in the background (no UI)
        "--python", render_script_path , # Specify the Python render script to run
        "--log-level", "NONE"
    ]

    print("\033[34mRunning command...\033[0m")

    # Show the spinning animation while Blender is processing
    show_spinner()

    # Execute the Blender command
    subprocess.run(command)

    print("\033[92mRender completed!\033[0m")

#-----------------------------------------------------------------------------------------#
#------------------------------    INPUT HANDLER      ------------------------------------#
#-----------------------------------------------------------------------------------------#

def handle_user_choice(user_input, config):
    """Handle the user's input for the app's main menu."""
    if user_input == "r":
        render_blend_file(config)
    elif user_input == "e":
        print(f"Current Blender executable path: {config.get('blender_executable', 'Not set')}")
        confirm = input("Do you want to change the Blender executable path? (Y/N): ").strip().lower()
        if confirm == "y":
            new_path = input("Enter the new Blender executable file path: ").strip()
            if os.path.exists(new_path) and new_path.endswith("blender.exe"):
                config["blender_executable"] = new_path
                save_config(config)
                print("\033[92mBlender path updated successfully!\033[0m")
            else:
                print("\033[91mInvalid path. Please enter a valid path.\033[0m")
        else:
            print("Blender executable path remains unchanged.")
    elif user_input == "c":
        clear_app_data()
    elif user_input == "q":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("\033[91mInvalid option. Please try again.\033[0m")

#-----------------------------------------------------------------------------------------#
#------------------------------    MAIN FUNCTION      ------------------------------------#
#-----------------------------------------------------------------------------------------#

def main():
    # Load configuration
    config = load_config()

    # Check if Blender executable is set, otherwise ask for it
    if "blender_executable" not in config:
        print("\033[91mBlender executable path is not set.\033[0m")
        blender_path = input("Please enter the Blender executable file path: ").strip()
        while not os.path.exists(blender_path) or not blender_path.endswith("blender.exe"):
            print("\033[91mInvalid path. Please enter a valid path.\033[0m")
            blender_path = input("Please enter the Blender executable file path: ").strip()
        config["blender_executable"] = blender_path
        save_config(config)
        print("\033[92mBlender path set successfully!\033[0m")

    # Welcome message and options
    print(art)
    #print("\033[92mWelcome to Pixel Plunger!\033[0m")
    # print("\nOptions:")
    # print("R - Render a .blend file")
    # print("E - Change Blender executable path")
    # print("C - Clear app data")
    # print("Q - Quit")

    #print("R - Render  | E - Change Blender executable path | C - Clear app data | Q - Quit")
    print("\033[32mR\033[0m - Render  | \033[35mE\033[0m - Change Blender executable path | \033[33mC\033[0m - Clear app data | \033[31mQ\033[0m - Quit")



    while True:
        user_input = input("\nChoose an option: ").strip().lower()
        handle_user_choice(user_input, config)

if __name__ == "__main__":
    main()
