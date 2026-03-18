## Data Analytsis_Automotive 
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

df = None
report_df = None
file_path = None
chart_figure = None

### FUNCTIONS

def browse_file():
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel Files","*.xlsx *.xls"),("CSV Files","*.csv")]
    )
    if file_path:
        file_entry.delete(0,tk.END)
        file_entry.insert(0,file_path)


def read_file():
    global df

    if not file_entry.get():
        messagebox.showerror("Error","Please select a file first")
        return

    try:
        path=file_entry.get()

        if path.endswith(".csv"):
            df=pd.read_csv(path)
        else:
            df=pd.read_excel(path)

        rows,cols=df.shape

        info_box.delete(1.0,tk.END)
        info_box.insert(tk.END,f"Rows : {rows}\n")
        info_box.insert(tk.END,f"Columns : {cols}\n\n")

        info_box.insert(tk.END,"Columns:\n")

        for c in df.columns:
            info_box.insert(tk.END,f"• {c}\n")

        detect_columns()

    except Exception as e:
        messagebox.showerror("Error",str(e))


def detect_columns():

    text_cols=[]
    numeric_cols=[]

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)

        else:
            try:
                pd.to_numeric(df[col])
                numeric_cols.append(col)
            except:
                text_cols.append(col)

    group_combo["values"]=text_cols
    value_combo["values"]=numeric_cols


def preview_report():

    global report_df

    if df is None:
        messagebox.showerror("Error","Read the file first")
        return

    g=group_var.get()
    v=value_var.get()
    a=agg_var.get()

    if not g or not v or not a:
        messagebox.showerror("Error","Select all options")
        return

    report_df=(df.groupby(g)[v]
              .agg(a)
              .reset_index()
              .sort_values(by=v,ascending=False))

    tree.delete(*tree.get_children())

    tree["columns"]=list(report_df.columns)
    tree["show"]="headings"

    for c in report_df.columns:
        tree.heading(c,text=c)
        tree.column(c,width=180)

    for _,r in report_df.iterrows():
        tree.insert("",tk.END,values=list(r))


def export_report():

    if report_df is None:
        messagebox.showerror("Error","Generate report first")
        return

    folder=os.path.dirname(file_entry.get())
    fmt=export_var.get()

    if fmt=="Excel":
        path=os.path.join(folder,"analysis_report.xlsx")
        report_df.to_excel(path,index=False)
    else:
        path=os.path.join(folder,"analysis_report.csv")
        report_df.to_csv(path,index=False)

    messagebox.showinfo("Success",f"Saved:\n{path}")


def preview_chart():

    global chart_figure

    if report_df is None:
        messagebox.showerror("Error","Generate report first")
        return

    for w in chart_area.winfo_children():
        w.destroy()

    x=report_df.iloc[:,0]
    y=report_df.iloc[:,1]

    chart_type=chart_var.get()

    chart_figure=plt.Figure(figsize=(6,4))
    ax=chart_figure.add_subplot(111)

    if chart_type=="Bar":
        ax.bar(x,y)

    elif chart_type=="Column":
        ax.bar(x,y)

    elif chart_type=="Line":
        ax.plot(x,y,marker="o")

    elif chart_type=="Pie":
        ax.pie(y,labels=x,autopct="%1.1f%%")

    ax.set_title("Data Analysis Chart")

    canvas=FigureCanvasTkAgg(chart_figure,chart_area)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH,expand=True)


def export_chart():

    if chart_figure is None:
        messagebox.showerror("Error","Preview chart first")
        return

    folder=os.path.dirname(file_entry.get())
    path=os.path.join(folder,"analysis_chart.png")

    chart_figure.savefig(path)

    messagebox.showinfo("Saved",path)


# MAIN WINDOW

root=tk.Tk()
root.title("Corporate Data Analyzer")
root.geometry("1100x750")
root.configure(bg="#f4f6f7")

# HEADER

header=tk.Label(
    root,
    text="Corporate Data Analyzer",
    font=("Segoe UI",22,"bold"),
    bg="#2c3e50",
    fg="white",
    pady=10
)

header.pack(fill=tk.X)

# FILE SECTION

file_frame=tk.LabelFrame(root,text="Step 1 : Select Data File",font=("Segoe UI",10,"bold"),padx=10,pady=10)
file_frame.pack(fill="x",padx=20,pady=10)

file_entry=tk.Entry(file_frame,width=70)
file_entry.grid(row=0,column=0,padx=10)

tk.Button(file_frame,text="Browse",command=browse_file,width=12).grid(row=0,column=1,padx=5)
tk.Button(file_frame,text="Read File",command=read_file,width=12).grid(row=0,column=2,padx=5)

# DATA INFO

info_frame=tk.LabelFrame(root,text="Dataset Information",font=("Segoe UI",10,"bold"))
info_frame.pack(fill="x",padx=20,pady=10)

info_box=tk.Text(info_frame,height=6)
info_box.pack(fill="x",padx=10,pady=10)

# REPORT BUILDER

report_frame=tk.LabelFrame(root,text="Step 2 : Build Analysis Report",font=("Segoe UI",10,"bold"),padx=10,pady=10)
report_frame.pack(fill="x",padx=20,pady=10)

group_var=tk.StringVar()
value_var=tk.StringVar()
agg_var=tk.StringVar()

tk.Label(report_frame,text="Group By").grid(row=0,column=0,padx=10)
tk.Label(report_frame,text="Value Column").grid(row=0,column=1,padx=10)
tk.Label(report_frame,text="Aggregation").grid(row=0,column=2,padx=10)

group_combo=ttk.Combobox(report_frame,textvariable=group_var,width=20)
value_combo=ttk.Combobox(report_frame,textvariable=value_var,width=20)

agg_combo=ttk.Combobox(report_frame,textvariable=agg_var,width=20,
values=["sum","mean","max","min","count","median"])

group_combo.grid(row=1,column=0,padx=10)
value_combo.grid(row=1,column=1,padx=10)
agg_combo.grid(row=1,column=2,padx=10)

tk.Button(report_frame,text="Preview Report",command=preview_report,width=15).grid(row=1,column=3,padx=15)

# TABLE

table_frame=tk.LabelFrame(root,text="Analysis Result",font=("Segoe UI",10,"bold"))
table_frame.pack(fill="both",expand=True,padx=20,pady=10)

tree=ttk.Treeview(table_frame)

scroll_y=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview)
tree.configure(yscroll=scroll_y.set)

tree.pack(side="left",fill="both",expand=True)
scroll_y.pack(side="right",fill="y")

# EXPORT

export_frame=tk.Frame(root,bg="#f4f6f7")
export_frame.pack(pady=5)

export_var=tk.StringVar()

export_combo=ttk.Combobox(export_frame,textvariable=export_var,width=15,
values=["Excel","CSV"])

export_combo.grid(row=0,column=0,padx=10)

tk.Button(export_frame,text="Export Report",command=export_report).grid(row=0,column=1,padx=10)

# CHART SECTION

chart_controls=tk.LabelFrame(root,text="Step 3 : Chart Builder",font=("Segoe UI",10,"bold"))
chart_controls.pack(fill="x",padx=20,pady=10)

chart_var=tk.StringVar()

chart_combo=ttk.Combobox(chart_controls,textvariable=chart_var,width=20,
values=["Bar","Column","Line","Pie"])

chart_combo.grid(row=0,column=0,padx=10,pady=5)

tk.Button(chart_controls,text="Preview Chart",command=preview_chart).grid(row=0,column=1,padx=10)
tk.Button(chart_controls,text="Export Chart",command=export_chart).grid(row=0,column=2,padx=10)

# CHART AREA

chart_area=tk.Frame(root,bg="white")
chart_area.pack(fill="both",expand=True,padx=20,pady=10)

root.mainloop()
