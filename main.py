import subprocess
import os
import sys

def launch_ui(ui_file):
    """Helper function to launch a UI script."""
    if os.path.exists(ui_file):
        print(f"\nLaunching {ui_file}...")
        try:
            subprocess.Popen(['python', ui_file])
        except Exception as e:
            print(f"Error launching {ui_file}: {e}")
            sys.exit(1)
    else:
        print(f"Error: {ui_file} not found!")
        sys.exit(1)

def main():
    # Paths to the UI scripts
    ui_files = ['./scripts/ui.py']

    # Launch both UIs simultaneously
    for ui_file in ui_files:
        launch_ui(ui_file)

    # Optionally, keep the script running
    try:
        while True:
            pass  # This keeps the main script alive
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
