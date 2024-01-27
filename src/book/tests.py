import os

from django.core.files.uploadedfile import SimpleUploadedFile

from core.settings import MEDIA_ROOT
from rest_framework.test import APITestCase
from account.models.account import User
from .models.book import (
    Book, 
    Genre, 
    Language,
    Condition,
    BookRequestStatus,
    AvailabilityStatus,
)


class Test(APITestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.user = User.objects.create(
            username='username1', 
            phone_number='998901234567',
            email='user@email.com',
            first_name='First',
            last_name='Last',
            telegram_username='telegram_user_1',
            telegram_user_id='770000001',
            password='secretpassword',
        )
        
        cls.book1 = Book.objects.create(
            title='Book1',
            author='Author1',
            genre='Fiction',
            description='Description1',
            cover_photo='',
            telegram_photo_id='some_telegram_photo_id_1',
            code='0001',
            shared_by=cls.user,
            edition='1st',
            condition='Like New',
            language='UZ',
            status='Available'  
        )
        
        cls.book2 = Book.objects.create(
            title='Book2',
            author='Author2',
            genre='Non-Fiction',
            description='Description2',
            cover_photo='',
            telegram_photo_id='some_telegram_photo_id_2',
            code='0002',
            shared_by=cls.user,
            edition='2nd',
            condition='NEW',
            language='RU',
            status='Rejected'
        )
        
        cls.post_data = {
            'title': 'Book3', 
            'author': 'Author3', 
            'genre': 'Sci-Fi', 
            'description': 'Description3',
            'cover_photo': SimpleUploadedFile('image.jpg', b'file_content', content_type='image'),
            'telegram_photo_id': 'some_telegram_photo_id_3', 
            'code': '0003',
            'shared_by': {
                'username':'username3', 
                'phone_number':'998901234567',
                'email': 'user@email.com',
                'first_name':'First',
                'last_name': 'Last',
                'telegram_username':'telegram_user_2',
                'telegram_user_id': '770000003',
                'is_admin': True,
                'password': 'supersecretpassword'
                }, 
            'edition': '3rd', 
            'condition': 'New', 
            'language': 'EN', 
            'status': 'Available'
            }
        
        cls.create_read_url = f'/api/v1/books/books/'
        cls.read_update_delete_url = f'/api/v1/books/books/{cls.book1.id}/'

    def setUp(self) -> None:
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        response = self.client.get('/api/v1/books/books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_detail(self):
        response = self.client.get(self.read_update_delete_url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(self.create_read_url, self.post_data, format='json')
        self.assertEqual(response.status_code, 201)
    
    # def test_create_required_fields(self):
    #     response = self.client.post(self.create_read_url, {}, format='json')
    #     content = {}
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json(), content)

    # def test_update(self):
    #     content = {}
    #     response = self.client.put(self.read_update_delete_url, content, format='json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), content)

    # def test_delete(self):
    #     response = self.client.delete(self.read_update_delete_url)
    #     self.assertEqual(response.status_code, 204)
    #     self.assertEqual(response.objects.count(), 1)

    @classmethod
    def tearDownClass(cls):
        super(Test, cls).tearDownClass()
        files = []
        for file in files:
            file_path = os.path.join(MEDIA_ROOT, file)
            if os.path.exists(file_path):
                os.remove(file_path)
