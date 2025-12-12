from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from databaseApp.models import Post, Comment, Message


class SystemTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="john", password="password123")

    def test_full_user_flow(self):
        # Register a new user
        response = self.client.post(reverse("register"), {
            "username": "alice",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertEqual(response.status_code, 200)


        login = self.client.post(reverse("login"), {
            "username": "john",
            "password": "password123",
        })
        self.assertEqual(login.status_code, 302)


        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)


        create = self.client.post(reverse("create_post"), {
            "title": "My Post",
            "description": "This is a test post."
        })
        self.assertEqual(create.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.first()


        comment_resp = self.client.post(
            reverse("comment", kwargs={"pk": post.id}),
            {"body": "Nice post!"}
        )
        self.assertEqual(comment_resp.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)


        delete_resp = self.client.post(reverse("dashboard"), {
            "post-id": post.id
        })
        self.assertEqual(delete_resp.status_code, 200)
        self.assertEqual(Post.objects.count(), 0)

    def test_message_flow(self):
        other = User.objects.create_user(username="kate", password="pass321")

        self.client.login(username="john", password="password123")

        send = self.client.post(reverse("messages", kwargs={"pk": other.id}), {
            "msg-txt": "Hello Kate!"
        })

        self.assertEqual(send.status_code, 302)
        self.assertEqual(Message.objects.count(), 1)
