import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
from graphviz import Source
from Parser.RD.rd_parser import RDParser
from Scanner.scanner import Scanner
from Parser.RD.test_rd import draw_nltk_tree,display_error_list
window_bg = "#576F72"
button = "#D0C9C0"
Error = ["error1", "error2", "error3", "error4", "error5",
         "error6"]


def Identifier():
    Identifier_window = tk.Toplevel()
    Identifier_window.config(width=400, height=200)
    Identifier_window.title("Identifier_DFA")
    Identifier_window.geometry("595x195")
    Label(Identifier_window, text="ID DFA").pack()
    dot_representation = '''
                    digraph finite_statemachine {
                        rankdir=LR;
                        size="8,5"
                        node [shape = doublecircle]; q2 ;
                        node [shape = circle];
                        q0[shape = point]
                        q0->q1 [label = " "];
                        q1 -> q2 [label = "[a-z],_,$"];
                        q1 -> reject [label = "any other char"];
                        q2 -> q2 [label = "[a-z],_,[0-9],$"];
                        q2 -> reject [label = "any other char"];
                        reject ->reject [label = "any other char"];
                    }
                    '''
    # Generate the DFA diagram as an image
    graph = Source(dot_representation, format='png')
    graph.render(filename='Identifier_DFA')
    # Load the image into Tkinter
    image = ImageTk.PhotoImage(Image.open('Identifier_DFA.png'))
    panel = tk.Label(Identifier_window, image=image)
    panel.pack(fill="both", expand=True)
    panel.config(Identifier_window)


def Integer():
    Integer_Window = tk.Toplevel()
    Integer_Window.config(width=400, height=200)
    Integer_Window.title("Integer_DFA")
    Integer_Window.geometry("565x195")
    Label(Integer_Window, text="Integer_DFA").pack()
    dot_representation2 = '''
                digraph finite_state_machine {
                    rankdir=LR;
                    size="8,5"
                    node [shape = doublecircle]; q2 ;
                    node [shape = circle];
                    q0[shape = point]
                    q0->q1 [label = " "];
                    q1 -> q2 [label = "[0-9]"];
                    q1 -> reject [label = "any other char"];
                    q2 -> q2 [label = "[0-9]"];
                    q2 -> reject [label = "any other char"];
                    reject->reject [label = "any other char"];
                }
                '''
    # Generate the DFA diagram as an image
    graph1 = Source(dot_representation2, format='png')
    graph1.render(filename='Integer_DFA')
    # Load the image into Tkinter
    image1 = ImageTk.PhotoImage(Image.open('Integer_DFA.png'))
    panel = tk.Label(Integer_Window, image=image1)
    panel.pack(fill="both", expand=True)
    panel.config(Integer_Window)


def Real():
    Real_Window = tk.Toplevel()
    Real_Window.config(width=400, height=200)
    Real_Window.title("Real Numbers ")
    Real_Window.geometry("775x245")
    Label(Real_Window, text="Real Numbers DFA").pack()
    dot_representation3 = '''
                digraph finite_state_machine {
                    rankdir=LR;
                    size="8,5"
                    node [shape = doublecircle]; q4,q6 ;
                    node [shape = circle];
                    node [start = true]; q1 ;
                    q0 [shape = point];
                    q0->q1 [label = " "];
                    q1 -> q2 [label = "[0-9]"];
                    q1 -> q7 [label = "any other char"];
                    q2 -> q3 [label = "."];
                    q2 -> q7 [label = "any other char"];
                    q3-> q4 [label = "[0-9]"];
                    q3-> q7 [label = "any other char"];
                    q4 -> q4 [label = "[0-9]"];
                    q4-> q5 [label = "e"];
                    q4-> q7 [label = "any other char"];
                    q5-> q6 [label = "[0-9]"];
                    q5-> q7 [label = "any other char"];
                    q6-> q6 [label = "[0-9]"];
                    q6-> q7 [label = "any other char"];
                    q7 -> q7 [label = "any other char"];
                    q2->q2 [label = "[0-9]"];
                    
                }
                '''
    # Generate the DFA diagram as an image
    graph2 = Source(dot_representation3, format='png')
    graph2.render(filename='Real_No')
    # Load the image into Tkinter
    image2 = ImageTk.PhotoImage(Image.open('Real_No.png'))
    panel = tk.Label(Real_Window, image=image2)
    panel.pack(fill="both", expand=True)
    panel.config(Real_Window)


def Operator():
    Operator_Window = tk.Toplevel()
    Operator_Window.config(width=400, height=200)
    Operator_Window.title("Operator_DFA")
    Operator_Window.geometry("780x480")
    Label(Operator_Window, text="Operators_DFA").pack()
    dot_representation4 = '''
             digraph finite_state_machine {
    rankdir=LR;
    size="8,5";
    node [shape = doublecircle]; q2,q3,q4,q5,q6,q7,q8;
    node [shape = circle];
    q0[shape = point]
    q0->q1 [label = " "];
    q1 -> q2 [label = "\:"];
    q2 -> q3 [label = "\="];
    q3 -> reject [label = "any other char"];

    q1 -> q4 [label = "\<"];
    q4 -> q5 [label = "\>,\="];
    q5 -> reject [label = "any other char"];

    q1 -> q6 [label = "\>"];
    q6 -> q7 [label = "\="];
    q7 -> reject [label = "any other char"];

    q1 -> q8 [label = "\~,\*,\/,\+,\-,\&,\|,\!,\{,\},\(,\),\[, \],'',\=,\,"];
    q1 -> reject [label = "any other char"];

    q2 -> reject [label = "any other char"];
    q4 -> reject [label = "any other char"];
    q6 -> reject [label = "any other char"];
    q8 -> reject [label = "any other char"];
}

                '''
    # Generate the DFA diagram as an image
    graph4 = Source(dot_representation4, format='png')
    graph4.render(filename='Operator_DFA')
    # Load the image into Tkinter
    image4 = ImageTk.PhotoImage(Image.open('Operator_DFA.png'))
    panel = tk.Label(Operator_Window, image=image4)
    panel.pack(fill="both", expand=True)
    panel.config(Operator_Window)


def String():
    String_Window = tk.Toplevel()
    String_Window.config(width=400, height=200)
    String_Window.title("String ")
    String_Window.geometry("705x175")
    Label(String_Window, text="String_DFA").pack()
    dot_representation3 = '''
                digraph finite_state_machine {
                    rankdir=LR;
                    size="8,5"
                    node [shape = doublecircle]; q3 ;
                    node [shape = circle];
                    q0[shape = point]
                    q0->q1 [label = " "];
                    q1 -> q2 [label = "'"];
                    q2 -> q3 [label = ","];
                    q1 -> reject [label = "any other char"];
                    reject -> reject [label = "any other char"];
                    q3-> reject [label = "any other char"];
                    q2->q2 [label = "any other char"];
                    
                }
                '''
    # Generate the DFA diagram as an image
    graph5 = Source(dot_representation3, format='png')
    graph5.render(filename='String_DFA')
    # Load the image into Tkinter
    image4 = ImageTk.PhotoImage(Image.open('String_DFA.png'))
    panel = tk.Label(String_Window, image=image4)
    panel.pack(fill="both", expand=True)
    panel.config(String_Window)


def Comment():
    Comment_Window = tk.Toplevel()
    Comment_Window.config(width=400, height=200)
    Comment_Window.title("Comment ")
    Comment_Window.geometry("775x345")
    Label(Comment_Window, text="Comment_DFA").pack()
    dot_representation3 = '''
                digraph finite_state_machine {
                    rankdir=LR;
                    size="8,5"
                    node [shape = doublecircle]; q4,q7 ;
                    node [shape = circle];
                    q1 -> q2 [label = "{"];
                    q2 -> q5 [label = "*"];
                    q2 -> q3 [label = "any other char"];
                    q2->q4 [label = "}"];
                    reject -> reject [label = "any other char"];
                    q1->reject [label = "any other char"];
                    q3->q3 [label = "any other char"];
                    q3->q4 [label = "}"];
                    q4->reject[label = "any other char"];
                    q3-> reject [label = "any other char"];
                    q5->q5 [label = "any other char"];
                    q5->q6 [label ="*"];
                    q6->q5 [label = "any other char"];
                    q6->q7 [label = "}"];
                    q7->reject [label = "any other char"];
                }
                '''
    # Generate the DFA diagram as an image
    graph6 = Source(dot_representation3, format='png')
    graph6.render(filename='Comment_DFA')
    # Load the image into Tkinter
    image5 = ImageTk.PhotoImage(Image.open('Comment_DFA.png'))
    panel = tk.Label(Comment_Window, image=image5)
    panel.pack(fill="both", expand=True)
    panel.config(Comment_Window)


def Dfa_new_window():
    DFA_Window = tk.Toplevel()
    DFA_Window.config(bg=window_bg)
    DFA_Window.geometry("500x400")
    DFA_Window.title("DFA's Window")
    Identifier_Button = tk.Button(DFA_Window, text="Identifier", command=Identifier, bg=button)
    Identifier_Button.config(command=Identifier, width=10)
    Identifier_Button.pack(padx=10, pady=10)
    Integer_Button = tk.Button(DFA_Window, text="Integer", command=Integer, bg=button)
    Integer_Button.config(command=Integer, width=10)
    Integer_Button.pack(padx=10, pady=10)
    Real_Numbers_Button = tk.Button(DFA_Window, text="Real Numbers", command=Real, bg=button)
    Real_Numbers_Button.config(command=Real, width=10)
    Real_Numbers_Button.pack(padx=10, pady=10)
    Operator_Button = tk.Button(DFA_Window, text="Operators", command=Operator, bg=button)
    Operator_Button.config(command=Operator, width=10)
    Operator_Button.pack(padx=10, pady=10)
    String_Button = tk.Button(DFA_Window, text="String", command=String, bg=button)
    String_Button.config(command=String, width=10)
    String_Button.pack(padx=10, pady=10)
    String_Button = tk.Button(DFA_Window, text="Comment", command=Comment, bg=button)
    String_Button.config(command=Comment, width=10)
    String_Button.pack(padx=10, pady=10)

def Scan(sourceCode):
    scanner = Scanner()
    tokens = scanner.scan(sourceCode)
    parser = RDParser(tokens)
    tree = parser.parse()
    display_error_list(parser.errors)
    draw_nltk_tree(tree)
    # S_window = tk.Toplevel()
    # S_window.geometry("600x400")
    # S_window.config(bg=window_bg)
    # S_window.title("Scan Window")
    # error = tk.Label(S_window, text="Error List: ", bg=window_bg, font=("Arial", 15))
    # error.grid(row=0, column=0, columnspan=2)
    # listbox = tk.Listbox(S_window, font=("Arial", 10, "bold"), borderwidth=0, width=25, height=10)
    # listbox.grid(row=1, column=0)
    # for i in range(len(Error)):
    #     listbox.insert(i, Error[i])

def Parser():
    window_Pars = tk.Toplevel()
    window_Pars.geometry("600x400")
    window_Pars.config(bg=window_bg)
    window_Pars.title = ("Parser Window")
    text_label = tk.Label(window_Pars, text="Enter your code: ", bg=window_bg, font=("Arial", 15))
    text_label.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='e')
    text = tk.Text(window_Pars, font=("Courier", 10), width=60, height=15)
    text.grid(row=2, column=1, columnspan=3)
    Scan_Button = tk.Button(window_Pars, command=lambda:Scan( text.get(1.0, "end-1c")), text="Scan", bg=button)
    Scan_Button.config(width=15)
    Scan_Button.grid(row=3, column=2, columnspan=2, padx=10, pady=10)




root = tk.Tk()
root.config(bg=window_bg)
root.geometry("500x200")
Parsar_Button = tk.Button(root, command=Parser, text="Parser", bg=button)
Parsar_Button.config(text="Parser", width=10)
Parsar_Button.pack(padx=10, pady=10)
DFA_newWindow_Button = tk.Button(root, command=Dfa_new_window, text="DFA's", bg=button)
DFA_newWindow_Button.config(command=Dfa_new_window, text="DFA's", width=10)
DFA_newWindow_Button.pack(padx=10, pady=10)
root.mainloop()
