import cv2
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from Detektorer.Detektor_service.Detektor_service import Detektor_service

_DS = Detektor_service()

class Lys_Detektor():

    _LysNivå_Grense_Fult_bilde = 45
    # Last modellen
    model = fasterrcnn_resnet50_fpn(weights='COCO_V1')
    model.eval()


    def sjekk_lys_Hele_Bildet(image_path):
        # Last inn bildet
        image = cv2.imread(image_path)
        image_height, image_width = image.shape[:2]
        brightness_values = image

        # Beregn gjennomsnittet av lysverdiene
        brightness = brightness_values.mean()
        return brightness

    def Lavt_Lysnivå_allesider_dekk(self,image_path):
        """
        This function convolves a grayscale image with
        a Laplacian kernel and calculates its variance.
        """
        bgr_image = cv2.imread(image_path)
        
        image_height, image_width = bgr_image.shape[:2]
        imgae_size = image_height*image_width
        # Klipp bildet fra sentrum av x-aksen
        overst = _DS.crop_image_from_center(bgr_image, int(image_width * 0.4), int(image_height*0.070), -int(image_width * 0.20), -int(image_height*0.4))
        nederst = _DS.crop_image_from_center(bgr_image,int(image_width * 0.33), int(image_height*0.07), -int(image_width * 0.09), int(image_height*0.44)) 
        hoyre = _DS.crop_image_from_center(bgr_image,int(image_width * 0.07), int(image_height*0.33), int(image_width * 0.33), int(image_height*0.1))
        
        ov= overst.mean()
        nv = nederst.mean()
        hv= hoyre.mean()
        return (ov+nv+hv)/3
        if(overst.mean()>nederst.mean() and overst.mean()>hoyre.mean()):
            return overst.mean()
        if(nederst.mean()>overst.mean() and nederst.mean() > hoyre.mean()):
            return nederst.mean()
        return hoyre.mean()
        
    
    def Lysnivå_for_lav(self,image_path):
        return self.Lavt_Lysnivå_allesider_dekk(image_path)< self._LysNivå_Grense_Fult_bilde
