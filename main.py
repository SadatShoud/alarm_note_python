import tkinter as tk
from tkinter import scrolledtext, messagebox
import time
import pygame

class NotepadApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Notepad, Alarm, and Clock")

        # Text area for writing notes
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=10)
        self.text_area.pack(padx=10, pady=10)

        # Timer section
        self.timer_label = tk.Label(self.root, text="Set Timer (HH:MM:SS):")
        self.timer_label.pack(pady=5)

        self.timer_entry = tk.Entry(self.root, width=10)
        self.timer_entry.pack(pady=5)

        self.start_timer_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        self.start_timer_button.pack(pady=5)

        self.countdown_label = tk.Label(self.root, text="")
        self.countdown_label.pack(pady=5)

        self.stop_timer_button = tk.Button(self.root, text="Stop Timer", command=self.stop_timer)
        self.stop_timer_button.pack(pady=5)

        # Clock section
        self.clock_label = tk.Label(self.root, text="Current Time:")
        self.clock_label.pack(pady=5)

        self.update_clock()
        self.root.after(1000, self.update_clock)  # Update clock every 1000 milliseconds

        # Alarm section
        alarm_frame = tk.Frame(self.root)
        alarm_frame.pack(pady=5)

        self.alarm_label = tk.Label(alarm_frame, text="Set Alarm Time (HH:MM):")
        self.alarm_label.pack(side=tk.LEFT)

        self.alarm_entry = tk.Entry(alarm_frame, width=10)
        self.alarm_entry.pack(side=tk.LEFT, padx=5)

        # AM/PM option for set alarm
        self.am_pm_var = tk.StringVar()
        self.am_pm_var.set("AM")

        self.am_pm_label = tk.Label(alarm_frame, text="AM/PM:")
        self.am_pm_label.pack(side=tk.LEFT, padx=5)

        self.am_pm_menu = tk.OptionMenu(alarm_frame, self.am_pm_var, "AM", "PM")
        self.am_pm_menu.pack(side=tk.LEFT, padx=5)

        self.set_alarm_button = tk.Button(alarm_frame, text="Set Alarm", command=self.set_alarm)
        self.set_alarm_button.pack(side=tk.LEFT, padx=5)

        self.alarm_text_label = tk.Label(self.root, text="")
        self.alarm_text_label.pack(pady=5)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Timer variables
        self.timer_seconds_left = 0
        self.timer_running = False

        # Alarm variables
        self.alarm_time = None
        self.alarm_set = False  # Initialize alarm_set attribute

        # Run the GUI loop
        self.root.mainloop()

    def start_timer(self):
        time_str = self.timer_entry.get()

        try:
            hours, minutes, seconds = map(int, time_str.split(":"))
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid time in HH:MM:SS format.")
            return

        if not (0 <= hours < 24) or not (0 <= minutes < 60) or not (0 <= seconds < 60):
            tk.messagebox.showerror("Error", "Please enter valid values for hours, minutes, and seconds.")
            return

        total_seconds = hours * 3600 + minutes * 60 + seconds

        self.timer_seconds_left = total_seconds
        self.timer_running = True

        self.update_countdown()

    def update_countdown(self):
        if self.timer_running and self.timer_seconds_left > 0:
            self.countdown_label.config(text=f"Time remaining: {self.format_time(self.timer_seconds_left)}")
            self.timer_seconds_left -= 1
            self.root.after(1000, self.update_countdown)
        elif self.timer_running:
            self.timer_running = False
            self.countdown_label.config(text="Time is up!")
            self.play_alarm()
            self.show_text()

    def stop_timer(self):
        self.timer_running = False
        self.countdown_label.config(text="")
        self.timer_seconds_left = 0

    def play_alarm(self):
        pygame.mixer.music.load(r"Path")
        pygame.mixer.music.play()

    def show_text(self):
        text = self.text_area.get("1.0", tk.END)
        tk.messagebox.showinfo("Timer Finished", f"Time is up!\n\nYour Note:\n{text}")

    def update_clock(self):
        current_time = time.localtime()
        formatted_time = time.strftime("%I:%M:%S %p", current_time)
        self.clock_label.config(text=f"Current Time: {formatted_time}")
        self.check_alarm()  # Check for the alarm at each clock update
        self.root.after(1000, self.update_clock)

    def set_alarm(self):
        alarm_time_str = self.alarm_entry.get()
        am_pm_choice = self.am_pm_var.get()

        try:
            alarm_hours, alarm_minutes = map(int, alarm_time_str.split(":"))
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid time in HH:MM format.")
            return

        if not (0 <= alarm_hours < 24) or not (0 <= alarm_minutes < 60):
            tk.messagebox.showerror("Error", "Please enter valid values for hours and minutes.")
            return

        if am_pm_choice == "PM" and alarm_hours < 12:
            alarm_hours += 12
        elif am_pm_choice == "AM" and alarm_hours == 12:
            alarm_hours = 0

        current_time = time.localtime()
        current_hours, current_minutes = current_time.tm_hour, current_time.tm_min

        # Calculate the time difference for the alarm
        alarm_seconds = alarm_hours * 3600 + alarm_minutes * 60
        current_seconds = current_hours * 3600 + current_minutes * 60
        time_difference = alarm_seconds - current_seconds

        # Ensure the time difference is positive
        if time_difference <= 0:
            time_difference += 24 * 3600  # Add 24 hours to the time difference

        self.alarm_time = time.time() + time_difference
        self.alarm_set = True
        self.alarm_text_label.config(text=f"Alarm set for {alarm_time_str} {am_pm_choice}")
        self.check_alarm()  # Call check_alarm after setting the alarm
        tk.messagebox.showinfo("Set Alarm", f"Alarm set for {alarm_time_str} {am_pm_choice}")

    def check_alarm(self):
        if hasattr(self, 'alarm_set') and self.alarm_set and time.time() >= self.alarm_time:
            self.alarm_set = False
            self.play_alarm()
            alarm_text = self.text_area.get("1.0", tk.END)
            tk.messagebox.showinfo("Alarm", f"Time to wake up!\n\nYour Note:\n{alarm_text}")

    def format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    NotepadApp()
