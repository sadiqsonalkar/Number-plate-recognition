#C:/Users/Sadiq/AppData/Local/Tesseract-OCR/tesseract.exe
#Step 1: Import the library We are using OpenCV and Pytesseract

#We are using opencv and pytesseract

import cv2
import pytesseract

#Step 2: Load the tesseract file 
pytesseract.pytesseract.tesseract_cmd = "C:/Users/Sadiq/AppData/Local/Tesseract-OCR/tesseract.exe"

#Step 3: Read the image
img=cv2.imread("car2.jpg")

#Step 4: Convert that image into gray
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("Original Image",img) #Will display original Image

#Step 5: Apply filter to reduce noise
'''
We are applying bilateralFilter on the gray image we got
A bilateral filter is used for smoothening images and reducing noise, while keeping the edges
'''
flter=cv2.bilateralFilter(gray,11,15,15)

#Step 6: Edge detection
'''
In open cv there is a edge detection method name canny
we will apply that on filtered image
pass lower threshold and upper threshold value
'''
edge=cv2.Canny(flter,170,200)

#Step 7: Contour Detection 
'''
It return value in 2 parts so we will take 2 variable
'''
contor,herf=cv2.findContours(edge,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#Step 8: Sort the contour according to area
'''
Now we will get many contour here. We will sort according to area of rectangle because number plate is rectangle
'''
ctn=sorted(contor,key=cv2.contourArea,reverse=True)

for c in ctn:
    #Step 9: Find perimeter of the contour
    peri=cv2.arcLength(c,True) 
    Findside=0.018*peri # This function will provide us the no. of side
    apporx=cv2.approxPolyDP(c,Findside,True) #Will return No. of Side 

    if len(apporx)==4: # If size is 4 then it is rectangle
        x,y,w,h=cv2.boundingRect(apporx) # We need x,y co-ordinate,width and height to crop the image. boundingRect will return the co-ordinates
        img2=img[y:y+h,x:x+w] #This will crop the original image into img2
        cv2.imshow("Cropped Number Plate",img2) #Will display the cropped number plate
        '''
        Now we will pass The cropped number plate image to tesseract to read the text in the image
        '''
        configr = ('-l eng --oem 1 --psm 3')

        text=pytesseract.image_to_string(img2,config=configr)#Will convert image to string
        print(text) #Will print the string
        final=cv2.drawContours(img,[apporx],-1,(255,0,0),3) #Then we will get the contour with side 4 we will draw a rectangle around it and give colour to that rectangle
        break
    
cv2.imshow("Number Plate Recognize",img) #display the image
cv2.waitKey(0) #Will take no waiting time
#Waitkey allows users to display a window for given milliseconds or until any key is pressed. If 0 is passed in the argument it waits till any key is pressed.
