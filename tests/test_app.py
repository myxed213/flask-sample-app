import unittest
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, routes

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        routes.items.clear()  # Clear the in-memory item list before each test

    def test_hello_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("<title>Flask CRUD Demo</title>", response.data.decode('utf-8'))

    def test_add_item_route(self):
        response = self.client.post('/items', json={"name": "item1"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['message'], 'Item added successfully')
        self.assertEqual(response.get_json()['item'], {'id': 0, 'name': 'item1', 'price': 0.0})

    def test_get_item_route(self):
        self.client.post('/items', json={"name": "item1"})
        response = self.client.get('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'item': {'id': 0, 'name': 'item1', 'price': 0.0}})

    def test_get_nonexistent_item_route(self):
        response = self.client.get('/items/99')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

    def test_update_item_route(self):
        self.client.post('/items', json={"name": "old name"})
        response = self.client.put('/items/0', json={"name": "new name"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['item'], {"id": 0, "name": "new name", "price": 0.0})

    def test_update_nonexistent_item_route(self):
        response = self.client.put('/items/5', json={"name": "fail"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

    def test_delete_item_route(self):
        self.client.post('/items', json={"name": "to be deleted"})
        response = self.client.delete('/items/0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Item deleted successfully')
        self.assertEqual(response.get_json()['item'], {'id': 0, 'name': 'to be deleted', 'price': 0.0})

    def test_delete_nonexistent_item_route(self):
        response = self.client.delete('/items/100')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Item not found'})

if __name__ == '__main__':
    unittest.main()
