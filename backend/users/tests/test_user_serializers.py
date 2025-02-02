import pytest
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from blog.models import BlogPost, Comment
from backend.users.serializers import UserSerializer, UserUpdateSerializer


@pytest.mark.django_db
class TestUserSerializer:
    """
    Test suite for read-only UserSerializer.
    """

    def test_user_serializer_output(self, create_user):
        """
        Ensure serializer works as expected and includes
        the correct fields.
        """
        user = create_user(username='serialization_user',
                           email='serializer@example.com')

        # Create related blog post and comment to confirm fields are read-only
        blog_post = BlogPost.objects.create(
            title='User Post', content='Post content', author=user)
        comment = Comment.objects.create(
            blog_post=blog_post, author=user, content='Nice post!')

        serializer = UserSerializer(instance=user)
        data = serializer.data

        assert data['id'] == user.id
        assert data['username'] == user.username
        assert data['email'] == user.email

        # Ensure read-only fields are a list of IDs of related objects
        assert len(data['blog_posts']) == 1
        assert data['blog_posts'][0] == blog_post.id
        assert len(data['comments']) == 1
        assert data['comments'][0] == comment.id


@pytest.mark.django_db
class TestUserUpdateSerializer:
    """
    Test sutie for UpdateUserSerializer, which handles
    partial user updates and password changes
    """

    def test_updating_username_and_email(self, create_user):
        """
        Ensure username and email fields can be updated
        as expected
        """
        user = create_user(username='original_user',
                           email='original@example.com')
        serializer = UserUpdateSerializer(instance=user, data={
            'username': 'updated_user',
            'email': 'updated@example.com'
        }, partial=True)

        assert serializer.is_valid(), serializer.errors
        updated_user = serializer.save()

        assert updated_user.username == 'updated_user'
        assert updated_user.email == 'updated@example.com'

    def test_password_update_success(self, create_user):
        """
        Ensure that a valid password update is applied and hashed.
        """
        user = create_user(username='password_user',
                           password='OriginalPass1234!')
        serializer_data = {
            'password': 'NewPass123!',
            'password2': 'NewPass123!'
        }
        serializer = UserUpdateSerializer(
            instance=user, data=serializer_data, partial=True)
        assert serializer.is_valid(), serializer.errors
        updated_user = serializer.save()

        assert updated_user.check_password('NewPass123!') is True

    def test_password_mismatch(self, create_user):
        """
        Ensure that an error is raised when password and password2
        don't match.
        """
        user = create_user(username='pwd_mismatch_user')
        serializer_data = {
            'password': 'NewPass123!',
            'password2': 'MismatchPass321!'
        }
        serializer = UserUpdateSerializer(
            instance=user, data=serializer_data, partial=True)

        assert not serializer.is_valid()
        assert 'password' in serializer.errors
        assert 'Passwords do not match.' in serializer.errors['password']

    def test_no_same_password(self, create_user):
        """
        Ensure tht users cannot reuse their old password as 
        the new one
        """
        user = create_user(username='reuse_pwd_user', password='ReusePass123!')
        serializer_data = {
            'password': 'ReusePass123!',
            'password2': 'ReusePass123!'
        }
        serializer = UserUpdateSerializer(
            instance=user, data=serializer_data, partial=True)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors
        assert 'New password cannot be the same as the old password.' in serializer.errors[
            'password']

    def test_non_admin_cannot_set_admin(self, create_user):
        """
        A regular user should NOT be able to update their own
        admin status
        """
        user = create_user(username='regular_user')
        serializer_data = {
            'admin': True
        }
        serializer = UserUpdateSerializer(
            instance=user, data=serializer_data, partial=True)

        assert serializer.is_valid(), serializer.errors

        # No request in context OR user is not admin => SHOULD fail
        with pytest.raises(ValidationError) as exc_info:
            serializer.save()

        assert 'You do not have permission to modify the admin field.' in str(
            exc_info.value)

    def test_admin_can_set_admin(self, create_admin_user):
        """
        An admin user should be able to set another user's
        admin status.
        """
        admin_user = create_admin_user(username='admin_user')
        user = User.objects.create_user(
            username='target_user', email='target@example.com', password='targetPass123!')
        request_context = {
            'request': type('Request', (), {'user': admin_user})
        }
        serializer_data = {
            'admin': True
        }
        serializer = UserUpdateSerializer(
            instance=user, data=serializer_data, context=request_context, partial=True)
        assert serializer.is_valid(), serializer.errors
        updated_user = serializer.save()

        assert updated_user.is_staff is True
        assert updated_user.is_superuser is True
