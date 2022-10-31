'''
    Testing auser model 
'''
import email
from django.test import TestCase
# from django.core.files.uploadedfile import SimpleUploadedFile

from auser.models import User, Author

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # image_file = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        User.objects.create(first_name="Bacha", last_name="Debla", profile_picture="uploads/profile_pictures/test_image.jpg")

    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "email address")
    
    def tes_sex_char_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("sex").max_length
        self.assertEqual(max_length, 2)

    def test_profile_picture_field(self):
        user = User.objects.get(id=1)
        target = user.profile_picture
        self.assertEqual(target, "uploads/profile_pictures/test_image.jpg")

class TestAuthorModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name="Bacha", last_name="Debla", email="test@yahoo.com", phone_number="0912121212",
                              sex="M")
    
    def test_last_name(self):
        author = Author.objects.get(id=1)
        value = author.last_name
        self.assertEqual(value, "Debla")

    def test_email(self):
        author = Author.objects.get(id=1)
        value = author.email
        self.assertEqual(value, "test@yahoo.com")
    def tes_username_max_length(self):
        author =Author.objects.get(id=1)
        max_len = author._meta.get_field("username").max_length
        self.assertEqual(max_len, 150)
    
    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), "/author/1/detail/")

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

