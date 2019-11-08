from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse

from .forms import DocumentForm

#for image processing

import numpy as np
import time
import cv2

def show_page(request):
    return render(request, 'page3.html')

def nothing(x):
    pass

def show_bands(request):

    # Create a window and resize it
    window_name = 'image'

    cv2.namedWindow(window_name) #width, hight

    # create trackbars for color change
    cv2.createTrackbar('RL',window_name,0,255,nothing)
    cv2.createTrackbar('GL',window_name,0,255,nothing)
    cv2.createTrackbar('BL',window_name,0,255,nothing)
    cv2.createTrackbar('RU',window_name,1,255,nothing)
    cv2.createTrackbar('GU',window_name,1,255,nothing)
    cv2.createTrackbar('BU',window_name,1,255,nothing)
    
    #get image to be processed if not then show error and ask to upload image again
    try:
        filepath = request.GET.get('filepath', None)
        img = cv2.imread(filepath)
        img = cv2.resize(img,(400,500))
        
    except Exception as e:
        print(e)
        return HttpResponseRedirect('colourband/')
    
    while(cv2.getWindowProperty(window_name, 0) >= 0):
        
        # get current positions of four trackbars
        rl = cv2.getTrackbarPos('RL',window_name)
        gl = cv2.getTrackbarPos('GL',window_name)
        bl = cv2.getTrackbarPos('BL',window_name)
        ru = cv2.getTrackbarPos('RU',window_name)
        gu = cv2.getTrackbarPos('GU',window_name)
        bu = cv2.getTrackbarPos('BU',window_name)

        lowerbound = [bl,gl,rl]
        upperbound = [bu,gu,ru]

        lower = np.array(lowerbound, dtype = "uint8")
        upper = np.array(upperbound, dtype = "uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask= cv2.inRange(img,lower,upper)
        output = cv2.bitwise_and(img,img, mask=mask)
    
        # show the images
        cv2.imshow(window_name, np.hstack([img,output]))
        
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cv2.imwrite('media/output.jpg',output) # to save the image on pressing esc key
            break

    cv2.destroyWindow(window_name)

    return HttpResponse(status=200)


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']    
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
        
    return render(request, 'upload.html')