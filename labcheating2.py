import win32gui
import datetime
from tkinter import Tk, Label, Button, messagebox, simpledialog, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

browsers = ["chrome", "firefox", "edge", "safari", "opera"]

def get_window():
    foreground_window = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(foreground_window)
    return title.strip()

def check_browser(win):
    for b in browsers:
        if b.lower() in win.lower():
            messagebox.showwarning("WARNING", "browser is opened")
            return True
    return False

def ask_password():
    password = simpledialog.askstring("Admin Authentication", "Enter password to close app:")
    return password == "Fast1234"

def create_visualization(root, labels, times, stime, etime):
    if not labels:
        messagebox.showinfo("error", "no data available for visualizing")
        return

    times_hours = [t / 3600 for t in times] 
    fig, ax = plt.subplots()
    ax.pie(times_hours, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 
    chart_title = f'App usage between {stime.strftime("%I:%M %p")} - {etime.strftime("%I:%M %p")}'
    ax.set_title(chart_title)

    pie_chart_window = Toplevel(root)
    pie_chart_window.title(chart_title)
    canvas = FigureCanvasTkAgg(fig, master=pie_chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    plt.close(fig)

def main():
    root = Tk()
    root.title("Lab Cheating Detection Software")
    app_label = Label(root, text="Press Start Monitoring button to start")
    app_label.pack(pady=10)

    apps = []
    times = []
    ltime = datetime.datetime.now()
    monitoring_stime = None

    def on_close():
        if ask_password():
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    def update_app():
        nonlocal ltime
        ctime = datetime.datetime.now()
        etime = (ctime - ltime).total_seconds()
        ltime = ctime

        win = get_window()
        app_label.config(text=f"Current App: {win}")

        if check_browser(win):
            pass  

        if win not in apps:
            apps.append(win)
            times.append(etime)
        else:
            index = apps.index(win)
            times[index] += etime

        root.after(5000, update_app)  

    def start_monitoring():
        nonlocal monitoring_stime
        monitoring_stime = datetime.datetime.now()
        update_app()  

    def stop_monitoring():
        etime = datetime.datetime.now()
        create_visualization(root, apps, times, monitoring_stime, etime)

    start_button = Button(root, text="Start Monitoring", command=start_monitoring)
    start_button.pack(pady=10)

    stop_button = Button(root, text="Stop Monitoring", command=stop_monitoring)
    stop_button.pack(pady=10)

    close_button = Button(root, text="Close", command=on_close)
    close_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
