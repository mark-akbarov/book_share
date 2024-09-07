import os

from django.core.files.uploadedfile import SimpleUploadedFile

from core.settings import MEDIA_ROOT
from rest_framework.test import APITestCase
from apps.account.models.account import User
from apps.book.models.book import (
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
            genre=Genre.FICTION,
            description='Description1',
            cover_photo=SimpleUploadedFile('image.jpg', b'file_content', content_type='image'),
            telegram_photo_id='some_telegram_photo_id_1',
            code='0001',
            shared_by=cls.user,
            edition='1st',
            condition=Condition.GOOD,
            language=Language.RUSSIAN,
            status=AvailabilityStatus.TAKEN
        )
        
        cls.book2 = Book.objects.create(
            title='Book2',
            author='Author2',
            genre=Genre.PROGRAMMING.value,
            description='Description2',
            cover_photo=SimpleUploadedFile('image.jpg', b'file_content', content_type='image'),
            telegram_photo_id='some_telegram_photo_id_2',
            code='0002',
            shared_by=cls.user,
            edition='2nd',
            condition=Condition.GOOD.value,
            language=Language.RUSSIAN.value,
            status=AvailabilityStatus.AVAILABLE.value
        )
        
        cls.post_data = {
            'title': 'Book3', 
            'author': 'Author3', 
            'genre': Genre.HISTORY.value, 
            'description': 'Description3',
            'cover_photo': SimpleUploadedFile('image.jpg', b'file_content', content_type='image'),
            'telegram_photo_id': 
                'AgACAgIAAxkBAAId0GWFz38QapaHL7gWJL5sM3qPEm-IAAKj1TEboKkxSKyRW1W9vrvsAQADAgADbQADMwQ', 
            'code': '0003',
            'shared_by': 1,
            'edition': '3rd',
            'condition': Condition.LIKE_NEW.value,
            'language': Language.ENGLISH.value,
            'status': AvailabilityStatus.AVAILABLE.value
            }
        
        cls.update_data = {
            'id': 1,
            'title': 'Book4', 
            'author': 'Author4', 
            'genre': Genre.FANTASY.value, 
            'description': 'Description3',
            'cover_photo': SimpleUploadedFile('image1.jpg', b'file_content', content_type='image'),
            'telegram_photo_id': 
                'AgACAgIAAxkBAAId0GWFz38QapaHL7gWJL5sM3qPEm-IAAKj1TEboKkxSKyRW1W9vrvsAQADAgADbQADMwQ', 
            'code': '0003',
            'shared_by': 1, 
            'edition': '3rd', 
            'condition': Condition.LIKE_NEW.value, 
            'language': Language.RUSSIAN.value, 
            'status': AvailabilityStatus.AVAILABLE.value
        }
        
        cls.create_read_url = f'/api/v1/books/books/'
        cls.read_update_delete_url = f'/api/v1/books/books/{cls.book1.id}/'

    def setUp(self) -> None:
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        response = self.client.get(self.create_read_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_detail(self):
        response = self.client.get(self.read_update_delete_url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(self.create_read_url, self.post_data, format='multipart')
        self.assertEqual(response.status_code, 201)

    def test_update(self):
        response = self.client.put(self.read_update_delete_url, self.update_data, format='multipart')
        book1 = Book.objects.get(id=1)
        self.assertEqual(book1.title, self.update_data['title'])
        self.assertEqual(response.json()['cover_photo'].split('/')[-1], self.update_data['cover_photo'].name)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.delete(self.read_update_delete_url)
        self.assertEqual(response.status_code, 204)

    @classmethod
    def tearDownClass(cls):
        super(Test, cls).tearDownClass()
        files = ['image1.jpg', 'image.jpg']
        for file in files:
            file_path = os.path.join(MEDIA_ROOT, file)
            if os.path.exists(file_path):
                os.remove(file_path)
