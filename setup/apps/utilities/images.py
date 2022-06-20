from PIL import Image
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django.db.models.signals import pre_save

import io


def resize_image(image_file, new_width):
    transposed = False
    width, height = image_file.size
    if width < height:
        image_file = image_file.transpose(Image.ROTATE_90)
        width, height = image_file.size
        transposed = True

    if width < new_width:
        resized_image = image_file
    else:
        width_percent = (new_width / float(width))
        new_height = int((float(height) * float(width_percent)))
        new_image_size = (new_width, new_height)
        resized_image = image_file.resize(new_image_size, Image.NEAREST)

    if transposed:
        resized_image = resized_image.transpose(Image.ROTATE_270)

    resized_image = resized_image.convert('RGBA')

    new_RGB_image = Image.new("RGB", resized_image.size, (255, 255, 255))
    alpha = resized_image.split()[3]
    new_RGB_image.paste(resized_image, mask=alpha)
    return new_RGB_image


def resize_image_as_bytes_io(image_file, new_width):
    with io.BytesIO() as output:
        image = resize_image(image_file, new_width)
        image.save(output, format="JPEG", quality=80)
        file_name = get_random_string(length=33)
        return ContentFile(output.getvalue(), f"{file_name}.jpg")


def resize_image_field(image_field, new_width):
    try:
        image_file = Image.open(image_field)
    except FileNotFoundError:
        return None
    return resize_image_as_bytes_io(image_file, new_width)


def add_resize_image_signal(model_class, width_list=[300, ], image_field_name="image", ):
    print(f"*****************\n\nadd_resize_image_signal\n\n*****************")

    def resize_signal(sender, instance, **kwargs):
        print(f"***********\n\ninstance: {instance}")
        image = getattr(instance, image_field_name, None)
        print(f"\n\nimage: {image}")
        if image:
            try:
                image_file = Image.open(image)
            except FileNotFoundError:
                return None

            print(f"\n\nimage_file: {image_file}\n\n**********")
            for width in width_list:
                resized_image = resize_image_as_bytes_io(image_file, width)
                setattr(instance, f"image_{width}", resized_image)

    print(f"*****************\n\nDone {width_list}\n\n*****************")
    pre_save.connect(resize_signal, sender=model_class)
