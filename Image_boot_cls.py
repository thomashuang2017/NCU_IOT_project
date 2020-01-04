import cv2 as cv
from picamera import PiCamera
from time import sleep
from imutils import paths

def image_boot_cls():

    cemra_output_path = 'save_image/target_image.png'
    #cemra_output_path = 'training_data/negative/images_0.jpg'
    model_path = 'model/boost_cls_model.pb'
    image_target_path = 'save_image'
    #image_target_path =  'training_data/negative'

    # Camera capture
    print('[INFO]Camera activate')
    with PiCamera() as camera:
        camera.resolution = (480,480)
        camera.start_preview()
        sleep(5)
        camera.capture(cemra_output_path)
        camera.stop_preview()

    # Load the model.
    print('[INFO]Model activate')
    net = cv.dnn.readNet(model_path)

    # Specify target device.
    net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)
    image = sorted(list(paths.list_images(image_target_path)))
    image = cv.imread(image[0])
    blob = cv.dnn.blobFromImage(image, size=(28, 28), ddepth=cv.CV_8U)
    net.setInput(blob)
    out = net.forward() # out = [[0,1]](power on), out = [[1,0]](power off)

    if out[0][0] == 1: # if the computer is power off (1) , else computer is power on (0)
        print('[INFO]Computer if power off')
        return 1
    else:
        print('[INFO]Computer if power on')
        return 0
    
















