from django.urls import path
from .uploads import PresignUploadView

urlpatterns = [path("presign/", PresignUploadView.as_view(), name="upload-presign")]
