from imageai.Detection import ObjectDetection
from os.path import isfile, join
import os



def imganalyze(pathtoimages):
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(os.getcwd()+'/content_detection', "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()
    ######
    path = f'{os.getcwd()}/content_detection/imagebank/'


    detections = detector.detectObjectsFromImage(input_image=os.path.join(path, 'downloaded_image.jpg'), output_image_path=os.path.join(path , 'Analysedimage.jpg'))

    for eachObject in detections:
        print(eachObject["name"] , " : " , eachObject["percentage_probability"] )

