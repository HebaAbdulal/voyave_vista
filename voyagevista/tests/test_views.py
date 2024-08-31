from django.test import TestCase, Client
from django.urls import reverse
from voyagevista.models import Post



class TestViews(TestCase):
    """
    Unit tests for views in the VoyageVista app
    """
    def setUp(self):
        """
        Create test users and posts.
        """
        self.user = User.objects.create_user(username='testuser', password='testpass')
        logged_in = self.client.login(username='testuser', password='testpass')
        self.assertTrue(logged_in, "Login failed in setUp method")
        
        self.category = Category.objects.create(name='Test Category')
        
        self.post = Post.objects.create(
            title="test title",
            slug="test-title",
            author=self.user,
            content="Content of test post",
            category=self.category,
            status=1
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        """
        Test the correct template is used for the home page.
        """
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, template_name='index.html')

    def test_posts_passed_into_template(self):
        """
        Test that the blog posts are passed into the blog template.
        """
        response = self.client.get(reverse('home'))
        posts = Post.objects.all()
        self.assertEqual(len(response.context['page_obj']), len(posts))
        self.assertQuerySetEqual(
            response.context['page_obj'],
            posts,
            transform=lambda x: x
        )
