from django.urls import reverse
import base64
import hashlib
import hmac
import imghdr
from django.conf import settings
from django.utils.six import text_type


# This function makes it possible to expose an image url to a template.
# See http://docs.wagtail.io/en/latest/advanced_topics/images/image_serve_view.html
def generate_image_url(image, filter_spec):
    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))

    # Append image's original filename to the URL (optional)
    url += image.file.name[len('original_images/'):]

    return url


def generate_signature(image_id, filter_spec, key=None):
    """
    Copied from wagtail.wagtail.view.serve.py to avoid a "Models aren't loaded yet" error.
    """
    if key is None:
        key = settings.SECRET_KEY

    # Key must be a bytes object
    if isinstance(key, text_type):
        key = key.encode()

    # Based on libthumbor hmac generation
    # https://github.com/thumbor/libthumbor/blob/b19dc58cf84787e08c8e397ab322e86268bb4345/libthumbor/crypto.py#L50
    url = '{}/{}/'.format(image_id, filter_spec)
    return base64.urlsafe_b64encode(hmac.new(key, url.encode(), hashlib.sha1).digest())

