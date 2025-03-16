import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# Interpolación lineal de Newton
def intLinNewton(x, x0, x1, fx0, fx1):
    return fx0 + ((fx1 - fx0) / (x1 - x0)) * (x - x0)


# Interpolación cuadrátrica de Newton
def intSqrNewton(x, x0, x1, x2, fx0, fx1, fx2):
    f01 = (fx1 - fx0) / (x1 - x0)
    f12 = (fx2 - fx1) / (x2 - x1)
    f012 = (f12 - f01) / (x2 - x0)
    return fx0 + f01 * (x - x0) + f012 * (x - x0) * (x - x1)


# Interpolación lineal de Lagrange
def intLinLagrange(x, x0, x1, fx0, fx1):
    L0 = (x - x1) / (x0 - x1)
    L1 = (x - x0) / (x1 - x0)
    return L0 * fx0 + L1 * fx1


# Interpolación cuadrátrica de Lagrange
def intSqrLagrange(x, x0, x1, x2, fx0, fx1, fx2):
    L0 = ((x - x1) * (x - x2)) / ((x0 - x1) * (x0 - x2))
    L1 = ((x - x0) * (x - x2)) / ((x1 - x0) * (x1 - x2))
    L2 = ((x - x0) * (x - x1)) / ((x2 - x0) * (x2 - x1))
    return L0 * fx0 + L1 * fx1 + L2 * fx2


def calculate():
    try:
        x_val = float(entry_x.get())
        x0_val = float(entry_x0.get())
        x1_val = float(entry_x1.get())
        fx0_val = float(entry_fx0.get())
        fx1_val = float(entry_fx1.get())

        x2_val = fx2_val = None
        if option.get() in ("Newton Cuadrático", "Lagrange Cuadrático"):
            x2_val = float(entry_x2.get())
            fx2_val = float(entry_fx2.get())

        if option.get() == "Newton Lineal":
            result = intLinNewton(x_val, x0_val, x1_val, fx0_val, fx1_val)
        elif option.get() == "Newton Cuadrático":
            result = intSqrNewton(
                x_val, x0_val, x1_val, x2_val, fx0_val, fx1_val, fx2_val
            )
        elif option.get() == "Lagrange Lineal":
            result = intLinLagrange(x_val, x0_val, x1_val, fx0_val, fx1_val)
        elif option.get() == "Lagrange Cuadrático":
            result = intSqrLagrange(
                x_val, x0_val, x1_val, x2_val, fx0_val, fx1_val, fx2_val
            )

        result_label.config(text=f"f(x) ≈ {result:.6f}")

        if valor_exacto_var.get() and entry_fx_exacto.get():
            fx_exacto = float(entry_fx_exacto.get())
            error = (fx_exacto - result) / fx_exacto * 100
            error_label.config(text=f"Error: {error:.6f}%")
        else:
            error_label.config(text="")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")


def cleanLabel():
    for widget in frame_inputs.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)

    result_label.config(text="")
    error_label.config(text="")


def globalLabel(*args):
    for widget in frame_inputs.winfo_children():
        widget.destroy()

    global \
        entry_x, \
        entry_x0, \
        entry_x1, \
        entry_fx0, \
        entry_fx1, \
        entry_x2, \
        entry_fx2, \
        entry_fx_exacto
    entry_x2 = entry_fx2 = entry_fx_exacto = None

    campos = [
        ("x:", "entry_x"),
        ("x0:", "entry_x0"),
        ("x1:", "entry_x1"),
        ("f(x0):", "entry_fx0"),
        ("f(x1):", "entry_fx1"),
    ]

    if option.get() in ("Newton Cuadrático", "Lagrange Cuadrático"):
        campos.extend([("x2:", "entry_x2"), ("f(x2):", "entry_fx2")])

    for i, (label, var_name) in enumerate(campos):
        tk.Label(frame_inputs, text=label).grid(row=i, column=0)
        entry = tk.Entry(frame_inputs)
        entry.grid(row=i, column=1)
        globals()[var_name] = entry

    tk.Checkbutton(
        frame_inputs,
        text="Tengo f(x) exacto",
        variable=valor_exacto_var,
        command=vvLabelYN,
    ).grid(row=len(campos), columnspan=2)


def vvLabelYN():
    if valor_exacto_var.get():
        tk.Label(frame_inputs, text="f(x) exacto:").grid(row=9, column=0)
        global entry_fx_exacto
        entry_fx_exacto = tk.Entry(frame_inputs)
        entry_fx_exacto.grid(row=9, column=1)
    else:
        if entry_fx_exacto:
            entry_fx_exacto.destroy()


# INICIA GUI
window = tk.Tk()
window.title("Calculadora de interpolación")
window.geometry("500x500")

option = tk.StringVar()
option.trace_add("write", globalLabel)
valor_exacto_var = tk.BooleanVar()

frame_menu = tk.Frame(window)
frame_menu.pack()
tk.Label(frame_menu, text="Seleccione método:").pack()
ttk.Combobox(
    frame_menu,
    textvariable=option,
    values=[
        "Newton Lineal",
        "Newton Cuadrático",
        "Lagrange Lineal",
        "Lagrange Cuadrático",
    ],
    state="readonly",
).pack()

frame_inputs = tk.Frame(window)
frame_inputs.pack()

result_label = tk.Label(window, text="")
result_label.pack()
error_label = tk.Label(window, text="")
error_label.pack()

tk.Button(window, text="Calcular", command=calculate).pack()
tk.Button(window, text="Limpiar", command=cleanLabel).pack()

window.mainloop()
