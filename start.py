
from controllers.imageController  import  ImageController;

def launch():
    print('STARTED :: Launching the SmartDim app..')
    imgControllerObj = ImageController();
    imgControllerObj.readImage();
    print('END :: Launching the SmartDim app..')

launch();


