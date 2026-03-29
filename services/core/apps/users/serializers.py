from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'phone_number',
            'profile_photo',
            'background_photo'
        ]
        read_only_fields = [
            'id',
            'email',
            'full_name',
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True,required=True)
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "phone_number",
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

class UserUpdateSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=False)
    background_photo = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'profile_photo',
            'background_photo',
        ]

class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
            'groups': {'read_only': True},
            'user_permissions': {'read_only': True},
        }