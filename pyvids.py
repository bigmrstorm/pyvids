import tkinter as tk
from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter import messagebox, filedialog

def browse_directory():
    download_directory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH", title="Save Video")
    download_path.set(download_directory)

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_var.set(percentage)
    progress_bar.update()
    percentage_label.config(text=f"{percentage:.2f}%")

def download_video():
    youtube_link = video_link.get()
    download_folder = download_path.get()

    if not youtube_link or not download_folder:
        messagebox.showwarning("Input Error", "Please provide both YouTube link and download destination.")
        return

    try:
        video = YouTube(youtube_link, on_progress_callback=on_progress)
        stream = video.streams.filter(progressive=True).order_by('resolution').desc().first()  # Get highest quality progressive stream

        # Download the video
        stream.download(output_path=download_folder)
        messagebox.showinfo("Download Complete", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while downloading the video: {str(e)}")
    finally:
        progress_var.set(0)  # Reset the progress bar
        percentage_label.config(text="0%")  # Reset the percentage label

# Create the main window
root = tk.Tk()
root.title("PyVids")
root.geometry("500x350")
root.resizable(False, False)

# Apply a modern style
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TEntry", font=("Segoe UI", 10), padding=6)
style.configure("TProgressbar", thickness=20)
style.configure("TProgressbar.Horizontal.TProgressbar", troughcolor='white', background='blue')  # Make progress bar blue

# Variables to store user input
video_link = StringVar()
download_path = StringVar()
progress_var = DoubleVar()  # Variable to update progress bar

# Widgets
header_label = ttk.Label(root, text="PyVids", font=("Segoe UI", 16))
header_label.pack(pady=20)

link_frame = ttk.Frame(root)
link_frame.pack(pady=10, padx=10, fill=X)
ttk.Label(link_frame, text="YouTube link:").pack(side=LEFT, padx=(0, 10))
ttk.Entry(link_frame, textvariable=video_link, width=50).pack(side=LEFT, fill=X, expand=True)

destination_frame = ttk.Frame(root)
destination_frame.pack(pady=10, padx=10, fill=X)
ttk.Label(destination_frame, text="Destination:").pack(side=LEFT, padx=(0, 10))
ttk.Entry(destination_frame, textvariable=download_path, width=40).pack(side=LEFT, fill=X, expand=True)
ttk.Button(destination_frame, text="Browse", command=browse_directory).pack(side=LEFT, padx=10)

progress_frame = ttk.Frame(root)
progress_frame.pack(pady=20, padx=10, fill=X)
percentage_label = ttk.Label(progress_frame, text="0%")
percentage_label.pack(side=TOP, pady=(0, 10))
progress_bar = ttk.Progressbar(progress_frame, orient=HORIZONTAL, length=300, mode='determinate', variable=progress_var, style="TProgressbar.Horizontal.TProgressbar")
progress_bar.pack(fill=X, expand=True)

# Ensure the download button is visible
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)
ttk.Button(button_frame, text="Download Video", command=download_video).pack()

root.mainloop()
