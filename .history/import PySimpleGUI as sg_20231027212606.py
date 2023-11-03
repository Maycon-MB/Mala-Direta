import PySimpleGUI as sg
import random, string

# ------ Some functions to help generate data for the table ------
def word():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))
def number(max_val=1000):
    return random.randint(0, max_val)

def make_table(num_rows, num_cols):
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    data[0] = [word() for _ in range(num_cols)]
    for i in range(0, num_rows):
        data[i] = [i, word(), *[number() for i in range(num_cols - 1)]]
    return data

def edit_cell(window, key, row, col, justify='left'):

    global textvariable, edit

    def callback(event, row, col, text, key):
        global edit
        widget = event.widget
        if key == 'Return':
            text = widget.get()
            print(text)
        widget.destroy()
        widget.master.destroy()
        values = list(table.item(row, 'values'))
        values[col] = text
        table.item(row, values=values)
        edit = False

    if edit or row <= 0:
        return

    edit = True
    root = window.TKroot
    table = window[key].Widget

    text = table.item(row, "values")[col]
    x, y, width, height = table.bbox(row, col)

    frame = sg.tk.Frame(root)
    frame.place(x=x, y=y, anchor="nw", width=width, height=height)
    textvariable = sg.tk.StringVar()
    textvariable.set(text)
    entry = sg.tk.Entry(frame, textvariable=textvariable, justify=justify)
    entry.pack()
    entry.select_range(0, sg.tk.END)
    entry.icursor(sg.tk.END)
    entry.focus_force()
    entry.bind("<Return>", lambda e, r=row, c=col, t=text, k='Return':callback(e, r, c, t, k))
    entry.bind("<Escape>", lambda e, r=row, c=col, t=text, k='Escape':callback(e, r, c, t, k))

def main_example1():
    global edit

    edit = False
    # ------ Make the Table Data ------
    # sg.Print('Creating table...')
    data = make_table(num_rows=1_000, num_cols=6)
    # headings = [str(data[0][x])+'     ..' for x in range(len(data[0]))]
    headings = [f'Col {col}' for col in range(len(data[0]))]
    # sg.Print('Done creating table.  Creating GUI...')
    sg.set_options(dpi_awareness=True)
    layout = [[sg.Table(values=data, headings=headings, max_col_width=25,
                        auto_size_columns=True,
                        # display_row_numbers=True,
                        justification='right',
                        num_rows=20,
                        alternating_row_color=sg.theme_button_color()[1],
                        key='-TABLE-',
                        # selected_row_colors='red on yellow',
                        # enable_events=True,
                        # select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True,
                        expand_y=True,
                        enable_click_events=True,  # Comment out to not enable header and other clicks
                        )],
              [sg.Button('Read'), sg.Button('Double'), sg.Button('Change Colors')],
              [sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')]]


    window = sg.Window('Table Element - Example 1', layout, resizable=True, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif isinstance(event, tuple):
            cell = row, col = event[2]
            window['-CLICKED-'].update(cell)
            edit_cell(window, '-TABLE-', row+1, col, justify='right')

    window.close()

main_example1()