import os

from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Skip resizing when the file is missing (fresh checkout/tests) or is the shared default
        # image, which must not be rewritten in place.
        if (
            not self.image
            or self.image.name == self._meta.get_field("image").default
            or not os.path.exists(self.image.path)
        ):
            return

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
