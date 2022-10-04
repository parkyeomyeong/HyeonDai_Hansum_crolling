from PIL import Image


def save_prod_detail_image(element, img_out_path):
    Image.MAX_IMAGE_PIXELS = None
    location = element.location
    size = element.size

    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h

    im = Image.open(img_out_path)
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(img_out_path)
