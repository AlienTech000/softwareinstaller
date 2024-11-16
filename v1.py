import tkinter as tk
from tkinter import messagebox
import subprocess
import getpass

# Function to check if the root password is correct
def check_root_password(password):
    try:
        # Run a simple command with sudo to check if the password is correct
        result = subprocess.run(
            ["sudo", "-S", "ls", "/"],
            input=password + "\n",  # provide password to sudo
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True  # Correct password
        else:
            return False  # Incorrect password
    except Exception as e:
        return False  # Error in running sudo

# Function to check if Flatpak is installed
def is_flatpak_installed():
    try:
        # Check if Flatpak is installed by running 'flatpak --version'
        result = subprocess.run(
            ["flatpak", "--version"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0  # If return code is 0, Flatpak is installed
    except FileNotFoundError:
        return False  # Flatpak is not installed

# Function to install Flatpak
def install_flatpak():
    if not check_root_password(root_password_entry.get()):
        messagebox.showerror("Authentication Error", "Incorrect root password. You need to enter the correct password to proceed.")
        return

    try:
        # First, try the standard installation command
        result = subprocess.run(
            ["sudo", "apt", "install", "-y", "flatpak"],
            capture_output=True,
            text=True
        )

        # If Flatpak is not installed, try adding the PPA repository
        if result.returncode != 0:
            messagebox.showinfo("Info", "Flatpak not found. Adding PPA and installing Flatpak...")
            subprocess.run(
                ["sudo", "add-apt-repository", "ppa:flatpak/stable", "-y"],
                capture_output=True,
                text=True
            )
            subprocess.run(["sudo", "apt", "update", "-y"], capture_output=True, text=True)
            subprocess.run(["sudo", "apt", "install", "-y", "flatpak"], capture_output=True, text=True)

            # Install GNOME software plugin for Flatpak
            subprocess.run(["sudo", "apt", "install", "-y", "gnome-software-plugin-flatpak"], capture_output=True, text=True)

        # Add Flathub repository if not already added
        subprocess.run(["sudo", "flatpak", "remote-add", "--if-not-exists", "flathub", "https://dl.flathub.org/repo/flathub.flatpakrepo"], capture_output=True, text=True)

        messagebox.showinfo("Success", "Flatpak and Flathub repository installed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while installing Flatpak: {str(e)}")

# Function to install a specific Flatpak application
def install_flatpak_app(app_id):
    # Check if Flatpak is installed
    if not is_flatpak_installed():
        messagebox.showerror("Error", "Flatpak is not installed. You need Flatpak to install applications.")
        return
    
    # If Flatpak is installed, proceed with the application installation
    if not check_root_password(root_password_entry.get()):
        messagebox.showerror("Authentication Error", "Incorrect root password. You need to enter the correct password to proceed.")
        return

    try:
        # Install the specified Flatpak app
        result = subprocess.run(
            ["sudo", "flatpak", "install", "flathub", app_id, "-y"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            messagebox.showinfo("Success", f"{app_id} installed successfully!")
        else:
            messagebox.showerror("Error", f"Failed to install {app_id}: {result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to install Google Chrome via Flatpak
def install_chrome():
    install_flatpak_app("com.google.Chrome")

# Function to install Discord via Flatpak
def install_discord():
    install_flatpak_app("com.discordapp.Discord")

# Function to install Spotify via Flatpak
def install_spotify():
    install_flatpak_app("com.spotify.Client")

# Function to install Kdenlive via Flatpak
def install_kdenlive():
    install_flatpak_app("org.kde.kdenlive")

# Function to install OBS Studio via Flatpak
def install_obs_studio():
    install_flatpak_app("com.obsproject.Studio")

# Function to install Stacer
def install_stacer():
    if not check_root_password(root_password_entry.get()):
        messagebox.showerror("Authentication Error", "Incorrect root password. You need to enter the correct password to proceed.")
        return

    try:
        # Use subprocess to run the install command
        result = subprocess.run(
            ["sudo", "apt", "install", "-y", "stacer"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            messagebox.showinfo("Success", "Stacer installed successfully!")
        else:
            messagebox.showerror("Error", f"Failed to install Stacer: {result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Software Installer")
root.geometry("350x400")

# Add a label
label = tk.Label(root, text="Enter your root password to continue:")
label.pack(pady=10)

# Add a password entry field
root_password_entry = tk.Entry(root, show="*", width=30)
root_password_entry.pack(pady=10)

# Function to check password and unlock UI
def authenticate():
    if check_root_password(root_password_entry.get()):
        label.config(text="Choose a software to install:")
        install_button.pack(pady=5)
        install_chrome_button.pack(pady=5)
        install_discord_button.pack(pady=5)
        install_spotify_button.pack(pady=5)
        install_kdenlive_button.pack(pady=5)
        install_obs_studio_button.pack(pady=5)
        install_flatpak_button.pack(pady=5)
        root_password_entry.pack_forget()  # Hide password entry
        auth_button.pack_forget()  # Hide authenticate button
    else:
        messagebox.showerror("Authentication Error", "Incorrect root password.")

# Add a button to authenticate (check password)
auth_button = tk.Button(root, text="Authenticate", command=authenticate)
auth_button.pack(pady=10)

# Add a button to install Stacer (initially hidden)
install_button = tk.Button(root, text="Install Stacer", command=install_stacer)

# Add a button to install Google Chrome via Flatpak (initially hidden)
install_chrome_button = tk.Button(root, text="Install Google Chrome", command=install_chrome)

# Add a button to install Discord via Flatpak (initially hidden)
install_discord_button = tk.Button(root, text="Install Discord", command=install_discord)

# Add a button to install Spotify via Flatpak (initially hidden)
install_spotify_button = tk.Button(root, text="Install Spotify", command=install_spotify)

# Add a button to install Kdenlive via Flatpak (initially hidden)
install_kdenlive_button = tk.Button(root, text="Install Kdenlive", command=install_kdenlive)

# Add a button to install OBS Studio via Flatpak (initially hidden)
install_obs_studio_button = tk.Button(root, text="Install OBS Studio", command=install_obs_studio)

# Add a button to install Flatpak (initially hidden)
install_flatpak_button = tk.Button(root, text="Install Flatpak", command=install_flatpak)

# Run the main event loop
root.mainloop()

