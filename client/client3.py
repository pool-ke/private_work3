import requests
import os
import pickle
import sys

POST_IMAGES_URL="http://127.0.0.1:8080/api/images/"
POST_IMAGE_URL="http://127.0.0.1:8080/api/image/"

def post_data(data,files,api_url=POST_IMAGES_URL):
    while True:
        r=requests.post(url=api_url,files=files,data=data,headers={'Connection':'close'})
        if r.status_code==200:
            break
    print (r.status_code)

def generate_image_id(path):
    if not os.path.isdir(path) and "." in path:
        imageName=path.split(".")[-1]
        return imageName
    elif os.path.isdir(path):
        imageNames=os.listdir(path)
        return imageNames
    else:
        return None

def upload_images(path,json_file):
    if os.path.isdir(path):
        imageIds=generate_image_id(path)
        image_buffer_dict={}
        for imageId in imageIds:
            imagePath=os.path.join(path,imageId)
            with open(imagePath,'rb') as f:
                image_buffer_dict[imageId]=f.read()
        image_buffer_str=pickle.dumps(image_buffer_dict)
        post_data(image_budder_str)
    elif os.path.isfile(path):
        imageId=generate_image_id(path)
        with open(path,'rb') as f:
            image_buffer=f.read()
        post_data(image_buffer,POST_IMAGE_URL+imageId)
    else:
        print ("param path is not normal,please check it carefully")

 if __name__=="__main__":
     print (generate_image_id)
     upload_images(xxx)    