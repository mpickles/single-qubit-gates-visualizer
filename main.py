import qiskit
from qiskit import QuantumCircuit
from qiskit.visualization import visualize_transition
import tkinter as tk
from tkinter import LEFT, END, DISABLED, NORMAL
import numpy as np
import warnings

warnings.filterwarnings('ignore')


# Define the root window
root = tk.Tk()
root.title('Single-Qubit Visualizer')

# Set Icon
root.iconbitmap(default='atom.ico')
root.geometry('399x428') # Size the window
root.resizable(0,0) # block the resizing feature 

# Define colors and fonts
background = '#2c94c8'
buttons= '#834558'
special_buttons = '#bc3454'
button_font = ('Ariel', 18)
display_font=('Ariel', 32)

# Initialize Quantum Circuit
def initialize_circuit():
    global circuit
    circuit = QuantumCircuit(1)

initialize_circuit()
theta = 0;

# Define Display Function
def display_gate(gate_input):
    '''
    Adds corresponding gate_input to display frame to keep track of operations
    If the number of operations reaches 10, all gate buttons become disabled
    '''
    display.insert(END,gate_input)

    # Check if number of operations == 10

    input_gates = display.get()
    num_gates = len(input_gates)
    list_gates = list(input_gates)
    search_word = ["R", "D"]
    count_double_val_gates=[list_gates.count(i) for i in search_word]
    num_gates -= sum(count_double_val_gates)
    if num_gates == 10:
        gates=[x_gate, y_gate, z_gate, Rx_gate, Ry_gate, Rz_gate, s_gate, sd_gate, t_gate, td_gate, hadamard]
        for gate in gates:
            gate.config(state=DISABLED)

# Clear Function
def clear(circuit):
    '''
    Clears the display
    Reinitializes Quantum Circuit for new calculation
    Enables Buttons if disabled
    '''
    display.delete(0, END)
    initialize_circuit()
    if x_gate['state'] == DISABLED:
         gates=[x_gate, y_gate, z_gate, Rx_gate, Ry_gate, Rz_gate, s_gate, sd_gate, t_gate, td_gate, hadamard]
         for gate in gates:
            gate.config(state=NORMAL)
        

# Define About Function
def about():
    info= tk.Tk()
    info.title('About')
    info.geometry('650x470')
    info.resizable(0,0)

    text = tk.Text(info, height=20, width=20)

    # Create Label
    label=tk.Label(info, text="About This Program:")
    label.config(font=("Ariel", 14))

    text_to_display='''
Visualization Tool for Single Qubit Rotation on Bloch Sphere

Gate Buttons and corresponding qiskit commands:

X = flips the state vector of Qubit -                           cicuit.x()
Y = rotates the state vector about Y-axis-                      cicuit.y()
Z = flips the phase by PI radians -                             cicuit.z()
Rx = parameterized rotation about X-axis -                      cicuit.rx()
Ry = parameterized rotation about X-axis -                      cicuit.ry()
Rz = parameterized rotation about X-axis -                      cicuit.rz()
S = rotates the state vector about Z-axis by PI/2 radians -     circuit.s
T = rotates the state vector about Z-axis by PI/4 radians -     circuit.t
Sd = rotates the state vector about Z-axis by -PI/2 radians -   circuit.sdg()
Td = rotates the state vector about Z-axis by -PI/4 radians -   circuit.tdg()
H = creates superposition state -                               cicuit.h()

For Rx, Ry, Rz:
    theta(rotation angle) allowed range in the app is [-2*PI, 2*PI]

In the case of a visualization error, the app closes automatically
This indicates the visualiation of your circuit is not possible

At a time, only 10 operations can be visualized
 
    '''

    label.pack()
    text.pack(fill='both', expand=True)

    text.insert(END,text_to_display)

    info.mainloop()

def visualize_circuit(circuit, window):
    '''
    Visualizes the single qubit rotations corresponding to the applied gates in a seperate tkinter window
    Handles visualization error
    '''
    try:
        visualize_transition(circuit=circuit, trace=True, fpg=30)
    except qiskit.visualization.exceptions.VisualizationError:
        window.destroy()

def change_theta(num, window, circuit, key):
    '''
    Changes Global theta and destroys window
    '''
    global theta
    theta = num * np.pi
    if key == 'x':
        circuit.rx(theta,0)
        theta = 0;
    elif key == 'y':
        circuit.ry(theta,0)
        theta = 0;
    else:
        circuit.rz(theta,0)
        theta = 0;
    window.destroy()



def user_input(circuit, key):
    '''
    Get user input for rotation angle for parameterized rotation gates Rx, Ry, Rz
    '''
    # Initialize and define Window Properties
    get_input =tk.Tk()
    get_input.title("Get Theta")
    get_input.geometry('360x160')
    get_input.resizable(0,0)

    val1=tk.Button(get_input,height=2,width=10,bg=buttons,font=('Ariel',10),text="PI/4",command=lambda:change_theta(0.25,get_input,circuit,key))
    val1.grid(row=0,column=0)

    val2=tk.Button(get_input,height=2,width=10,bg=buttons,font=('Ariel',10),text="PI/2",command=lambda:change_theta(0.50,get_input,circuit,key))
    val2.grid(row=0,column=1)

    val3=tk.Button(get_input,height=2,width=10,bg=buttons,font=('Ariel',10),text="PI",command=lambda:change_theta(1.0,get_input,circuit,key))
    val3.grid(row=0,column=2)

    val4=tk.Button(get_input,height=2,width=10,bg=buttons,font=('Ariel',10),text="2*PI",command=lambda:change_theta(2.0,get_input,circuit,key))
    val4.grid(row=0,column=3)

    nval1=tk.Button(get_input,height=2,width=10,bg=buttons,font=('Ariel',10),text="-PI/4",command=lambda:change_theta(-0.25,get_input,circuit,key))
    nval1.grid(row=1,column=0)

    nval2=tk.Button(get_input,height=2,width=10,bg=buttons,font=('Ariel',10),text="-PI/2",command=lambda:change_theta(-0.50,get_input,circuit,key))
    nval2.grid(row=1,column=1)

    nval3=tk.Button(get_input,height=2,width=10,bg=buttons,font=('Ariel',10),text="-PI",command=lambda:change_theta(-1.0,get_input,circuit,key))
    nval3.grid(row=1,column=2)

    nval4=tk.Button(get_input,height=2,width=10,bg=buttons,font=('Ariel',10),text="-2*PI",command=lambda:change_theta(-2.0,get_input,circuit,key))
    nval4.grid(row=1,column=3)

    text_obj = tk.Text(get_input, height=20, width=20,bg="light cyan")

    note = '''
    GIVE THE VALUE FOR THETA
    The value has the range [-2*PI, 2*PI]
    '''

    text_obj.grid(sticky='WE', columnspan=4)
    text_obj.insert(END, note)


# Define Layout
# Define the Frames
display_frame = tk.LabelFrame(root)
button_frame = tk.LabelFrame(root, bg='black')
display_frame.pack();
button_frame.pack(fill='both', expand=True)

#Define the Display Frame Layout
display = tk.Entry(display_frame, width=120, font=display_font, bg=background, borderwidth=10, justify=LEFT)
display.pack(padx=3,pady=4)

# Define first row of buttons
x_gate = tk.Button(button_frame, font=button_font, bg=buttons, text='X',command=lambda:[display_gate('x'),circuit.x(0)])
y_gate = tk.Button(button_frame, font=button_font, bg=buttons, text='Y', command=lambda:[display_gate('y'),circuit.y(0)])
z_gate = tk.Button(button_frame, font=button_font, bg=buttons, text='Z', command=lambda:[display_gate('z'),circuit.z(0)])
# Insert Buttons into Frame
x_gate.grid(row=0, column=0, ipadx=45, pady=1)
y_gate.grid(row=0, column=1, ipadx=45, pady=1)
z_gate.grid(row=0, column=2, ipadx=53, pady=1) #, sticky='E') # E - East (stick button to east side)

# Row 2
Rx_gate = tk.Button(button_frame, font=button_font, bg=buttons, text='Rx', command=lambda:[display_gate('Rx'),user_input(circuit,'x')])
Ry_gate = tk.Button(button_frame, font=button_font, bg=buttons, text='Ry', command=lambda:[display_gate('Ry'),user_input(circuit,'x')])
Rz_gate = tk.Button(button_frame, font=button_font, bg=buttons, text='Rz', command=lambda:[display_gate('Rz'),user_input(circuit,'x')])
Rx_gate.grid(row=1, column=0, columnspan=1, sticky='WE', pady=1)
Ry_gate.grid(row=1, column=1, columnspan=1, sticky='WE', pady=1)
Rz_gate.grid(row=1, column=2, columnspan=1, sticky='WE', pady=1)

# Row 3
s_gate = tk.Button(button_frame, font=button_font, bg=buttons, text='S', command=lambda:[display_gate('S'),circuit.s(0)])
sd_gate = tk.Button(button_frame, font=button_font, bg=buttons, text='SD', command=lambda:[display_gate('SD'),circuit.sdg(0)])
hadamard = tk.Button(button_frame, font=button_font, bg=buttons, text='H', command=lambda:[display_gate('H'),circuit.h(0)])
s_gate.grid(row=2, column=0, columnspan=1, sticky='WE', pady=1)
sd_gate.grid(row=2, column=1, sticky='WE', pady=1)
hadamard.grid(row=2, column=2, rowspan=2, sticky='WENS', pady=1)

# Row 4/5
t_gate = tk.Button(button_frame, font=button_font, bg=buttons, text='T', command=lambda:[display_gate('T'),circuit.t(0)])
td_gate = tk.Button(button_frame, font=button_font, bg=buttons, text='TD', command=lambda:[display_gate('TD'),circuit.tdg(0)])
t_gate.grid(row=3, column=0, sticky='WE', pady=1)
td_gate.grid(row=3, column=1, sticky='WE', pady=1)

# Quit and Visualize Buttons
quit_button = tk.Button(button_frame, font=button_font, bg=special_buttons, text='Quit', command=root.destroy)
visualize = tk.Button(button_frame, font=button_font, bg=buttons, text='Visualize', command=lambda:visualize_circuit(circuit,root))
quit_button.grid(row=4, column=0, columnspan=2, sticky='WE', ipadx=5,pady=1)
visualize.grid(row=4, column=2, columnspan=1, sticky='WE', ipadx=8, pady=1)

# Clear Button
clear_button = tk.Button(button_frame, font=button_font, bg=special_buttons, text='Clear', command=lambda:clear(circuit))
clear_button.grid(row=5, column=0, columnspan=3, sticky='WE')

# About Button
about_button = tk.Button(button_frame, font=button_font, bg=special_buttons, text='About', command=about)
about_button.grid(row=6, column=0, columnspan=3, sticky='WE')

# Run Main Loop
root.mainloop()