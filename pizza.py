import tkinter as tk
from tkinter import ttk
from time import strftime
import os
from tkinter import messagebox
import textwrap
from fpdf import FPDF

main = tk.Tk()
order_no = 0
main.title("Pizza Bill Generator")
main.geometry("1080x860")
main.minsize(1080,860)
main.configure(bg='white')
main.state('zoomed')
main.columnconfigure(0,weight=1)
main.columnconfigure(1,weight=1)

header1 = '\t\t\t\t---CASH BILL---\n\n'
header2 = '\n\nSNO\tPARTICULARS\t\t\tRATE\tEXTRA\tPERQTY\tQTY\tTOTAL'
seperator = '\n---------------------------------------------------------------------------------\n'

pizza = ['Pan Pizza','Stuffed Crust','Regular Pizza']
toppings = ['Onion','Cheese','Tomato','Baby Corn']
priceA = [249.0,199.0,99.0]
priceB= [50.0,80.0,40.0,30.0]

def text_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')

style = ttk.Style(main)
style.theme_use('clam')
style.configure('TFrame', background='white')
style.configure('TLabelframe', background='white')
style.configure('TRadiobutton', background='white')
style.configure('TLabelframe.Label', background='white')
style.configure('TCheckbutton', background='white')
style.configure('TLabel', background='white')
style.configure('TButton', background = '#4A6984', foreground = 'white')
style.map('TButton', background=[('active','#4A6984')])

def add_to_bill():
    quantity = int(qty.get())
    pizzaName = pizza[var.get()]
    pizzaPrice = priceA[var.get()]
    t = ''
    tprice = 0
    price = pizzaPrice
    if(CheckVar1.get() == 1):
        tprice += priceB[0]
        t += toppings[0] + ' '
    if(CheckVar2.get() == 1):
        tprice += priceB[1]
        t += toppings[1] + ' '
    if(CheckVar3.get() == 1):
        tprice += priceB[2]
        t += toppings[2] + ' '
    if(CheckVar4.get() == 1):
        tprice += priceB[3]
        t += toppings[3] + ' '
    priceperqty = (pizzaPrice + tprice)
    price = priceperqty * quantity
    
    temp = (pizzaName,t,str(pizzaPrice),str(tprice),str(priceperqty),str(quantity),str(price))
    tree.insert('','end',values=temp)
    var.set(0)
    CheckVar1.set(0)
    CheckVar2.set(0)
    CheckVar3.set(0)
    CheckVar4.set(0)
    qty.delete(0,'end')
    qty.insert('end','1')
    qty.focus_set()

def generate_order_no():
    global order_no
    order_no = strftime("%Y%m%d%I%M%S")
    orderno.delete(0,'end')
    orderno.insert('end',order_no)

def clear_all():
    orderno.delete(0,'end')
    generate_order_no()
    customer.delete(0,'end')
    qty.delete(0,'end')
    qty.insert('end','1')
    var.set(0)
    CheckVar1.set(0)
    CheckVar2.set(0)
    CheckVar3.set(0)
    CheckVar4.set(0)
    for i in tree.selection():
        pass
    customer.focus_set()

def delete_item():
    selected_item = tree.selection()[0]
    values = tuple(tree.item(selected_item)['values'])
    tree.delete(selected_item)

def generate_bill():
    newView = tk.Toplevel(main)
    newView.geometry('800x600')
    newView.resizable(0,0)
    bill = []
    for item in tree.get_children():
        bill.append(tree.item(item, 'values'))
    def save_bill():
        
        try:
            os.mkdir('saved_bill')
        except:
            pass
        text = billView.get('1.0','end')
        text_to_pdf(text, 'saved_bill/{}_bill.pdf'.format(order_no))
        messagebox.showinfo('Success','Bill Saved Successfully. Check out the bill at "saved_bill" directory')
        newView.destroy()
    
    button2 = ttk.Button(newView,text="Save Bill",width=15,command=save_bill)
    button2.pack(anchor='ne',padx=10,pady=10)
    sb2 = ttk.Scrollbar(newView,orient='vertical')
    billView = tk.Text(newView,yscrollcommand=sb2.set,width=45)
    billView.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,pady=10,padx=(10,0))
    sb2.configure(command=billView.yview)
    sb2.pack(side=tk.RIGHT,fill=tk.Y,pady=10,padx=(0,10))

    customerName = customer.get()
    orderNo = orderno.get()
    billView.delete("1.0","end")
    billView.insert(tk.END,header1)
    billView.insert(tk.END,'CUSTOMER NAME: '+customerName)
    billView.insert(tk.END,'\nORDER NO: '+orderNo)
    billView.insert(tk.END,header2+seperator)

    n = len(bill)
    if(n!=0):
        Tot = 0.0
        for i in range(n):
            a = '{:>3}\t'.format(i+1)
            b = '{}\t\t\t'.format(bill[i][0])
            c = '{:>6}\t'.format(bill[i][2])
            d = '{:>6}\t'.format(bill[i][3])
            e = '{:>6}\t'.format(bill[i][4])
            f = '{:>3}\t'.format(bill[i][5])
            g = '{:>7}\n'.format(bill[i][6])
            h = bill[i][1] + '\n'
            if(h != ''):
                h = '\t' + h
            temp = a + b + c + d + e + f + g + h
            billView.insert(tk.END,temp)
            Tot += float(bill[i][6])
        billView.insert(tk.END,seperator+'\t\t\t\t\t\t\t    Total: '+str(Tot))

    newView.mainloop()

frame1 = ttk.Frame(main)
frame1.grid(row=0,column=0,columnspan=2)
frame1.columnconfigure(0,weight=1)
title = ttk.Label(frame1,text="Pizza Bill Generator",font=("Arial",14))
title.grid(row=0,column=0,columnspan=2,sticky='ew',padx=10,pady=10)

frame2 = ttk.Frame(main)
frame2.grid(row=1,column=0,columnspan=2)

frame2.columnconfigure(0,weight=1)
frame2.columnconfigure(1,weight=1)
frame2.columnconfigure(2,weight=1)

labelframe1 = ttk.LabelFrame(frame2,text="Order No")
labelframe2 = ttk.LabelFrame(frame2,text="Customer Name")
labelframe3 = ttk.LabelFrame(frame2,text="Quantity")

labelframe1.grid(row=0,column=0,padx=10,pady=5)
labelframe2.grid(row=0,column=1,padx=10,pady=5)
labelframe3.grid(row=0,column=2,padx=10,pady=5)

orderno = ttk.Entry(labelframe1,font=('Arial',14))
customer = ttk.Entry(labelframe2,font=('Arial',14))
qty = ttk.Entry(labelframe3,font=('Arial',14))

labelframe1.columnconfigure(0,weight=1)
labelframe2.columnconfigure(0,weight=1)
labelframe3.columnconfigure(0,weight=1)

orderno.grid(row=0,column=0,padx=10,pady=5)
customer.grid(row=0,column=0,padx=10,pady=5)
qty.grid(row=0,column=0,padx=10,pady=5)

frame3 = ttk.Frame(main)
frame3.grid(row=2,column=0,columnspan=2,padx=10,pady=5,sticky='ew')
frame3.columnconfigure(0,weight=1)
frame3.columnconfigure(1,weight=1)

labelframe4 = ttk.LabelFrame(frame3,text="Pizza Type")
labelframe5 = ttk.LabelFrame(frame3,text="Toppings")

labelframe4.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')
labelframe5.grid(row=0,column=1,padx=10,pady=10,sticky='nsew')

var = tk.IntVar()
R1 = ttk.Radiobutton(labelframe4, text="Pan Pizza\tRs.249", variable=var, value=0)
R1.grid(row=0,column=0,padx=10,pady=10,sticky='w')

R2 = ttk.Radiobutton(labelframe4, text="Stuffed Crust\tRs.199", variable=var, value=1)
R2.grid(row=1,column=0,padx=10,pady=10,sticky='w')

R3 = ttk.Radiobutton(labelframe4, text="Regular\t\tRs.99", variable=var, value=2)
R3.grid(row=2,column=0,padx=10,pady=10,sticky='w')

CheckVar1 = tk.IntVar()
CheckVar2 = tk.IntVar()
CheckVar3 = tk.IntVar()
CheckVar4 = tk.IntVar()
C1 = ttk.Checkbutton(labelframe5, text = "Onion\t\tRs.50", variable = CheckVar1, onvalue = 1, offvalue = 0)
C2 = ttk.Checkbutton(labelframe5, text = "Cheese\t\tRs.80", variable = CheckVar2, onvalue = 1, offvalue = 0)
C3 = ttk.Checkbutton(labelframe5, text = "Tomato\t\tRs.40", variable = CheckVar3, onvalue = 1, offvalue = 0)
C4 = ttk.Checkbutton(labelframe5, text = "Baby Corn\tRs.30", variable = CheckVar4, onvalue = 1, offvalue = 0)
C1.grid(row=0,column=0,padx=10,pady=10,sticky='w')
C2.grid(row=1,column=0,padx=10,pady=10,sticky='w')
C3.grid(row=2,column=0,padx=10,pady=10,sticky='w')
C4.grid(row=3,column=0,padx=10,pady=10,sticky='w')

frame4 = ttk.Frame(main)
frame4.grid(row=3,column=0,columnspan=2,padx=10,pady=10,sticky='nsew')
frame4.columnconfigure(0,weight=1)
frame4.columnconfigure(1,weight=1)
frame4.rowconfigure(0,weight=1)

bill = ttk.Frame(frame4)
bill.grid(row=0,column=0,sticky='nsew',padx=10,pady=5)

columnids = ('c1','c2','c3','c4','c5','c6','c7')

sb = ttk.Scrollbar(bill,orient='vertical')
tree = ttk.Treeview(bill,yscrollcommand=sb.set,column=columnids,show='headings')

tree.column('c3',width=110)
tree.column('c4',width=110)
tree.column('c5',width=110)
tree.column('c6',width=70)
tree.column('c7',width=110)

tree.heading('c1',text='Pizza Name')
tree.heading('c2',text='Toppings')
tree.heading('c3',text='Rate')
tree.heading('c4',text='Extra Rate')
tree.heading('c5',text='Rate per qty')
tree.heading('c6',text='Quantity')
tree.heading('c7',text='Rate')

tree.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
sb.configure(command=tree.yview)
sb.pack(side=tk.RIGHT,fill=tk.Y)

frame5 = ttk.Frame(frame4)
frame5.grid(row=0,column=1,padx=10,pady=10,sticky='nsew')

button0 = ttk.Button(frame5,text="Add to Bill",width=15,command=add_to_bill)
button0.pack(anchor='center',padx=10,pady=10)

button1 = ttk.Button(frame5,text="Generate Bill",width=15,command=generate_bill)
button1.pack(anchor='center',padx=10,pady=10)

button3 = ttk.Button(frame5,text="Clear All",width=15,command=clear_all)
button3.pack(anchor='center',padx=10,pady=10)

button4 = ttk.Button(frame5,text="Delete Item",width=15,command=delete_item)
button4.pack(anchor='center',padx=10,pady=10)

generate_order_no()
qty.insert('end','1')
customer.focus_set()

main.mainloop()
