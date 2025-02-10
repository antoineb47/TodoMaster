from django.test import TestCase
from .models import Todo
from django.contrib.auth.models import User

class TodoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.todo = Todo.objects.create(title='Test Todo', description='Test Description', user=self.user)

    def test_todo_creation(self):
        self.assertEqual(self.todo.title, 'Test Todo')
        self.assertEqual(self.todo.description, 'Test Description')
        self.assertFalse(self.todo.completed)

    def test_todo_str(self):
        self.assertEqual(str(self.todo), 'Test Todo')

class TodoViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_todo_list_view(self):
        response = self.client.get('/todos/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_list.html')

    def test_todo_create_view(self):
        response = self.client.post('/todos/create/', {'title': 'New Todo', 'description': 'New Description'})
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())
