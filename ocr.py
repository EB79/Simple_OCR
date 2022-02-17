import cv2
import numpy as np
import pytesseract

class OCR():


    def auto_skew_correction_buttion(self, image):
        """This function is an automatic skew calculator and corrector in text images

        Args:
            image (ndarray): The input image is one channel gray image.

        Returns:
            ndarray: The output is a skew correted one channel gray image.
        """

        ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        #Calculates the minimum border that contains rotated text
        coords = np.column_stack(np.where(thresh > 0))
        #This function gives the rectangle border containing the whole text area, and the rotation angle of this border is the same as that of the text in the figure
        angle = cv2.minAreaRect(coords)[-1]

        #Adjust the angle
        if angle < -45:
            angle = -(90+ angle)
        else:
            angle = -angle

        #Affine transformation
        h, w = image.shape[:2]
        center = (w//2, h//2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        return rotated


    def threshold(self, image, threshold_model, thresh_value , block_size=3):
        """This function is threshold applier based on various methods.

        Args:
            image (ndarray): The input image is one channel gray image.
            threshold_model (str): BINARY, BINARY_INV, ADAPTIVE MEAN, ADAPTIVE GAUSSIAN, OTSU
            thresh_value (int): A threshold value from 0 to 255
            block_size (int, optional): Block size for ADAPTIVE MEAN and ADAPTIVE GAUSSIAN. Defaults to 3.

        Returns:
            ndarray: The output is a thresholded gray image.
        """

        if threshold_model == "BINARY":
            ret,image_thresh = cv2.threshold(image, thresh_value, 255, cv2.THRESH_BINARY)
        
        elif threshold_model == "BINARY_INV":
            ret,image_thresh = cv2.threshold(image, thresh_value, 255, cv2.THRESH_BINARY_INV)

        elif threshold_model == "ADAPTIVE MEAN":
            image_thresh = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, 2)
            
        elif threshold_model == "ADAPTIVE GAUSSIAN":
            image_thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, 2)
        
        elif threshold_model == "OTSU":
            ret,image_thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        return image_thresh


    def blur(self, image, blur_model ,block_size, sigma=None):
        """This function is for blurring gray images based on various methods.

        Args:
            image (ndarray): The input image is one channel gray image.
            blur_model (str): Average, gaussian, median
            block_size (int): Block size for average, gaussian, median
            sigma (type, optional): Standard deviation value for gaussian blurring. Defaults to None.

        Returns:
            ndarray: The output is a blurred gray image.
        """
        if blur_model == "average":
            # Average Blurring
            blur_image = cv2.blur(image,(block_size,block_size))
        elif blur_model == "gaussian":
            # Gaussian Blurring
            blur_image = cv2.GaussianBlur(image, (block_size,block_size), sigma) 
        elif blur_model == "median":
            # Median blurring
            blur_image = cv2.medianBlur(image,block_size)
        return blur_image


    def erode(self, image, kernel_x, kernel_y, structure="rectangle", iterations=1):
        """Morphologic filter erosion

        Args:
            image (ndarray): The input image is one channel gray image.
            kernel_x (int): Kernel size in x axis
            kernel_y (int): Kernel size in y axis
            structure (str, optional): rectangle, ellipse, cross. Defaults to "rectangle".
            iterations (int, optional): Iterations of applying chosen filter. Defaults to 1.

        Returns:
            ndarray: The output is a filterd gray image.
        """
        # Selected Structure Element
        if structure == "rectangle" :
            st = cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_x, kernel_y))
        elif structure == "ellipse":
            st = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kernel_x, kernel_y))
        elif structure == "cross":
            st = cv2.getStructuringElement(cv2.MORPH_CROSS,(kernel_x, kernel_y))

        # Image Erosion
        erosion = cv2.erode(image, st, iterations)

        return erosion


    def dilate(self, image, kernel_x, kernel_y, structure="rectangle", iterations=1):
        """[Morphologic filter delation]

        Args:
            image (ndarray): The input image is one channel gray image.
            kernel_x (int): Kernel size in x axis
            kernel_y (int): Kernel size in y axis
            structure (str, optional): rectangle, ellipse, cross. Defaults to "rectangle".
            iterations (int, optional): Iterations of applying chosen filter. Defaults to 1.

        Returns:
            ndarray: The output is a filterd gray image.
        """

        # Selected Structure Element
        if structure == "rectangle" :
            st = cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_x, kernel_y))
        elif structure == "ellipse":
            st = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kernel_x, kernel_y))
        elif structure == "cross":
            st = cv2.getStructuringElement(cv2.MORPH_CROSS,(kernel_x, kernel_y))
        
        # Image Dilation
        dilation = cv2.dilate(image, st, iterations)

        return dilation

        
    def open(self, image, kernel_x, kernel_y, structure="rectangle", iterations=1):
        """[Morphologic filter opening]

        Args:
            image [ndarray): The input image is one channel gray image.
            kernel_x (int): Kernel size in x axis
            kernel_y (int): Kernel size in y axis
            structure (str, optional): rectangle, ellipse, cross. Defaults to "rectangle".
            iterations (int, optional): Iterations of applying chosen filter. Defaults to 1.

        Returns:
            ndarray: The output is a filterd gray image.
        """
        # Selected Structure Element
        if structure == "rectangle" :
            st = cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_x, kernel_y))
        elif structure == "ellipse":
            st = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kernel_x, kernel_y))
        elif structure == "cross":
            st = cv2.getStructuringElement(cv2.MORPH_CROSS,(kernel_x, kernel_y))
        
        # Image Opening
        open_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, st)

        return open_image


    def close(self, image, kernel_x, kernel_y, structure="rectangle", iterations=1):
        """Morphologic filter closing

        Args:
            image (ndarray): [The input image is one channel gray image.
            kernel_x (int): Kernel size in x axis
            kernel_y (int): Kernel size in y axis
            structure (str, optional): rectangle, ellipse, cross. Defaults to "rectangle".
            iterations (int, optional): Iterations of applying chosen filter. Defaults to 1.

        Returns:
            ndarray: The output is a filterd gray image.
        """
        # Selected Structure Element
        if structure == "rectangle" :
            st = cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_x, kernel_y))
        elif structure == "ellipse":
            st = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kernel_x, kernel_y))
        elif structure == "cross":
            st = cv2.getStructuringElement(cv2.MORPH_CROSS,(kernel_x, kernel_y))
        
        # Image Closing
        close_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, st)

        return close_image

        
    def sharpen(self, image, sharp_model):
        """This function is for sharpening gray images based on various methods.

        Args:
            image (ndarray): The input image is one channel gray image.
            sharp_model (str): weak , strong

        Returns:
            type: The output is a sharped gray image.
        """
        if sharp_model == "weak":
            kernel = np.array([[0, -1, 0],
                            [-1, 5, -1],
                            [0, -1, 0]])
            sharp_image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)

        elif sharp_model =="strong":
            kernel = np.array([[-1, -1, -1],
                            [-1, 9, -1],
                            [-1, -1, -1]])
        
            sharp_image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
        
        return sharp_image


    def crop(self, image):
        """This function is for cropping gray images

        Args:
            image (ndarray): The input image is one channel gray image.

        Returns:
            ndarray: The output is a cropped gray image.
        """
        image_copy = image.copy()
        coordinates = []

        def draw_rectangle(event, x, y, flags, param):
            global ix, iy

            if event == cv2.EVENT_LBUTTONDOWN:
                ix = x
                iy = y
            elif event == cv2.EVENT_LBUTTONUP:
                is_drawing = False
                cv2.rectangle(img=image_copy, pt1=(ix, iy), pt2=(x, y), color=(50, 0, 0), thickness=3)
                coordinates.append([ix, iy, x, y])

        cv2.namedWindow("Crop Image")
        cv2.setMouseCallback("Crop Image", draw_rectangle)

        while True:
            cv2.imshow("Crop Image", image_copy)

            # wait 5 seconds then wait for ESC key
            if cv2.waitKey(5) & 0xFF == 27:
                break

        cv2.destroyAllWindows()
        return image[coordinates[0][0]:coordinates[0][3],coordinates[0][1]:coordinates[0][2]]


    def read_text(self, image, lang, to_txt_file=True, export_name="output"):
        """This is a fucntion for reading text from a preprocessed image

        Args:
            image (ndarray): The input image is one channel gray image.
            lang (str): chosen language to read from image
            to_txt_file (bool, optional): [Output as text file option]. Defaults to True.
            export_name (str, optional): [Output file name as string]. Defaults to "output".

        Returns:
            str: Output is the extracted text from image.
        """
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        data = pytesseract.image_to_string(image, lang)

        if to_txt_file == True:
            with open(f"{export_name}.txt", "w") as f:
                f.write(data)
            return data
        else:
            return data