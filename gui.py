# Importing libraries
import cv2
import os

from ocr import OCR
import tkinter as tk
from PIL import ImageTk,Image 
from tkinter.filedialog import askopenfilename
from tkinter import Label, Toplevel, messagebox, Button, Frame, Text, Scrollbar, Listbox, RAISED, Radiobutton, Entry, LabelFrame



class OcrGui():
    def __init__(self, master):

        # Root Frame Properties
        self.master = master
        self.master.title("Simple OCR Application")
        self.master.iconphoto(True, tk.PhotoImage(file='eye_vision.png'))
        self.master.geometry("1200x700+100+25")
        # self.master.resizable(True, True)

        #Storing loaded images
        self.image = {}
        # Creating an ocr object
        self.ocr_applier = OCR()

        # Main functions for each frame in main window
        self.header_frame()
        self.show_image_frame()
        self.operation_frame()
        self.image_listbox_frame()
        self.show_message_frame()

        self.master.mainloop()


    def __import_image_func(self):

        filetypes = (("PNG image format", "*.png"),
                    ("JPEG image format", "*.jpeg"),
                    ("JPG image format", "*.jpg"),
                    ("BMP image format", "*.bmp"))

        filepath = askopenfilename(title='Open your image file', initialdir='/', filetypes=filetypes)
        filename = os.path.basename(filepath)

        if filename in self.image:
            messagebox.showerror("Simple OCR", "Image already exists")
        elif type(cv2.imread(filepath, 0)) != type(None):
            self.image[filename] = (cv2.imread(filepath, 0))
            self.image_listbox(1)
        else:
            messagebox.showwarning("Simple OCR", "No Image is selected")
    

    def __delete_image_func(self):

        if self.imagelist.curselection() :
            selected_image = self.imagelist.get(tk.ACTIVE)
            self.image.pop(selected_image)
            messagebox.showinfo("Simple OCR", "Image deleted successfully")
            self.show_message(f"{selected_image} deleted successfully\n")
            self.show_message("-----------------------------\n")
            self.image_listbox(2)  
        else:
            messagebox.showwarning("Simple OCR", "No Image is selected")

    def __show_image_opencv_func(self):

        if self.imagelist.curselection() :
            selected_image = self.imagelist.get(tk.ACTIVE)
            cv2.imshow(selected_image, self.image[selected_image])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            messagebox.showwarning("Simple OCR", "No Image is selected")

    def __apply_auto_skew_correction_func(self):

        def apply():

            if self.imagelist.curselection() :
                selection = f"image={self.imagelist.get(tk.ACTIVE)}\n"
                img = self.ocr_applier.auto_skew_correction_buttion(self.image[self.imagelist.get(tk.ACTIVE)])
                self.image[f"{self.imagelist.get(tk.ACTIVE)}+asc"] = img
                messagebox.showinfo("Simple OCR","Done!")
                self.show_message(f"Auto Skew Correction\n-> {selection}\n")
                self.show_message(f"{self.imagelist.get(tk.ACTIVE)}+asc is created\n")
                self.show_message("-----------------------------\n")
                self.image_listbox()
            else:
                messagebox.showwarning("Simple OCR", "No Image is selected")

        top = tk.Toplevel(self.master)
        top.geometry("400x500+150+100")

        title = Label(top,bd=10, text="Auto Skew Correction")
        title.pack()
        labelframe = LabelFrame(top)
        labelframe.pack(fill="both", expand="yes")

        apply_button = Button(labelframe, bd=5, fg='red', text="apply", command=apply)
        apply_button.pack()
    
    def __apply_thresh_func(self):

        def apply():

            if self.imagelist.curselection() :
                selection = f"image={self.imagelist.get(tk.ACTIVE)}\nthreshold_model={var1.get()}\nthresh_value={thresh_val_entry.get()}\nblock_size={var2.get()}\n"

                img = self.ocr_applier.threshold(self.image[self.imagelist.get(tk.ACTIVE)], var1.get(), int(thresh_val_entry.get()), var2.get())
                self.image[f"{self.imagelist.get(tk.ACTIVE)}+thresh_{var1.get()}"] = img
                messagebox.showinfo("Simple OCR","Done!")
                self.show_message(f"threshold\n-> {selection}\n")
                self.show_message(f"{self.imagelist.get(tk.ACTIVE)}+thresh_{var1.get()} is created\n")
                self.show_message("-----------------------------\n")
                self.image_listbox()
            else:
                messagebox.showwarning("Simple OCR", "No Image is selected")

        top = tk.Toplevel(self.master)
        top.geometry("400x500+150+100")

        title = Label(top,bd=10, text="Thresholding")
        title.pack()
        labelframe = LabelFrame(top)
        labelframe.pack(fill="both", expand="yes")
        
        var1 = tk.StringVar()
        thresh_model_1 = Radiobutton(labelframe, text="BINARY", variable=var1, value="BINARY")
        thresh_model_1.pack()
        thresh_model_2 = Radiobutton(labelframe, text="BINARY_INV", variable=var1, value="BINARY_INV")
        thresh_model_2.pack()
        thresh_model_3 = Radiobutton(labelframe, text="ADAPTIVE MEAN", variable=var1, value="ADAPTIVE MEAN")
        thresh_model_3.pack()
        thresh_model_4 = Radiobutton(labelframe, text="ADAPTIVE GAUSSIAN", variable=var1, value="ADAPTIVE GAUSSIAN")
        thresh_model_4.pack()
        thresh_model_5 = Radiobutton(labelframe, text="OTSU", variable=var1, value="OTSU")
        thresh_model_5.pack()

        thresh_val_label = Label(labelframe, text="threshold value")
        thresh_val_label.pack()

        thresh_val_entry = Entry(labelframe, bd=5)
        thresh_val_entry.pack()

        var2 = tk.IntVar()
        blocksize_1 = Radiobutton(labelframe, text="Block size = (3)", variable=var2, value=3)
        blocksize_1.pack()
        blocksize_2 = Radiobutton(labelframe, text="Block size = (5)", variable=var2, value=5)
        blocksize_2.pack()

        apply_button = Button(labelframe, bd=5, fg='red', text="apply", command=apply)
        apply_button.pack()

    def __apply_erode_func(self):

        def apply():

            if self.imagelist.curselection() :
                try:
                    selection = f"image={self.imagelist.get(tk.ACTIVE)}\nkernel_x={kernel_x_entry.get()}\nkernel_y={kernel_y_entry.get()}\nstructure={var1.get()}\niterations=1\n"
                    img = self.ocr_applier.erode(self.image[self.imagelist.get(tk.ACTIVE)], int(kernel_x_entry.get()), int(kernel_y_entry.get()), var1.get())
                    self.image[f"{self.imagelist.get(tk.ACTIVE)}+erode"] = img
                    messagebox.showinfo("Simple OCR","Done!")
                    self.show_message(f"erosion\n-> {selection}\n")
                    self.show_message(f"{self.imagelist.get(tk.ACTIVE)}+erode is created\n")
                    self.show_message("-----------------------------\n")
                    self.image_listbox()
                except:
                    messagebox.showwarning("Simple OCR", "Fill all Options")
            else:
                messagebox.showwarning("Simple OCR", "No Image is selected")
        
        # image, kernel_x, kernel_y, structure="rectangle",
    
        top = tk.Toplevel(self.master)
        top.geometry("400x500+150+100")
        title = Label(top,bd=10, text="Erosion")
        title.pack()
        labelframe = LabelFrame(top)
        labelframe.pack(fill="both", expand="yes")

        kernel_x_label = Label(labelframe, text=" kernel x")
        kernel_x_label.pack()
        kernel_x_entry = Entry(labelframe, bd=5)
        kernel_x_entry.pack()

        kernel_y_label = Label(labelframe, text="kernel y")
        kernel_y_label.pack()
        kernel_y_entry = Entry(labelframe, bd=5)
        kernel_y_entry.pack()

        var1 = tk.StringVar()
        st_model_1 = Radiobutton(labelframe, text="rectangle", variable=var1, value="rectangle")
        st_model_1.pack()
        st_model_2 = Radiobutton(labelframe, text="ellipse", variable=var1, value="ellipse")
        st_model_2.pack()
        st_model_3 = Radiobutton(labelframe, text="cross", variable=var1, value="cross")
        st_model_3.pack()
        
        apply_button = Button(labelframe, bd=5, fg='red', text="apply", command=apply)
        apply_button.pack()


    def __apply_dilate_func(self):
        def apply():
            if self.imagelist.curselection() :
                selection = f"image={self.imagelist.get(tk.ACTIVE)}\nkernel_x={kernel_x_entry.get()}\nkernel_y={kernel_y_entry.get()}\nstructure={var1.get()}\niterations=1\n"
                img = self.ocr_applier.dilate(self.image[self.imagelist.get(tk.ACTIVE)], int(kernel_x_entry.get()), int(kernel_y_entry.get()), var1.get())
                self.image[f"{self.imagelist.get(tk.ACTIVE)}+dilate"] = img
                messagebox.showinfo("Simple OCR","Done!")
                self.show_message(f"dilation\n-> {selection}\n")
                self.show_message(f"{self.imagelist.get(tk.ACTIVE)}+dilate is created\n")
                self.show_message("-----------------------------\n")
                self.image_listbox()
            else:
                messagebox.showwarning("Simple OCR", "No Image is selected")
        
        
        # image, kernel_x, kernel_y, structure="rectangle",
    
        top = tk.Toplevel(self.master)
        top.geometry("400x500+150+100")
        title = Label(top,bd=10, text="Dilation")
        title.pack()
        labelframe = LabelFrame(top)
        labelframe.pack(fill="both", expand="yes")

        kernel_x_label = Label(labelframe, text=" kernel x")
        kernel_x_label.pack()
        kernel_x_entry = Entry(labelframe, bd=5)
        kernel_x_entry.pack()

        kernel_y_label = Label(labelframe, text="kernel y")
        kernel_y_label.pack()
        kernel_y_entry = Entry(labelframe, bd=5)
        kernel_y_entry.pack()

        var1 = tk.StringVar()
        st_model_1 = Radiobutton(labelframe, text="rectangle", variable=var1, value="rectangle")
        st_model_1.pack()
        st_model_2 = Radiobutton(labelframe, text="ellipse", variable=var1, value="ellipse")
        st_model_2.pack()
        st_model_3 = Radiobutton(labelframe, text="cross", variable=var1, value="cross")
        st_model_3.pack()
        
        apply_button = Button(labelframe, bd=5, fg='red', text="apply", command=apply)
        apply_button.pack()

    def __apply_close_func(self):
        def apply():
            if self.imagelist.curselection() :
                selection = f"image={self.imagelist.get(tk.ACTIVE)}\nkernel_x={kernel_x_entry.get()}\nkernel_y={kernel_y_entry.get()}\nstructure={var1.get()}\niterations=1\n"

                img = self.ocr_applier.close(self.image[self.imagelist.get(tk.ACTIVE)], int(kernel_x_entry.get()), int(kernel_y_entry.get()), var1.get())
                self.image[f"{self.imagelist.get(tk.ACTIVE)}+close"] = img
                messagebox.showinfo("Simple OCR","Done!")
                self.show_message(f"closing\n-> {selection}\n")
                self.show_message(f"{self.imagelist.get(tk.ACTIVE)}+close is created\n")
                self.show_message("-----------------------------\n")
                self.image_listbox()
            else:
                messagebox.showwarning("Simple OCR", "No Image is selected")

        # image, kernel_x, kernel_y, structure="rectangle",
    
        top = tk.Toplevel(self.master)
        top.geometry("400x500+150+100")
        title = Label(top,bd=10, text="Closing")
        title.pack()
        labelframe = LabelFrame(top)
        labelframe.pack(fill="both", expand="yes")

        kernel_x_label = Label(labelframe, text=" kernel x")
        kernel_x_label.pack()
        kernel_x_entry = Entry(labelframe, bd=5)
        kernel_x_entry.pack()

        kernel_y_label = Label(labelframe, text="kernel y")
        kernel_y_label.pack()
        kernel_y_entry = Entry(labelframe, bd=5)
        kernel_y_entry.pack()

        var1 = tk.StringVar()
        st_model_1 = Radiobutton(labelframe, text="rectangle", variable=var1, value="rectangle")
        st_model_1.pack()
        st_model_2 = Radiobutton(labelframe, text="ellipse", variable=var1, value="ellipse")
        st_model_2.pack()
        st_model_3 = Radiobutton(labelframe, text="cross", variable=var1, value="cross")
        st_model_3.pack()
        
        apply_button = Button(labelframe, bd=5, fg='red', text="apply", command=apply)
        apply_button.pack()

    def __apply_open_func(self):
        def apply():
            if self.imagelist.curselection() :
                selection = f"image={self.imagelist.get(tk.ACTIVE)}\nkernel_x={kernel_x_entry.get()}\nkernel_y={kernel_y_entry.get()}\nstructure={var1.get()}\niterations=1\n"

                img = self.ocr_applier.open(self.image[self.imagelist.get(tk.ACTIVE)], int(kernel_x_entry.get()), int(kernel_y_entry.get()), var1.get())
                self.image[f"{self.imagelist.get(tk.ACTIVE)}+open"] = img
                messagebox.showinfo("Simple OCR","Done!")
                self.show_message(f"opening\n-> {selection}\n")
                self.show_message(f"{self.imagelist.get(tk.ACTIVE)}+open is created\n")
                self.show_message("-----------------------------\n")
                self.image_listbox()
            else:
                messagebox.showwarning("Simple OCR", "No Image is selected")
            
        top = tk.Toplevel(self.master)
        top.geometry("400x500+150+100")
        title = Label(top,bd=10, text="Opening")
        title.pack()
        labelframe = LabelFrame(top)
        labelframe.pack(fill="both", expand="yes")

        kernel_x_label = Label(labelframe, text=" kernel x")
        kernel_x_label.pack()
        kernel_x_entry = Entry(labelframe, bd=5)
        kernel_x_entry.pack()

        kernel_y_label = Label(labelframe, text="kernel y")
        kernel_y_label.pack()
        kernel_y_entry = Entry(labelframe, bd=5)
        kernel_y_entry.pack()

        var1 = tk.StringVar()
        st_model_1 = Radiobutton(labelframe, text="rectangle", variable=var1, value="rectangle")
        st_model_1.pack()
        st_model_2 = Radiobutton(labelframe, text="ellipse", variable=var1, value="ellipse")
        st_model_2.pack()
        st_model_3 = Radiobutton(labelframe, text="cross", variable=var1, value="cross")
        st_model_3.pack()
        
        apply_button = Button(labelframe, bd=5, fg='red', text="apply", command=apply)
        apply_button.pack()

    def __apply_sharpen_func(self):
        def apply():
            if self.imagelist.curselection() :
                selection = f"image={self.imagelist.get(tk.ACTIVE)}\nsharp_model={var1.get()}\n"

                img = self.ocr_applier.sharpen(self.image[self.imagelist.get(tk.ACTIVE)], var1.get())
                self.image[f"{self.imagelist.get(tk.ACTIVE)}+sharp_{var1.get()}"] = img
                messagebox.showinfo("Simple OCR","Done!")
                self.show_message(f"Sharpening\n-> {selection}\n")
                self.show_message(f"{self.imagelist.get(tk.ACTIVE)}+sharp_{var1.get()} is created\n")
                self.show_message("-----------------------------\n")
                self.image_listbox()
            else:
                messagebox.showwarning("Simple OCR", "No Image is selected")
            
        top = tk.Toplevel(self.master)
        top.geometry("400x500+150+100")
        title = Label(top,bd=10, text="Sharpening")
        title.pack()
        labelframe = LabelFrame(top)
        labelframe.pack(fill="both", expand="yes")

        var1 = tk.StringVar()
        st_model_1 = Radiobutton(labelframe, text="Weak", variable=var1, value="weak")
        st_model_1.pack()
        st_model_2 = Radiobutton(labelframe, text="Strong", variable=var1, value="strong")
        st_model_2.pack()
        
        apply_button = Button(labelframe, bd=5, fg='red', text="apply", command=apply)
        apply_button.pack()

    def __apply_blur_func(self):
        def apply():
            if self.imagelist.curselection() :
                if sigma_entry.get() == "":
                    sigma = 2
                else:
                    sigma=int(sigma_entry.get())
                selection = f"image={self.imagelist.get(tk.ACTIVE)}\nblur_model={var1.get()}\nblock_size={var2.get()}\nsigma={sigma}\n"
                img = self.ocr_applier.blur(self.image[self.imagelist.get(tk.ACTIVE)], var1.get(), var2.get(), sigma)
                self.image[f"{self.imagelist.get(tk.ACTIVE)}+blur_{var1.get()}"] = img
                messagebox.showinfo("Simple OCR","Done!")
                self.show_message(f"Blurring\n-> {selection}\n")
                self.show_message(f"{self.imagelist.get(tk.ACTIVE)}+blur_{var1.get()} is created\n")
                self.show_message("-----------------------------\n")
                self.image_listbox()
            else:
                messagebox.showwarning("Simple OCR", "No Image is selected")
            
        top = tk.Toplevel(self.master)
        top.geometry("400x500+150+100")
        title = Label(top,bd=10, text="Blurring")
        title.pack()
        labelframe = LabelFrame(top)
        labelframe.pack(fill="both", expand="yes")

        var1 = tk.StringVar()
        blur_model_1 = Radiobutton(labelframe, text="average", variable=var1, value="average")
        blur_model_1.pack()
        blur_model_2 = Radiobutton(labelframe, text="gaussian", variable=var1, value="gaussian")
        blur_model_2.pack()
        blur_model_3 = Radiobutton(labelframe, text="median", variable=var1, value="median")
        blur_model_3.pack()

        var2 = tk.IntVar()
        blocksize_1 = Radiobutton(labelframe, text="Block size = (3)", variable=var2, value=3)
        blocksize_1.pack()
        blocksize_2 = Radiobutton(labelframe, text="Block size = (5)", variable=var2, value=5)
        blocksize_2.pack()

        sigma_label = Label(labelframe, text="sigma for gaussian")
        sigma_label.pack()
        sigma_entry = Entry(labelframe, bd=5)
        sigma_entry.pack()
        
        apply_button = Button(labelframe, bd=5, fg='red', text="apply", command=apply)
        apply_button.pack()

    def __apply_crop_func(self):

        def apply():
            if self.imagelist.curselection() :

                selection = f"image={self.imagelist.get(tk.ACTIVE)}\n"
                img = self.ocr_applier.crop(self.image[self.imagelist.get(tk.ACTIVE)])
                self.image[f"{self.imagelist.get(tk.ACTIVE)}+crop"] = img
                messagebox.showinfo("Simple OCR","Done!")
                self.show_message(f"Cropping\n-> {selection}\n")
                self.show_message(f"{self.imagelist.get(tk.ACTIVE)}+crop is created\n")
                self.show_message("-----------------------------\n")
                self.image_listbox()
            else:
                messagebox.showwarning("Simple OCR", "No Image is selected")
            
        top = tk.Toplevel(self.master)
        top.geometry("400x500+150+100")

        title = Label(top,bd=10, text="Cropping")
        title.pack()
        labelframe = LabelFrame(top)
        labelframe.pack(fill="both", expand="yes")

        apply_button = Button(labelframe, bd=5, fg='red', text="apply", command=apply)
        apply_button.pack()
    

    def __apply_image2text_func(self):

        def apply():

            if self.imagelist.curselection() :

                selection = f"image={self.imagelist.get(tk.ACTIVE)}\nlang={var1.get()}\nexport_name={outputname_entry.get()}\n"
                data = self.ocr_applier.read_text(self.image[self.imagelist.get(tk.ACTIVE)], lang=var1.get(), to_txt_file=True, export_name=outputname_entry.get())
                messagebox.showinfo("Simple OCR","Done!")
                self.show_message(f"Image to Text\n-> {selection}\n")
                self.show_message(f"{self.imagelist.get(tk.ACTIVE)}'S text is extracted!\n")
                self.show_message("-----------------------------\n")
                self.image_listbox(2)
            else:
                messagebox.showwarning("Simple OCR", "No Image is selected")
        
        top = tk.Toplevel(self.master)
        top.geometry("400x500+150+100")

        title = Label(top,bd=10, text="Image to Text")
        title.pack()
        labelframe = LabelFrame(top)
        labelframe.pack(fill="both", expand="yes")

        langlabel = Label(labelframe, text="------------Select Language-----------")
        langlabel.pack()

        var1 = tk.StringVar()
        lang1 = Radiobutton(labelframe, text="English language", variable=var1, value="eng")
        lang1.pack()
        lang2 = Radiobutton(labelframe, text="Persian language", variable=var1, value="fas")
        lang2.pack()
        lang3 = Radiobutton(labelframe, text="English and Persian language", variable=var1, value="eng+fas")
        lang3.pack()


        outputname_label = Label(labelframe,bd=5, text="Name for outputfile")
        outputname_label.pack()
        outputname_entry = Entry(labelframe, bd=5)
        outputname_entry.pack()

        apply_button = Button(labelframe, text="apply", command=apply)
        apply_button.pack(side="bottom")


    def show_message(self, message):
            
            # showing message of operations
            self.description.insert(tk.INSERT, message)

    
    def header_frame(self):
 
        # A placeholder for header part
        self.titleFrame = Frame(self.master, bd=10)
        self.titleFrame.pack(fill='both')

        # Header Title
        self.title = Label(self.titleFrame, text="Simple OCR", relief=RAISED, font="Arial 22")
        self.title.pack(fill='y')

        # Header image 
        self.icon = Image.open("eye_vision.png")
        self.iconn = self.icon.resize((50,50), resample=Image.BICUBIC)
        self.ref_icon = ImageTk.PhotoImage(self.iconn)
        self.icon_label = Label(self.titleFrame, image=self.ref_icon)
        self.icon_label.image = self.ref_icon
        self.icon_label.pack()


    def show_image_frame(self):

        # A placeholder for image display
        self.imageFrame = Frame(self.master, bd=15)
        self.imageFrame.pack(side="left", fill='y')

        # A placeholer for displaying image
        self.image_label = Label(self.imageFrame, bd=5, padx=200, pady=200)

        # A Image display Button 
        self.img_show = Button(self.imageFrame, bd=5, text="show image", command=self.show_image)
        self.img_show.pack(side='top', fill='x')
        self.image_label.pack(side='top' , fill='both')


    def operation_frame(self):

        # A placeholder for operation buttom list
        self.operationFrame = Frame(self.master, bd=15)
        self.operationFrame.pack(side="right", fill='y')

        # Button list Name 
        self.operation_title = Label(self.operationFrame, bd=5, bg="white", fg="red", text="Image Operations")
        self.operation_title.pack(side='top', fill='x')

        # A Button for loading image via choosing specific directory
        self.import_image = Button(self.operationFrame, bd=5, text="Import Image", command=self.__import_image_func)
        self.import_image.pack(side='top', fill='x')

        # A Button for loading image via choosing specific directory
        self.delete_image = Button(self.operationFrame, bd=5, text="Delete Image", command=self.__delete_image_func)
        self.delete_image.pack(side='top', fill='x')

        self.show_image_main = Button(self.operationFrame, bd=5, text="Show Image (opencv)", command=self.__show_image_opencv_func)
        self.show_image_main.pack(side='top', fill='x')

         # A Button for image skew correction
        self.apply_auto_skew_correction_buttion = Button(self.operationFrame, bd=5 ,text="Auto Skew Correction",
        command=self.__apply_auto_skew_correction_func)
        self.apply_auto_skew_correction_buttion.pack(side='top', fill='x')

        # A Button for gray image thresholding
        self.apply_thresh = Button(self.operationFrame, bd=5, text="Thresholding", command=self.__apply_thresh_func)
        self.apply_thresh.pack(side='top', fill='x')

        # A Button for image erosion 
        self.apply_erode = Button(self.operationFrame, bd=5, text="Erosion", command=self.__apply_erode_func)
        self.apply_erode.pack(side='top', fill='x')

        # A Button for image dilation
        self.apply_dilate = Button(self.operationFrame, bd=5, text="Delation", command=self.__apply_dilate_func)
        self.apply_dilate.pack(side='top', fill='x')

        # A Button for image closing
        self.apply_close = Button(self.operationFrame, bd=5, text="Closing", command=self.__apply_close_func)
        self.apply_close.pack(side='top', fill='x')

        # A Button for image opening
        self.apply_open = Button(self.operationFrame, bd=5, text="Opening", command=self.__apply_open_func)
        self.apply_open.pack(side='top', fill='x')

        # A Button for image sharpening
        self.apply_sharpen = Button(self.operationFrame, bd=5, text="Sharpening", command=self.__apply_sharpen_func)
        self.apply_sharpen.pack(side='top', fill='x')

        # A Button for image blurring
        self.apply_blur = Button(self.operationFrame, bd=5, text="Bluring", command=self.__apply_blur_func)
        self.apply_blur.pack(side='top', fill='x')

        # A Button for image cropping
        self.apply_crop = Button(self.operationFrame, bd=5, text="Crop Image", command=self.__apply_crop_func)
        self.apply_crop.pack(side='top', fill='x')

        # A Button for image to text conversion
        self.apply_crop = Button(self.operationFrame, bd=5, text="Image To Text", command=self.__apply_image2text_func)
        self.apply_crop.pack(side='top', fill='x')


    def image_listbox_frame(self):

        self.imagelistboxFrame = Frame(self.master)
        self.imagelistboxFrame.pack(side='top')

        self.imagelist_scrollbar = Scrollbar(self.imagelistboxFrame)
        self.imagelist_scrollbar.pack(side="right", fill = 'y')

        self.imagelist = Listbox(self.imagelistboxFrame, width=60, yscrollcommand = self.imagelist_scrollbar.set , selectmode=tk.SINGLE)
        self.imagelist.pack(side='left', fill='both')    
        
        self.imagelist_scrollbar.config( command = self.imagelist.yview )
    def show_message_frame(self):

        self.messageFrame = Frame(self.master)
        self.messageFrame.pack(side='top', fill='y')

        self.description = Text(self.messageFrame, width=50)
        self.description.pack(side = 'left', fill='both')

        self.description_scrollbar = Scrollbar(self.messageFrame)
        self.description_scrollbar.pack( side = 'right' , fill='y')
        self.description["yscrollcommand"] = self.description_scrollbar.set
        self.description_scrollbar.config(command = self.description.yview)

    def show_image(self):

        if self.imagelist.curselection() :
            image = Image.fromarray(self.image[self.imagelist.get(tk.ACTIVE)])
            maxsize = (500, 500)
            image.thumbnail( maxsize, Image.ANTIALIAS)
            ref_image = ImageTk.PhotoImage(image)

            self.image_label["image"] = ref_image
            self.image_label.image = ref_image

        else:
            messagebox.showwarning("Simple OCR", "First You should select an image from image list box")

    def image_listbox(self, choice=1):

        if self.imagelist.size() > 0:
            self.imagelist.delete(0, self.imagelist.size())
        
        for key in self.image:
            pos = 0
            self.imagelist.insert(pos, key)
            pos += 1
            final_key = key
        
        if choice == 1:
            try:
                messagebox.showinfo("Simple OCR", f"{final_key} loaded successfully!")
                self.show_message(f"{final_key} added to image list\n")
                self.show_message("-----------------------------\n")
            except:
                pass

        
    