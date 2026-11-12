from tkinter import *
from dotenv import load_dotenv
import os
import urllib.request
import threading

load_dotenv()
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
NTFY_TOPIC = os.getenv("NTFY_TOPIC")

class Pomodoro:

    def __init__(self):
        self.work_secs = WORK_MIN * 60
        self.short_break_secs = SHORT_BREAK_MIN * 60
        self.long_break_secs = LONG_BREAK_MIN * 60
        self.break_count = 1
        self.is_break = False
        self.timer = None

# ---------------------------- UI SETUP ------------------------------- #
        # window
        self.window = Tk()
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=50, bg=YELLOW)

        # Create a centered container frame
        container = Frame(self.window, bg=YELLOW)
        container.pack(expand=True)

        # label
        self.title_label = Label(container, text="Timer", font=(FONT_NAME, 50, "bold"), fg=GREEN, bg=YELLOW)
        self.title_label.grid(row= 0, column= 1)

        self.check_marks = Label(container, text="", fg=GREEN, bg=YELLOW, font=(...,12))
        self.check_marks.grid(row=3, column=1)

        # canvas
        self.canvas = Canvas(container, width=200, height=224, bg = YELLOW, highlightthickness=0)
        tomato_img = PhotoImage(file="tomato.png")
        self.canvas.create_image(100, 112, image=tomato_img)
        self.timer_text = self.canvas.create_text(102, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
        self.canvas.grid(row=1, column=1)

        # button
        self.start_button = Button(container, text="Start", highlightthickness=0, command=self.start_timer)
        self.reset_button = Button(container, text="Reset", highlightthickness=0, command=self.reset_timer)

        self.start_button.grid(row=2, column=0)
        self.reset_button.grid(row=2, column=2)

        self.center_window()

        self.window.mainloop()

    # ---------------------------- TIMER RESET ------------------------------- # 
    def reset_timer(self):
        if self.timer is not None:
            self.window.after_cancel(self.timer)
            self.timer = None

        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.title_label.config(text="Timer", fg=GREEN)
        self.check_marks.config(text="")
        self.break_count = 4
        self.is_break = False
        self.start_button.config(state="normal")

    # ---------------------------- TIMER MECHANISM ------------------------------- # 
    def start_timer(self):
        self.start_button.config(state="disabled")
        self.is_break = False
        self.title_label.config(text="WORK", fg=GREEN)
        self.countdown(self.work_secs)

    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
    def countdown(self, seconds_left):
        mins, secs = divmod(seconds_left, 60)
        self.canvas.itemconfig(self.timer_text, text=f"{mins:02d}:{secs:02d}")
    
        if seconds_left > 0:
            self.timer = self.window.after(1000, self.countdown, seconds_left - 1)
        elif self.is_break:
            # Break finished -> Switch back to Work session
            if (self.break_count - 1) % 4 == 0:
                self.notify_long_break_over()

            self.is_break = False
            self.title_label.config(text="Work", fg=GREEN)
            self.timer = self.window.after(1000, self.countdown, self.work_secs)
        elif self.break_count % 4 != 0:
            # Work finished -> Switch to Short Break
            self.is_break = True
            self.bring_to_front()
            self.break_count += 1
            self.title_label.config(text="Break", fg=PINK)
            self.check_marks.config(text="✓" * (self.break_count - 1))
            self.timer = self.window.after(1000, self.countdown, self.short_break_secs)
        else:
            # 4th Work finished -> Switch to Long Break
            self.is_break = True
            self.bring_to_front()
            self.break_count += 1
            self.title_label.config(text="Break", fg=RED)
            self.check_marks.config(text="✓" * (self.break_count - 1))
            self.timer = self.window.after(1000, self.countdown, self.long_break_secs)
    # ---------------------------- ADJUSTING WINDOW ------------------------------- #
    def bring_to_front(self):
        self.window.deiconify()  
        self.window.lift()
        self.center_window()
        self.window.config()      
        self.window.attributes("-topmost", True)  
        self.window.attributes("-topmost", False)  
        self.window.focus_force()

    def center_window(self):
        # Force Tkinter to calculate the exact width and height of all widgets
        self.window.update_idletasks()
        
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate top-left (x, y) coordinates to place the window in the middle
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        # Apply the position without overriding the window's natural size
        self.window.geometry(f"+{x}+{y}")

    # ---------------------------- NOTIFICATION HANDLER ------------------------------- #
    def notify_long_break_over(self):
        # Run in a background thread so the GUI stays smooth
        threading.Thread(target=self._send_push, daemon=True).start()

    def _send_push(self):
        url = f"https://ntfy.sh/{NTFY_TOPIC}"
        message = "Your 20-minute long break is over! Time to get back to work."
        
        req = urllib.request.Request(
            url,
            data=message.encode("utf-8"),
            headers={
                "Title": "Pomodoro Timer",
                "Priority": "high",
                "Tags": "tomato,alarm_clock"
            }
        )
        try:
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            print(f"Push notification failed: {e}")