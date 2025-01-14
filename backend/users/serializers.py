from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    blog_posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'blog_posts', 'comments']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information.
    Handles updating username, email, password, and admin status.
    """
    email = serializers.EmailField(
        required=False,  # for partial updates
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=False,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=False
    )
    admin = serializers.BooleanField(required=False)

    class Meta:
        model = User
        # fields that can be updated
        fields = ['username', 'email', 'password', 'password2', 'admin']
        # Make username and email optional for partial updates.
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
        }

    def validate(self, attrs):
        """
        Validates that both password and password2 are provided and that they match.
        """
        if 'password' in attrs or 'password2' in attrs:
            if attrs.get('password') != attrs.get('password2'):
                raise serializers.ValidationError(
                    {'password': 'Passwords do not match.'})
            user = self.instance
            if user and user.check_password(attrs.get('password')):
                raise serializers.ValidationError(
                    {'password': 'New password cannot be the same as the old password.'})
        return attrs

    def update(self, instance, validated_data):
        """
        Updates the user instance with validated data.
        Handles password and admin status updates.
        """
        # Extract admin status if present
        admin_status = validated_data.pop('admin', None)
        password = validated_data.pop('password', None)
        # remove password2 since it's only for validation
        validated_data.pop('password2', None)

        # Update username and email if provided
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle password update
        if password:
            instance.set_password(password)

        # Handle admin status update
        if admin_status is not None:
            instance.is_staff = admin_status
            instance.is_superuser = admin_status

        instance.save()
        return instance
