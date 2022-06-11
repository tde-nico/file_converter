from tkinter import messagebox
import tkinter as tkr
import os
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


#--------------------------------------- INITIALIZATION ---------------------------------------#


# Version: 1.6.4

path = os.getcwd() + '\\'
dirs = ['IN\\', 'OUT\\', 'Cache\\'] # [ Input dir , Output dir , Cache dir ]
column = 0
extension = ''


Inputs = [('jpg','jpg'),('png','png'),('pdf','pdf'),('svg','svg')]
Mods = [('default','default'),('merge','merge')]
Outputs = [('pdf','pdf'),('jpg','jpg'),('png','png'),('ico','ico')]


display = tkr.Tk()
display.title('Converter')


#--------------------------------------- CHECK fUNCTION ---------------------------------------#


def check_dir():
    for folder in dirs:
        if not os.path.exists(path + folder):
            os.mkdir(folder)


#--------------------------------------- GUI fUNCTION ---------------------------------------#


def new_frame(title, options, input_value):
    global column
    frame = tkr.LabelFrame(display, text=title, padx=5, pady=5)
    frame.grid(padx=10,pady=10,row=0,column=column)
    column += 1
    input_value.set(options[0][0])

    for row in range(len(options)):
        tkr.Radiobutton(frame, text=options[row][0], variable=input_value, value=options[row][1]).grid(row=row, column=column)
    column += 1


#--------------------------------------- MANIPULATION fUNCTIONS ---------------------------------------#           


class Converter():

    
    def image_default_pdf(in_folder=dirs[0], out_folder=dirs[1]):
        for jpg in os.listdir(path + in_folder):
            image_to_convert = Image.open(path + in_folder + jpg)
            image_converted = image_to_convert.convert('RGB')
            image_converted.save(out_folder + jpg[:-4] + '.pdf')
        

    def pdf_merge_pdf(in_folder=dirs[0], out_folder=dirs[1]):
        mergedObject = PdfFileMerger()
        for pdf in os.listdir(path + in_folder):
            if '.pdf' in pdf:
                mergedObject.append(PdfFileReader(in_folder + pdf[:-4] + '.pdf', 'rb'))
        mergedObject.write(out_folder + "Merged_Out.pdf")


    def image_default_ico(in_folder=dirs[0], out_folder=dirs[1]):
        for jpg in os.listdir(path + in_folder):
            image = Image.open(in_folder + jpg)
            image.save(out_folder + jpg[:-4] + '.ico',format = 'ICO', sizes=[(64,64)])


    def svg_default_image(in_folder=dirs[0], out_folder=dirs[1]):
        for jpg in os.listdir(path + in_folder):
            image = svg2rlg(in_folder + jpg)
            renderPM.drawToFile(image, out_folder + jpg[:-4] + '.' + extension, fmt=extension.upper())


#--------------------------------------- SECONDARY fUNCTIONS ---------------------------------------#

            
    def image_merge_pdf(in_folder=dirs[2]):
        Converter.image_default_pdf(out_folder=in_folder)
        Converter.pdf_merge_pdf(in_folder=in_folder)
        clean_cache()
    

    def svg_default_pdf():
        Converter.svg_default_image(out_folder=dirs[2])
        Converter.image_default_pdf(in_folder=dirs[2])
        clean_cache()


    def svg_merge_pdf():
        Converter.svg_default_image(out_folder=dirs[2])
        Converter.image_default_pdf(in_folder=dirs[2], out_folder=dirs[2])
        Converter.pdf_merge_pdf(in_folder=dirs[2])
        clean_cache()


#--------------------------------------- CACHE CLEAN fUNCTION ---------------------------------------#


def clean_cache():
    for file in os.listdir(path + dirs[2]):
        os.remove(dirs[2] + file)


#--------------------------------------- EXECUTION fUNCTION ---------------------------------------#

       
def execute(function):
    try:
        function()
        
        messagebox.showinfo('Info', 'Success')
    except Exception as er:
        print(er)
        messagebox.showerror('Error', 'Error')


#--------------------------------------- FUNCTION BUILDER FUNCTION ---------------------------------------#


def function_builder(inp, mod, out):
    global extension
    extension = out
    if inp == 'jpg' or inp == 'png':
        inp = 'image'
    if out == 'jpg' or out == 'png':
        out = 'image'
    
    execute(getattr(Converter, str(inp) + '_' + str(mod) + '_' + str(out)))


#--------------------------------------- MAIN LOOP ---------------------------------------#


check_dir()



input_option = tkr.StringVar()
mod_option = tkr.StringVar()
output_option = tkr.StringVar()


new_frame('Input', Inputs, input_option)
new_frame('Mods', Mods, mod_option)
new_frame('Output', Outputs, output_option)

conversion_button = tkr.Button(display, text='Convert', padx=10, pady=30, command=lambda: function_builder(input_option.get(), mod_option.get(), output_option.get()))
conversion_button.grid(row=0, column=column, padx=10)

display.mainloop()















