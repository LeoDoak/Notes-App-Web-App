from flask import session
import sys
sys.path.insert(1, '')


def test_logout(test_client):
    '''
    User story #5. Tests that logging out clears the user's session and redirects to the home page.
    '''
    with test_client:
        # Log the user in (set up the session)
        with test_client.session_transaction() as sess:
            sess['username'] = 'testuser'
        
        # Make sure the user is logged in
        assert 'username' in session

        # Simulate the logout
        response = test_client.get('/logout', follow_redirects=True)

        # Check that the user is redirected to the login page
        assert response.request.path == '/login'
        
        # Check that the session is cleared
        assert 'username' not in session
