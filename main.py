from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
my_timer = None
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer(timer_label, canvas, checkmarks):
    global reps
    window.after_cancel(my_timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    reps = 0
    checkmarks.config(text=" ")
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer(timer_label, canvas, checkmarks):
    global reps, my_timer
    
    # Cancel any existing timer before starting a new one
    if my_timer is not None:
        window.after_cancel(my_timer)
        
    reps += 1
    work_seconds = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    if reps % 8 == 0:
        count_down(long_break_sec, timer_text, canvas, timer_label, checkmarks)
        timer_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec, timer_text, canvas, timer_label, checkmarks)
        timer_label.config(text="Break", fg=PINK)
    else:
        count_down(work_seconds, timer_text, canvas, timer_label, checkmarks)
        timer_label.config(text="Work", fg=GREEN)
    if reps > 8:
        reset_timer(timer_label, canvas, checkmarks)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count, timer_text, canvas, timer_label, checkmarks):
    global my_timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_min < 10:
        count_min = f"0{count_min}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        my_timer = window.after(1000, count_down, count - 1, timer_text, canvas, timer_label, checkmarks)
    else:
        start_timer(timer_label, canvas, checkmarks)
        mark = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            mark += "✔"
        checkmarks.config(text=mark)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=210, height=230, bg=YELLOW, highlightthickness=0)
tomato_image = PhotoImage(file="tomato.png")
canvas.create_image(105, 115, image=tomato_image)
timer_text = canvas.create_text(105, 135, text="00:00", fill='white', font=(FONT_NAME, 35, "bold"))
canvas.grid(column=2, row=2)

timer_label = Label(text="Timer", font=(FONT_NAME, 50, "bold"), bg=YELLOW, fg=GREEN)
timer_label.grid(column=2, row=1)

start_button = Button(text="Start", font=(FONT_NAME, 12, "bold"), bg=PINK, command=lambda: start_timer(timer_label, canvas, checkmarks))
start_button.grid(column=1, row=3)
start_button.config(width=8)

reset_button = Button(text="Restart", font=(FONT_NAME, 12, "bold"), bg=PINK, command=lambda: reset_timer(timer_label, canvas, checkmarks))
reset_button.config(width=8)
reset_button.grid(column=3, row=3)

checkmarks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 18))
checkmarks.grid(column=2, row=4)

window.mainloop()