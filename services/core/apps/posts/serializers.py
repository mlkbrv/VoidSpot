from rest_framework import serializers
from .models import Post,Tweet,Media
import magic

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            "id",
            "file",
            "uploaded_at",
        ]

    def validate_file(self, value):
        allowed_mime_types = ["image/jpeg", "image/png", "video/mp4", "image/webp"]
        file_sample = value.read(2048)
        mime = magic.from_buffer(file_sample, mime=True)
        value.seek(0)
        if mime not in allowed_mime_types:
            raise serializers.ValidationError(f"Invalid file type: {mime}")
        if value.size > 100 * 1024 * 1024:
            raise serializers.ValidationError("File too large (max 100MB)")
        return value

class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(read_only=True,many=True)
    media_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Media.objects.all(),
        source="media",
        required=False
    )
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "media",
            "media_ids",
            "created_at",
        ]

class TweetSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Tweet
        fields = ["id", "content", "author", "created_at"]
