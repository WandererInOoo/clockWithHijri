#imports
#######################################################################################################
from time import *
from tkinter import *
from datetime import datetime
from hijri_converter import convert
from tkinter import colorchooser
#######################################################################################################

#functions
#######################################################################################################
def update():
    current_time = strftime("%I:%M:%S %p", localtime())
    time_label.config(text=current_time)

    current_day = strftime("%A", localtime())
    day_label.config(text=current_day)

    window.after(1000, update)

def toggle_date():
    global show_gregorian
    current_date = strftime("%B %d, %Y", localtime())

    if show_gregorian:
        date_label.config(text=current_date)
    else:
        gregorian_date = datetime.now()
        hijri_date = convert.Gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day).to_hijri()

        hijri_month_names = [
            "Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-Thani",
            "Jumada al-awwal", "Jumada al-Thani", "Rajab", "Sha'ban",
            "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"
        ]

        hijri_date_str = f"{hijri_date.day} {hijri_month_names[hijri_date.month - 1]} {hijri_date.year}"
        date_label.config(text=hijri_date_str)

    show_gregorian = not show_gregorian

    window.after(5000, toggle_date)

def start_drag(event):
    global startX, startY
    startX = event.x
    startY = event.y

def drag_window(event):
    x = window.winfo_pointerx() - startX
    y = window.winfo_pointery() - startY
    window.geometry(f'+{x}+{y}')

def freeze():
    window.unbind("<Button-1>")
    window.unbind("<B1-Motion>")

def unfreeze():
    window.bind("<Button-1>", start_drag)
    window.bind("<B1-Motion>", drag_window)

def show_options(event):
    drag_options.tk_popup(event.x_root, event.y_root)

def change_color():
    color_code = colorchooser.askcolor(title="Choose text color")[1]
    if color_code:
        time_label.config(fg=color_code)
        day_label.config(fg=color_code)
        date_label.config(fg=color_code)
#######################################################################################################

#window settings
#######################################################################################################
window = Tk()
window.overrideredirect(1)
window.title("Clock Mode")
transparent_color = 'red'
window.attributes('-transparentcolor', transparent_color)
window.config(bg=transparent_color)
#######################################################################################################

#keybinds
#######################################################################################################
window.bind("<Escape>", lambda e: window.destroy())
window.bind("<Button-1>", start_drag)
window.bind("<B1-Motion>", drag_window)
window.bind("<Button-3>", show_options)
#######################################################################################################

#labels
#######################################################################################################
time_label = Label(window, font=("Arial", 50, "bold"), fg="white", bg=transparent_color, highlightthickness=0)
time_label.pack()

day_label = Label(window, font=("Arial", 25, "bold"), fg="white", bg=transparent_color, highlightthickness=0)
day_label.pack()

date_label = Label(window, font=("Arial", 27, "bold"), fg="white", bg=transparent_color, highlightthickness=0)
date_label.pack()
#######################################################################################################

#right-click menu
#######################################################################################################
drag_options = Menu(window, tearoff=0)
drag_options.add_command(label="Freeze", command=freeze)
drag_options.add_command(label="Unfreeze", command=unfreeze)
drag_options.add_command(label="Color", command=change_color)
#######################################################################################################
show_gregorian = True
toggle_date()

update()

window.mainloop()
#######################################################################################################
#end
