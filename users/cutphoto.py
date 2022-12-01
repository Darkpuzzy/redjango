from PIL import Image


def crop_center(pil_imgs):
    print('Error HERE in function crop_center')
    """
    Функция для обрезки изображения по центру.
    """
    print(dir(pil_imgs))
    pil_img = pil_imgs
    print(dir(pil_img))
    print(pil_img.seek)
    img_width, img_height = pil_img.size
    print(img_width, img_height)
    new_image = pil_img.crop(((img_width - 200) // 2,
                              (img_height - 200) // 2,
                              (img_width + 200) // 2,
                              (img_height + 200) // 2))
    return new_image
