import json
import base64



#json 文件 a.json 转换 image b.jpg/bmp
def jsonfile_to_imagedata(JSON_NAME,IMAGE_NAME):
    # 读取 json 文件，并直接存入字典
    with open(JSON_NAME, "r") as json_file:
        raw_data = json.load(json_file)
        # 从字典中取得图片的 base64 字符串，形如“YABgAAD/2wBDAAYEBQYFBAY...."，
        image_base64_string = raw_data["image_base64_string"]
        # 将 base64 字符串解码成图片字节码
        image_data = base64.b64decode(image_base64_string)
        # 将字节码以二进制形式存入图片文件中，注意 'wb'
    with open(IMAGE_NAME, 'wb') as img_file:
        img_file.write(image_data)

def json_to_image(jsoninfo,image_file):
    pass
    # info_json=request.form.get("info_json")
    # imgs_info=json.loads(info_json)