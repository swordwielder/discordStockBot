import requests


def imageSaver(imageurl):
    img_data = requests.get(imageurl).content
    with open(f'content_detection/imagebank/downloaded_image.jpg', 'wb') as handler:
        handler.write(img_data)
