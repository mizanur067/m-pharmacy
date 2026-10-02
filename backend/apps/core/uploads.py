import uuid
from pathlib import PurePosixPath
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from django.conf import settings
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
PRESCRIPTION_TYPES = {"image/jpeg", "image/png", "application/pdf"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_PRESCRIPTION_SIZE = 10 * 1024 * 1024


class PresignUploadSerializer(serializers.Serializer):
    content_type = serializers.CharField()
    size = serializers.IntegerField(min_value=1)
    kind = serializers.ChoiceField(choices=("image", "prescription"))

    def validate(self, attrs):
        allowed = IMAGE_TYPES if attrs["kind"] == "image" else PRESCRIPTION_TYPES
        maximum = MAX_IMAGE_SIZE if attrs["kind"] == "image" else MAX_PRESCRIPTION_SIZE
        if attrs["content_type"] not in allowed:
            raise serializers.ValidationError({"content_type": "This file type is not supported."})
        if attrs["size"] > maximum:
            raise serializers.ValidationError({"size": f"File must be no larger than {maximum // (1024 * 1024)} MB."})
        return attrs


class PresignUploadView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PresignUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kind = serializer.validated_data["kind"]
        extension = serializer.validated_data["content_type"].split("/")[-1].replace("jpeg", "jpg")
        prefix = "prescriptions" if kind == "prescription" else "medicines"
        key = str(PurePosixPath(prefix) / str(request.user.id) / f"{uuid.uuid4()}.{extension}")
        client = boto3.client(
            "s3",
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL or None,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID or None,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY or None,
        )
        try:
            result = client.generate_presigned_post(
                Bucket=settings.AWS_PRIVATE_BUCKET_NAME if kind == "prescription" else settings.AWS_STORAGE_BUCKET_NAME,
                Key=key,
                Fields={"Content-Type": serializer.validated_data["content_type"]},
                Conditions=[
                    {"Content-Type": serializer.validated_data["content_type"]},
                    ["content-length-range", 1, serializer.validated_data["size"]],
                ],
                ExpiresIn=300,
            )
        except (BotoCoreError, ClientError) as exc:
            raise serializers.ValidationError({"storage": "Unable to create upload URL."}) from exc
        return Response({"key": key, "upload": result}, status=status.HTTP_200_OK)
