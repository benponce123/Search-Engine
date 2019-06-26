import Tkinter as tk
import project3


def button_call(sentence):
    return lambda : caller(sentence)

def caller(sentence):
    output_list = project3.retrieve_query()
    sentence.delete('1.0', tk.END)
    for x in output_list:
        sentence.insert(tk.END, (x + '\n'))
    sentence.see(tk.END)

def display_entry():
    return entry_box.get()

def enter_call(sentence):
    return lambda x: caller(sentence)


# Create main Gui window
root = tk.Tk()
frame = tk.Frame(root)
root.config(background = "white")
frame.grid(row = 1, column = 0)


# Create Group 99 Label
label = tk.Label(root, text = "Group 99", fg = 'royalblue1')
label.config(font=("futura", 50), background = "white")
label.grid(row = 0, column = 0, padx = 20, pady = 20)


# Create Entry box to search
entry_box = tk.Entry(root, borderwidth = 1, relief = 'solid',
                     font=("Calibri 15"), width = 60)
entry_box.grid(row = 1, column = 0, padx = 20, ipady = 5)
entry_box.focus_set()


# Create Gui results window
sentence = tk.Text(root, background = 'white', relief = 'groove', font=("Calibri 15"))
sentence.grid(row = 3, column = 0)


# Create search button
display_on_gui = tk.Button(root, text = "SEARCH",
                           command = button_call(sentence),
                           fg = 'blue', padx = 20, pady = 5, relief = 'raised')

display_on_gui.grid(row=2, column=0, padx = 25, pady = 25)


# Maintain center for all widgets upon expansion
root.grid_columnconfigure(0, weight = 1)
root.grid_rowconfigure(0, weight = 1)
root.grid_rowconfigure(1, weight = 1)
root.grid_rowconfigure(2, weight = 1)
root.grid_rowconfigure(3, weight = 1)


# Make enter key function as a search button press
entry_box.bind('<Return>', enter_call(sentence))


# Run main Gui App
root.mainloop()


