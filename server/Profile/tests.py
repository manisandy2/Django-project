from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Account
import uuid
# import HTMLTestRunner
import unittest

class AccountModelTest(TestCase):
    def setUp(self):
        # Create a custom user for testing
        self.user = get_user_model().objects.create_user(
            email="testuser@gmail.com", password="testpassword"
        )
    
    def test_account_creation(self):
        # Create an Account object
        account = Account.objects.create(
            name="Test Account",
            created_by=self.user,
            updated_by=self.user
        )
        
        # Test the account's name and id
        self.assertEqual(account.name, "Test Account")
        self.assertIsInstance(account.id, uuid.UUID)
        self.assertEqual(account.created_by, self.user)
        self.assertEqual(account.updated_by, self.user)
        self.assertIsNotNone(account.created_at)
        self.assertIsNotNone(account.updated_at)
    
    def test_account_str(self):
        # Create an Account object
        account = Account.objects.create(
            name="Test Account",
            created_by=self.user,
            updated_by=self.user
        )
        
        # Test the __str__ method
        self.assertEqual(str(account), f"Test Account ({account.id})")

    def test_account_optional_fields(self):
        # Create an Account object with optional fields
        account = Account.objects.create(
            name="Test Account With Website",
            website="https://example.com",
            created_by=self.user,
            updated_by=self.user
        )
        
        # Test that the website field is populated correctly
        self.assertEqual(account.website, "https://example.com")

    def test_account_secret_token(self):
        # Create an Account object and check the secret_token field
        account = Account.objects.create(
            name="Test Account",
            created_by=self.user,
            updated_by=self.user
        )
        
        # Ensure that the secret_token is automatically generated and is not empty
        self.assertIsNotNone(account.secret_token)
        self.assertNotEqual(account.secret_token, "")
    
    def test_account_null_values(self):
        # Test that the optional fields are nullable
        account = Account.objects.create(
            name="Test Account No Website",
            created_by=self.user,
            updated_by=self.user
        )
        
        # Test that website can be null
        self.assertIsNone(account.website)

# if __name__ == "__main__":
#     suite = unittest.TestLoader().loadTestsFromTestCase(AccountModelTest)
#     with open("test_report.html", "w") as report_file:
#         runner = HTMLTestRunner.HTMLTestRunner(stream=report_file, verbosity=2)
#         runner.run(suite)