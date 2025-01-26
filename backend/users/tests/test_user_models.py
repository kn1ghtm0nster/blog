import pytest
from blog.models import BlogPost, Comment


@pytest.mark.django_db
class TestUserModel:
    def test_create_regular_user(self, create_user):
        """
        Test that a regular user can be created successfully.
        """
        user = create_user(
            username='john_doe',
            email='john@example.com',
            password='securepassword123!'
        )
        assert user.username == 'john_doe'
        assert user.email == 'john@example.com'
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_admin_user(self, create_admin_user):
        """
        Test that an admin user can be created.
        """
        admin_user = create_admin_user(
            username='admin_jane',
            email='jane_admin@example.com',
            password='adminPass123!'
        )
        assert admin_user.username == 'admin_jane'
        assert admin_user.email == 'jane_admin@example.com'
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True

    def test_blogposts_cascade_delete(self, create_user):
        """
        Test that blog posts are deleted when a user is deleted.
        """
        user = create_user(
            username='cascade_user',
            email='cascade@example.com',
            password='cascadePass123!'
        )
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='Content here',
            author=user
        )

        # Ensure the blog post was created
        assert BlogPost.objects.filter(id=blog_post.id).exists()

        # Delete the user
        user.delete()

        # Ensure the blog post was ALSO deleted
        assert not BlogPost.objects.filter(id=blog_post.id).exists()

    def test_comments_cascade_delete(self, create_user):
        """
        Test that comments are deleted when a user is deleted.
        """
        user = create_user(
            username='comment_user',
            email='comment@example.com',
            password='commentPass123!'
        )
        blog_post = BlogPost.objects.create(
            title='Another Blog Post',
            content='Even more content',
            author=user
        )
        comment = Comment.objects.create(
            blog_post=blog_post,
            author=user,
            content='Nice post!'
        )

        # Ensure the comment exists
        assert Comment.objects.filter(id=comment.id).exists()

        # Delete the user
        user.delete()

        # Ensure the comment was ALSO deleted
        assert not Comment.objects.filter(id=comment.id).exists()

    def test_string_representation(self, create_user):
        """
        Test the string representation of the User model.
        """
        user = create_user(
            username='string_user',
            email='string@example.com',
            password='stringPass123!'
        )
        assert str(user) == 'string_user'
