'''
    Test views of catalog app
    '''
import uuid
from django.test import TestCase
from django.urls import reverse_lazy
import datetime
from django.utils import timezone
from django.contrib.auth.models import Permission

from catalog.models import BookInstance, Book, Genre, Language
from auser.models import User, Author

class LoanedBookInstancesByUserListViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', email="test12@yahoo.com", phone_number=+251912121212, password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD', email="test12@gmail.com", phone_number=+251912121223,)

        test_user1.save()
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
            language=test_language,
        )

        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        # for ff in genre_objects_for_book:
        #     print("34555", ff)
        test_book.genre.set(genre_objects_for_book) # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create 30 BookInstance objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.localtime() + datetime.timedelta(days=book_copy%5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = 'M'
            BookInstance.objects.create(
                book=test_book,
                imprint='Unlikely Imprint, 2016',
                due_back=return_date,
                borrower=the_borrower,
                status=status,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse_lazy('catalog:loaned_book'))
        self.assertRedirects(response, '/auth/login/?next=/catalog/book/loan_book/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('catalog:loaned_book'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']).strip(), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'catalog/loan_book/i_borrowed_list.html')

    def test_borrowed_book_list(self):
        login = self.client.login(username="testuser1", password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy("catalog:loaned_book"))

        # test our user is logged in 
        self.assertEqual(str(response.context['user']).strip(), 'testuser1')

        # check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('borrowed_books' in response.context)
        self.assertEqual(len(response.context['borrowed_books']), 0)
        
        books = BookInstance.objects.all()[:10]
        for book in books:
            book.status = "O"
            book.save()
        
        response = self.client.get(reverse_lazy("catalog:loaned_book"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']).strip(), 'testuser1')

        self.assertTrue("borrowed_books" in response.context)

        for book_item in response.context['borrowed_books']:
            # check user of is it borrower
            self.assertEqual(response.context['user'], book_item.borrower)
            # chech book_items is on loan book or not
            self.assertEqual(book_item.status, 'O')

    def test_page_order_by_due_date(self):
        # change all copies to on loan status
        book_instance = BookInstance.objects.all()
        for book in book_instance:
            book.status = "O"
            book.save()
        
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy("catalog:loaned_book"))
        self.assertEqual(str(response.context['user']).strip(), 'testuser1') # check user is logged in or not
        self.assertEqual(response.status_code, 200)
        
        # check number books it have
        self.assertEqual(len(response.context['borrowed_books']), 10)
        last_date = 0
        values = response.context['borrowed_books']
        for book in values:
            if last_date ==0 :
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back


class RenewalBookInstanceTestView(TestCase):
    """ testing view of renewal book_instance """

    def setUp(self):
        test_user1 = User.objects.create(
                    username='testuser1',
                    email="test12@yahoo.com",
                    phone_number=+251912121212,
                    password='1X<ISRUkw+tuK'   
                    )
        test_user2 = User.objects.create(
                    username='testuser2', 
                    password='2HJ1vRV0Z&3iD', 
                    email="test12@gmail.com", 
                    phone_number=+251912121223,
                    )

        test_user1.save()
        test_user2.save()

        # give permission for test_user2 to renew book
        permission = Permission.objects.get(name='Set book as returnes')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        test_author = Author.objects.create(
                        first_name="Bacha", 
                        last_name="Debla",
                        email="test@yahoo.com", 
                        phone_number="0912121212",
                        sex="M"
                    )
        
        test_genre = Genre.objects.create(name="Biblical")
        test_language = Language.objects.create(name='Amharic')
        test_book = Book.objects.create(
                    title="sample_title",
                    summary='no summary about thi book',
                    isbn='ABCDEU',
                    author=test_author,
                    language=test_language,
        )

         # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2022',
            due_back=return_date,
            borrower=test_user1,
            status='O',
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint='Unlikely Imprint, 2021',
            due_back=return_date,
            borrower=test_user2,
            status='O',
        )

    def test_redirect_if_not_loggedin(self):
        response = self.client.get(reverse_lazy("catalog:renew_due_back", 
                    kwargs={'pk': self.test_bookinstance1.pk})
                    )
        self.assertTrue(response.url.startswith("/auth/login/?next=/catalog/book/loan/"))
        self.assertEqual(response.status_code, 302)

    def test_permission_for_loggedin_user(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy("catalog:renew_due_back", 
                    kwargs={'pk': self.test_bookinstance1.pk})
                    )
        # now check permission is allowed or not
        self.assertEqual(response.status_code, 403)

    def test_logged_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse_lazy("catalog:renew_due_back", 
                                    kwargs={'pk': self.test_bookinstance2.pk}))
        self.assertEqual(response.status_code, 200)
        
    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse_lazy('catalog:renew_due_back', kwargs={'pk': self.test_bookinstance1.pk}))

        # Check that it lets us login. We're a librarian, so we can view any users book
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        # unlikely UID to match our bookinstance!
        test_uid = uuid.uuid4()
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse_lazy('catalog:renew_due_back', kwargs={'pk':test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse_lazy('catalog:renew_due_back', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'catalog/loan_book/renew.html')

    def test_form_renewal_date_initially_has_3weeks_in_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse_lazy('catalog:renew_due_back', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        date_3week_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(response.context['form'].initial['renewal_date'], date_3week_in_future)

    def test_redirects_to_all_borrowed_book_list_on_success(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
        response = self.client.post(reverse_lazy('catalog:renew_due_back', kwargs={'pk':self.test_bookinstance1.pk,}), {'renewal_date':valid_date_in_future})
        self.assertRedirects(response, reverse_lazy('catalog:list_loan'))

    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(reverse_lazy('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}), {'renewal_date': date_in_past})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal in past')

    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        response = self.client.post(reverse_lazy('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}), {'renewal_date': invalid_date_in_future})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'renewal_date', 'Invalid date - renewal more than 4 weeks ahead')
