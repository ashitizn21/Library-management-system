'''
   Test view is tests view logic of auser app
   '''
from django.test import TestCase
from django.urls import reverse_lazy
from auser.views import Author

class TestAuthorView(TestCase):

    @classmethod
    def setUpTestData(self):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            if len(str(author_id)) > 1:
                t = author_id
            else:
                t = str(0) + str(author_id)    
            Author.objects.create(
                username=f'sinper_{author_id}',
                email=f'sinper{author_id}@gmail.com',
                first_name=f'Ashenafi_{author_id}',
                phone_number=f'09{t}122323',
            )
        
    
    def test_author_list_view(self):
        '''  '''
        response = self.client.get('/author/')
        self.assertEqual(response.status_code, 200)

    def test_author_add_by_reverse_name(self):
        response = self.client.get(reverse_lazy("auser:author_add"))
        self.assertEqual(response.status_code, 200)

    def test_author_author_list_by_reverse_name(self):
        response = self.client.get(reverse_lazy("auser:authors_list"))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_10(self):
        response = self.client.get(reverse_lazy("auser:authors_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['authors']), 10)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse_lazy('auser:authors_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['authors']), 3)