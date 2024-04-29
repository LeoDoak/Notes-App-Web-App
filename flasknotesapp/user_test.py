# As a user I want to be able to login 
import unittest
from objects.user import User  

class TestUserClass(unittest.TestCase):

    def test_user_initialization(self):
            # Test initialization of User objects
            user = User("1", "JohnSmith1", "Random12", "js7456@uncw.edu")
            self.assertEqual(user.user_id, "1")
            self.assertEqual(user.username, "JohnSmith1")
            self.assertEqual(user.password, "Random12")
            self.assertEqual(user.email, "js7456@uncw.edu")

            #everything is blank
            try:
                # Test default initialization values
                user2 = User("", "", "", "")
                self.assertEqual(user2.user_id, "")
                self.assertEqual(user2.username, "")
                self.assertEqual(user2.password, "")
                self.assertEqual(user2.email, "")
            except Exception as e:
                self.fail(f"Meant to result in an error: {e}")

            # everything is integers
            try:
                # Test default initialization values
                user3 = User("10", "10", "10", "10")
                self.assertEqual(user2.user_id, "10")
                self.assertEqual(user2.username, "10")
                self.assertEqual(user2.password, "10")
                self.assertEqual(user2.email, "10")
            except Exception as e:
                self.fail(f"Meant to result in an error: {e}")


            # mix of blank and integer
            try:
                # Test default initialization values
                user3 = User("10", "", "", "10")
                self.assertEqual(user2.user_id, "10")
                self.assertEqual(user2.username, "")
                self.assertEqual(user2.password, "")
                self.assertEqual(user2.email, "10")
            except Exception as e:
                self.fail(f"Meant to result in an error: {e}")

            # invalid email 
            # mix of blank and integer
            try:
                # Test default initialization values
                user3 = User("10", "", "", "10")
                self.assertEqual(user2.user_id, "10")
                self.assertEqual(user2.username, "ldoak")
                self.assertEqual(user2.password, "Lsdfjksh1nk!")
                self.assertEqual(user2.email, "leodoak")
            except Exception as e:
                self.fail(f"Meant to result in an error from improper email : {e}")

            

    


    # Add more test cases for other methods...

if __name__ == '__main__':
    unittest.main()

