from django.db import models
from django.utils.timezone import now

class Cookie(models.Model):
    value = models.TextField(unique=True)  # Lưu cookie (tránh trùng lặp)
    created_at = models.DateTimeField(default=now)  # Thời gian nhập

    def __str__(self):
        return f"Cookie({self.id})"

class Token(models.Model):
    value = models.TextField(unique=True)  # Lưu token
    created_at = models.DateTimeField(default=now)  # Thời gian tạo
    # source_cookie = models.ForeignKey(Cookie, on_delete=models.CASCADE)  # Liên kết với cookie gốc

    def __str__(self):
        return f"Token({self.id})"
