from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import WasteCategory, WasteReport, UserProfile


class AppSmokeTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		# Create categories expected by the app
		categories = [
			'biodegradable', 'plastic', 'ewaste', 'metal', 'glass', 'hazardous'
		]
		for name in categories:
			WasteCategory.objects.create(
				name=name,
				icon='fa-icon',
				description=f'{name} description',
				color='#123456',
				treatment_method='test',
				environmental_impact='test',
			)

	def setUp(self):
		self.client = Client()

	def test_login_page_loads(self):
		resp = self.client.get('/')
		self.assertEqual(resp.status_code, 200)

	def test_signup_page_loads(self):
		resp = self.client.get('/signup/')
		self.assertEqual(resp.status_code, 200)

	def test_dashboard_redirects_anonymous(self):
		resp = self.client.get('/dashboard/')
		self.assertIn(resp.status_code, (301, 302))

	def test_admin_accessible(self):
		resp = self.client.get('/admin/')
		self.assertIn(resp.status_code, (200, 302))

	def test_category_page_redirects_anonymous(self):
		resp = self.client.get('/biodegradable/')
		self.assertIn(resp.status_code, (301, 302))

	def test_create_user_and_auth_flow(self):
		# Create user and profile
		user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
		UserProfile.objects.create(user=user)

		# Attempt login via POST to root as the project does in its smoke script
		resp = self.client.post('/', {'email': 'test@example.com', 'password': 'testpass123'})
		self.assertIn(resp.status_code, (200, 302))

		# Use client.login to ensure authentication backend works
		logged = self.client.login(username='testuser', password='testpass123')
		self.assertTrue(logged)

		resp2 = self.client.get('/dashboard/')
		self.assertEqual(resp2.status_code, 200)

	def test_category_count(self):
		self.assertEqual(WasteCategory.objects.count(), 6)

	def test_category_card_links(self):
		# Create user and authenticate
		user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
		UserProfile.objects.create(user=user)
		self.client.login(username='testuser', password='testpass123')

		# Get dashboard
		resp = self.client.get('/dashboard/')
		self.assertEqual(resp.status_code, 200)

		# Verify category URLs are in context
		categories = resp.context['waste_categories']
		for category in categories:
			self.assertTrue(hasattr(category, 'detail_url'), f"Category {category.name} missing detail_url")
			self.assertIn(f'/{category.name}/', category.detail_url)

	def test_category_detail_pages_accessible(self):
		# Create user and authenticate
		user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
		UserProfile.objects.create(user=user)
		self.client.login(username='testuser', password='testpass123')

		# Test all category detail pages are accessible
		categories = ['biodegradable', 'plastic', 'ewaste', 'metal', 'glass', 'hazardous']
		for category_name in categories:
			resp = self.client.get(f'/{category_name}/')
			self.assertEqual(resp.status_code, 200, f"Category detail page {category_name} not accessible")
			self.assertEqual(resp.context['category'].name, category_name)
