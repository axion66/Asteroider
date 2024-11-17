
from PIL import ImageEnhance

def transform(image):
  '''
    Add Contrast & Sharpness
    make sure to scale to 1024x1024
  '''
  sharp = ImageEnhance.Sharpness(image)
  img = sharp.enhance(6)
  contrast = ImageEnhance.Contrast(img)
  img = contrast.enhance(6)
  return img

