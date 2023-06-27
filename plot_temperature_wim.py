import tkinter as tk
from tkinter import ttk
from collections import deque

import numpy as np
import pandas as pd
import matplotlib.colors as mcolors
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.backends.backend_tkagg as tkagg
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter, AutoLocator

from r_to_t import r_to_t, r_to_t_dict


# Obtain matplotlib colors
color_view = mcolors.TABLEAU_COLORS.values()
color_dict = dict(zip(range(len(color_view)-2), color_view))


# Global values
ROW_AMOUNT = 2
MAX_COLUMNS = 4
R_TO_T_MAX = 20
MAX_PLOTS = 6
FIGSIZE = (6,3)

LOCATOR = mdates.AutoDateLocator(minticks=3, maxticks=7)
FORMATTER = mdates.ConciseDateFormatter(LOCATOR)


class onofflabel(tk.Label):
    def __init__(self, master, textvariable, active_color, command):
        super().__init__(master=master, width=10, textvariable=textvariable)
        self.bind("<Button-1>", lambda event: self.toggle(event))
        self.bind("<Enter>", lambda event: self.hover(event))
        self.bind("<Leave>", lambda event: self.leave_hover(event))

        self.value = False
        self.active_color = active_color
        self.command = command

    def toggle(self, event=None):
        self.value = not self.value
        if self.value:
            self.configure(background=self.active_color)
        else:
            self.configure(background="SystemButtonFace")
        self.command()

    def hover(self, event):
        self.configure(relief="solid")

    def leave_hover(self, event):
        self.configure(relief="flat")


def read_n_last_lines(path_to_file, n):
    with open(path_to_file, 'r') as f:
        q = deque(f, n)  # lines read at the end

    splitted_lines = [s.split("\t") for s in list(filter(None, '\n'.join(q).splitlines()))]
    splitted_lines = [s for s in splitted_lines if "#" not in s[0]]
    df = pd.DataFrame(splitted_lines)
    df = df.set_index(list(df)[0])
    df.index = pd.to_datetime(df.index.astype(str))
    df = df.apply(pd.to_numeric)
    return df


class Entrywidget(tk.Entry):
    """
    This class makes use of the tkinter Entry class
    to add functionality to the standard tkinter 
    Entry widget. This includes using the arrow
    keys to increase and decrease the number inside 
    the entry box, being able to type "k" for a 
    factor of 1000 and "M" for a million. It also 
    checks if the value inside the entry does not 
    exceed the minimum or maximum value of that box. 
    """
    def __init__(self, master, width, minmax, callfunc, textvariable=None):
        super().__init__(master=master, width=width, textvariable=textvariable)
        self.minmax = minmax

        self.callfunc = callfunc

        self.bind("<Up>", lambda event: self.up_arrow_input(event))
        self.bind("<Down>", lambda event: self.down_arrow_input(event))
        self.bind("<Return>", lambda event: self.enter_input(event))

    def enter_input(self, event=None):
        number_str = self.get()
        if number_str[-1] == "k":
            number_float = float(number_str[:-1])
            number_str = str(int(number_float*1000))
        elif number_str[-1] == "M":
            number_float = float(number_str[:-1])
            number_str = str(int(number_float*1000000))
        elif number_str[-1] not in "1234567890":
            while number_str[-1] not in "1234567890":
                number_str = number_str[:-1]
        if float(number_str) > self.minmax[1]:
            number_str = int(self.minmax[1])
        elif float(number_str) < self.minmax[0]:
            number_str = self.minmax[0]
        self.delete(0, tk.END)
        self.insert(0, number_str)
        self.callfunc()
            
    def up_arrow_input(self, event=None):
        tkinter_position = self.index(tk.INSERT)
        number_str = self.get()
        decimalindex = number_str.find(".")
        if decimalindex < 0:
            number_int = int(number_str)
            position = len(number_str)-tkinter_position
            new_number = number_int + 10 ** position
            if new_number > self.minmax[1]:
                new_number = number_int
            new_number_str = str(new_number)
            if len(new_number_str) > len(number_str):
                tkinter_position = tkinter_position + 1
        else:
            number_float = float(number_str)
            position = len(number_str)-tkinter_position
            shift = len(number_str)-decimalindex
            if position - shift >= 0:
                new_number = number_float + 10 ** (position-shift)
            elif position - shift < -1:
                new_number = number_float + 10 ** (position-shift+1)
            else:
                new_number = number_float
            if new_number > self.minmax[1]:
                new_number = number_float
            new_number_str = str(round(new_number, shift))
        self.delete(0, tk.END)
        self.insert(0, new_number_str)
        self.icursor(tkinter_position)
        self.callfunc()

    def down_arrow_input(self, event=None):
        tkinter_position = self.index(tk.INSERT)
        number_str = self.get()
        decimalindex = number_str.find(".")
        if decimalindex < 0:
            number_int = int(number_str)
            position = len(number_str)-tkinter_position
            new_number = number_int - 10 ** position
            if new_number < self.minmax[0]:
                new_number = number_int
            new_number_str = str(new_number)
            if len(new_number_str) < len(number_str):
                tkinter_position = tkinter_position - 1
        else:
            number_float = float(number_str)
            position = len(number_str)-tkinter_position
            shift = len(number_str)-decimalindex
            if position - shift >= 0:
                new_number = number_float - 10 ** (position-shift)
            elif position - shift < -1:
                new_number = number_float - 10 ** (position-shift+1)
            else:
                new_number = number_float
            if new_number < self.minmax[0]:
                new_number = number_float
            new_number_str = str(round(new_number, shift))
        self.delete(0, tk.END)
        self.insert(0, new_number_str)
        self.icursor(tkinter_position)
        self.callfunc()


class Plotframe(ttk.LabelFrame):
    def __init__(self, master, name, color, max_columns, names_dict):
        self.name = tk.StringVar(value=name)
        self.names_dict = names_dict

        self.framelabel = ttk.Label(textvariable=self.name, foreground=color)
        super().__init__(master=master, labelwidget=self.framelabel)
        self.framelabel.bind("<Double-Button-1>", lambda event: print("verander naam"))

        figureframe = tk.Frame(master=self)
        figureframe.pack(side="left",fill='both',expand=True)#grid(row=0,column=0,rowspan=8,sticky="nsew")
        self.fig = Figure(figsize=FIGSIZE, tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        self.construct_lines(max_columns)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Temperature [mK]')
        self.ax.grid()
        self.canvas = FigureCanvasTkAgg(self.fig, master=figureframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top",fill='both',expand=True)
        self.navtoolbar = tkagg.NavigationToolbar2Tk(self.canvas, figureframe)

        self.plotcontrolframe = tk.Frame(master=self)
        self.plotcontrolframe.pack(side="left", fill="both")

        lockframelabel = ttk.Label(text="lock", foreground="black")
        lockframe = ttk.LabelFrame(master=self.plotcontrolframe, labelwidget=lockframelabel)
        lockframe.grid(row=0, column=0, sticky="nsew")
        self.lockxvar = tk.BooleanVar(value="1")
        self.lockyvar = tk.BooleanVar(value="1")
        self.lockx = ttk.Checkbutton(master=lockframe, text="x axis", variable=self.lockxvar, command=self.plotupdate)
        self.locky = ttk.Checkbutton(master=lockframe, text="y axis", variable=self.lockyvar, command=self.plotupdate)
        self.lockx.state(["selected"])
        self.locky.state(["selected"])
        self.lockx.pack()
        self.locky.pack()

        self.update_axis_controls(max_columns)

    def update_axis_controls(self, max_columns):
        xdataframelabel = ttk.Label(text="x axis", foreground="black")
        xdataframe = ttk.LabelFrame(master=self.plotcontrolframe, labelwidget=xdataframelabel)
        xdataframe.grid(row=1, column=0, sticky="nsew")
        self.xdatacbb = ttk.Combobox(xdataframe, width=10, state="readonly")
        xdata_keys = [f"column {i}" for i in range(max_columns + 1)]
        xdata_keys[0] = "real time"
        xdata_keys[1] = "time [s]"
        self.xdata_dict = dict(zip(xdata_keys, range(max_columns + 1)))
        self.xdatacbb["values"] = list(self.xdata_dict.keys())
        self.xdatacbb.set("real time")
        self.xdatacbb.pack()
        self.xdatacbb.bind("<<ComboboxSelected>>", lambda event: self.plotupdate(event))

        ydataframelabel = ttk.Label(text="y axis", foreground="black")
        ydataframe = ttk.LabelFrame(master=self.plotcontrolframe, labelwidget=ydataframelabel)
        ydataframe.grid(row=2, column=0, sticky="nsew")
        self.ydatadict = {}
        for i in range(2, max_columns + 1):
            self.ydatadict[i] = onofflabel(master=ydataframe, textvariable=self.names_dict[i], active_color=color_dict[i-2], command=self.plotupdate)
            self.ydatadict[i].pack()

    def construct_lines(self, max_columns):
        self.line_dict = {}
        for i in range(2, max_columns + 1):
            self.line_dict[i], = self.ax.plot([], [])

    def change_position(self, new_name, new_color):
        self.framelabel.configure(text=new_name, foreground=new_color)

    def plotupdate(self, event=None):
        for i, line in self.line_dict.items():
            xent = self.xdata_dict[self.xdatacbb.get()]
            if xent == 0:
                # use datetime format on x axis
                tempx = self.df.index.to_numpy()
                self.ax.xaxis.set_major_locator(LOCATOR)
                self.ax.xaxis.set_major_formatter(FORMATTER)
                self.ax.set_xlabel('Time')
            elif xent == 1:
                # use scalar format on x axis
                tempx = self.df[xent].to_numpy()
                self.ax.xaxis.set_major_locator(AutoLocator())
                self.ax.xaxis.set_major_formatter(ScalarFormatter())
                self.ax.set_xlabel('Time [s]')
            else:
                # use scalar format on x axis
                tempx = self.df[xent].to_numpy()
                self.ax.xaxis.set_major_locator(AutoLocator())
                self.ax.xaxis.set_major_formatter(ScalarFormatter())
                self.ax.set_xlabel('Temperature (mK)')
            tempy = self.df[i].to_numpy()
            line.set_data(tempx, tempy)
            line.set_visible(self.ydatadict[i].value)
        self.ax.redraw_in_frame()
        self.ax.relim(visible_only=True)
        if self.lockxvar.get():
            self.ax.autoscale(axis="x")
        if self.lockyvar.get():
            self.ax.autoscale(axis="y")
        self.canvas.draw()
        self.navtoolbar.update()

    def add_data(self, df):
        self.df = df

    def change_name(self, name):
        self.name.set(name)

    def remove_window(self):
        self.destroy() 


class Mainwindow():
    def __init__(self):
        self.mainwindow = tk.Tk()
        self.mainwindow.title('Thermometers Wim')
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.quit_me)

        # keep track of used plot numbers
        self.used_dict = dict(zip(range(len(color_view)-2), np.zeros(len(color_view))))
        self.frame_dict = {}
        self.chosen_channels = dict(zip(range(len(color_view)-2), np.zeros(len(color_view))))
        self.name_dict = {}
        self.data_loaded = False
        self.max_columns = 0

        #self.construct_menu()
        self.construct_controls()

        self.mainwindow.mainloop()

    def construct_menu(self):
        menubar = tk.Menu(self.mainwindow)

        # self.plotmenu = tk.Menu(menubar, tearoff=0)
        # menubar.add_cascade(label="Plot name", menu=self.plotmenu)
        
        self.removemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Delete", menu=self.removemenu)

        self.mainwindow.config(menu=menubar)

    def construct_controls(self):
        framelabel = ttk.Label(text="Controls", foreground="#fd04d9")
        controlframe = ttk.LabelFrame(master=self.mainwindow, labelwidget=framelabel)
        controlframe.grid(row=0, column=0, sticky="nsew")

        self.plotframe = tk.Frame(master=self.mainwindow)
        self.plotframe.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.add_plot_btn = tk.Button(controlframe, text="add plot", command=self.add_plot)
        self.add_plot_btn.grid(row=0, column=0, sticky="nsew")

        self.choose_file_btn = tk.Button(controlframe, text="choose file", command=self.choose_file)
        self.choose_file_btn.grid(row=0, column=1, sticky="nsew")

        empty_label = tk.Label(master=controlframe)
        empty_label.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.last_points_var = tk.StringVar()
        last_points_lbl = tk.Label(master=controlframe, text="Last")
        self.last_points_ent = Entrywidget(master=controlframe, 
                                      width=6, 
                                      minmax=[0,100000], 
                                      callfunc=self.read_data, 
                                      textvariable=self.last_points_var)
        self.last_points_ent.insert(0,200)

        last_points_lbl.grid(row=3,column=0)
        self.last_points_ent.grid(row=3,column=1)

        empty_label2 = tk.Label(master=controlframe)
        empty_label2.grid(row=4, column=0, columnspan=2, sticky="nsew")

        self.start_btn = tk.Button(master=controlframe, text="start", command=self.start_reading)
        self.start_btn.grid(row=5, column=0, sticky="nsew")

        self.stop_btn = tk.Button(master=controlframe, text="stop", command=self.stop_reading)
        self.stop_btn.grid(row=5, column=1, sticky="nsew")

        self.add_plot_btn.config(state="disabled")
        self.last_points_ent.config(state="disabled")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="disabled")

    def thermometer_setup(self, max_columns):
        framelabel = ttk.Label(text="Thermometers", foreground="#fd04d9")
        thermometerframe = ttk.LabelFrame(master=self.mainwindow, labelwidget=framelabel)
        thermometerframe.grid(row=1, column=0, sticky="nsew")

        self.thermometer_var_dict = {}
        self.thermometer_func_dict = {}

        for i in range(2, max_columns + 1):
            self.thermometer_var_dict[i] = tk.StringVar(value=i)
            entry = tk.Entry(master=thermometerframe, textvariable=self.thermometer_var_dict[i], width=12)
            combo = ttk.Combobox(master=thermometerframe, width=8, state="readonly")
            combo["values"] = list(r_to_t_dict.keys())
            combo.set("no conv.")
            combo.bind("<<ComboboxSelected>>", lambda event: self.read_data(event))
            entry.grid(row=i-2, column=0)
            combo.grid(row=i-2, column=1)
            self.thermometer_func_dict[i] = combo


    def add_plot(self):
        total_plots = int(sum(self.used_dict.values()))
        if total_plots < MAX_PLOTS:
            plot_number = min([i for i, val in self.used_dict.items() if val == 0])
            frame = Plotframe(self.plotframe, plot_number, color_dict[plot_number], self.max_columns, self.thermometer_var_dict)

            self.used_dict[plot_number] = True

            row, column = np.divmod(total_plots, ROW_AMOUNT)
            frame.grid(row=row,column=column,padx=10,pady=10,sticky="nsew")

            self.frame_dict[plot_number] = frame
            self.name_dict[plot_number] = tk.StringVar(value=plot_number)
            self.removemenu.add_command(label=f"Plot {plot_number}", command=lambda: self.remove_plot(plot_number))
            # self.plotmenu.add_command(label=f"Plot {plot_number}", command=lambda: self.change_plot_name(plot_number))

            if self.data_loaded:
                frame.add_data(self.df)
                frame.ydatadict[plot_number + 2].toggle()
                frame.plotupdate()

    def remove_plot(self, number):
        self.frame_dict[number].remove_window()
        self.frame_dict.pop(number)
        self.name_dict.pop(number)
        maximum_plotvalue = max([i for i, val in self.used_dict.items() if i >= number and val != 0])
        self.used_dict[number] = False
        self.removemenu.delete(f"Plot {maximum_plotvalue}")
        # self.plotmenu.delete(f"Plot {maximum_plotvalue}")
        for n in [i for i, val in self.used_dict.items() if i > number and val != 0]:
            self.frame_dict[n-1] = self.frame_dict[n]
            self.frame_dict.pop(n)

            self.name_dict[n-1] = self.name_dict[n]
            self.name_dict.pop(n)

            self.used_dict[n-1] = self.used_dict[n]
            self.used_dict[n] = False

            row, column = np.divmod(n-1, ROW_AMOUNT)
            self.frame_dict[n-1].grid(row=row, column=column,padx=10,pady=10,sticky="nsew")
            self.frame_dict[n-1].change_position(f"{n-1}", color_dict[n-1])

    def change_plot_name(self, number):
        old_name = self.frame_dict[number].name.get()
        self.name_dict[number].set(old_name)

        self.SubmitNameWindow = tk.Toplevel(self.mainwindow)
        self.SubmitNameWindow.title("Change name")

        name_lbl = tk.Label(master=self.SubmitNameWindow, text="Fill in new name")
        name_lbl.pack()

        name_entry = tk.Entry(master=self.SubmitNameWindow, width=15)
        name_entry.pack()
        name_entry.insert(0, old_name)
        name_entry.bind('<Return>', lambda event: self.change_name(number, name_entry.get()))

        submit_btn = tk.Button(master=self.SubmitNameWindow, text="submit", command=lambda: self.change_name(number, name_entry.get()))
        submit_btn.pack()

        self.SubmitNameWindow.focus()
        name_entry.focus_set()
        name_entry.select_range(0, 'end')

    def change_name(self, number, name):
        self.SubmitNameWindow.destroy()
        self.frame_dict[number].change_name(name)

    def choose_file(self):
        self.filename = tk.filedialog.askopenfilename(title="Choose file", 
                                                      filetypes=[('Data File in DAT Format', '*.dat')])
        if self.filename:
            self.construct_menu()
            max_columns = len(read_n_last_lines(self.filename, 2).columns)
            if max_columns != self.max_columns:
                self.thermometer_setup(max_columns)
                self.max_columns = max_columns
            if not self.data_loaded:
                self.add_plot()
            self.read_data()
            self.last_points_ent.config(state="normal")
            self.start_btn.config(state="normal")
            self.add_plot_btn.config(state="normal")

    def plotupdate(self, event=None):
        for key, frame in self.frame_dict.items():
            frame.add_data(self.df)
            frame.plotupdate()

    def toggle_channel_dict(self, choices):
        for key, val in self.chosen_channels.items():
            self.chosen_channels[key] += choices[key]

    def read_data(self, event=None):
        self.df = read_n_last_lines(self.filename, int(self.last_points_var.get()))
        for col in self.df.columns[1:]:
            self.df[col] = self.df[col].transform(r_to_t(r_to_t_dict[self.thermometer_func_dict[col].get()]))
        if not self.data_loaded:
            self.plotupdate()
            self.frame_dict[0].ydatadict[2].toggle()
        self.data_loaded = True
        # self.max_columns = len(self.df.columns)
        # for key, frame in self.frame_dict.items():
        #     frame.update_axis_controls(self.max_columns)
        self.plotupdate()

    def start_reading(self):
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.choose_file_btn.config(state="disabled")
        self.read = True
        self.mainwindow.after(1000, self.read_in_loop)

    def stop_reading(self):
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.choose_file_btn.config(state="normal")
        self.read = False

    def read_in_loop(self):
        if self.read:
            self.read_data()
        self.mainwindow.after(5000, self.read_in_loop)

    def quit_me(self):
        self.mainwindow.quit()
        self.mainwindow.destroy()


def main():
    Mainwindow()


if __name__ == "__main__":
    main()