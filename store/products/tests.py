from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data.get('title'), 'Store')  # Use .get() for safety
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        products = Product.objects.all()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data.get('title'), 'Store - Каталог')  # Use .get()
        self.assertTemplateUsed(response, 'products/products.html')

        expected_products = list(products[:3]) if products.exists() else []
        self.assertEqual(list(response.context_data.get('object_list', [])), expected_products)

    def test_list_empty(self):
        """Test behavior when no products exist"""
        Product.objects.all().delete()
        path = reverse('products:index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(list(response.context_data.get('object_list', [])), [])

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        self.assertIsNotNone(category, "No categories available for testing")

        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        products = Product.objects.filter(category_id=category.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data.get('title'), 'Store - Каталог')  # Use .get()
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(list(response.context_data.get('object_list', [])), list(products))

    def test_list_with_nonexistent_category(self):
        """Test behavior when a category ID is used that doesn't exist"""
        path = reverse('products:category', kwargs={'category_id': 99999})  # Unlikely ID
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(list(response.context_data.get('object_list', [])), [])
