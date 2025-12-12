from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from databaseApp.models import Post, Comment, Message, Profile
from databaseApp.views import dashboard, comment, messages
from django.db.models import Q


class LogicTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="john", password="password123")
        self.other_user = User.objects.create_user(username="kate", password="pass321")

        # Create a post with correct fields
        self.post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            author=self.user
        )

        # Create a comment with correct fields
        self.comment = Comment.objects.create(
            post=self.post,
            name=self.user,
            body="Test comment"
        )

        self.profile=Profile.objects.create(
            user=self.user,
        )

    def test_dashboard_delete_post_logic(self):
        req = self.factory.post(reverse("dashboard"), {
            "post-id": self.post.id,
        })
        req.user = self.user

        dashboard(req)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_dashboard_delete_comment_logic(self):
        req = self.factory.post(reverse("dashboard"), {
            "comment-id": self.comment.id,
        })
        req.user = self.user

        dashboard(req)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_comment_view_assigns_correct_user_and_post(self):
        req = self.factory.post(
            reverse("comment", kwargs={"pk": self.post.id}),
            {"body": "Another comment"}
        )
        req.user = self.user

        comment(req, pk=self.post.id)

        saved = Comment.objects.last()
        self.assertEqual(saved.name, self.user)
        self.assertEqual(saved.post, self.post)



