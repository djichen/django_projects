
# Copy this file to github_settings.py (don't check it into github)

# Go to https://github.com/settings/developers

# Add a New OAuth2 App

# Using ngrok is hard because the url changes every time you start ngrok

# If you are running on localhost, here are some settings:

# Application name: Django on Desktop
# Homepage Url: http://localhost:8000
# Application Description: Whatever
# Authorization callback URL: http://127.0.0.1:8000/oauth/complete/github/


# Using PythonAnywhere here are some settings:
# Homepage Url: https://drchuck.pythonanywhere.com
# Application Description: Whatever
# Authorization callback URL: https://drchuck.pythonanywhere.com/oauth/complete/github/

# Also on PythonAnywhere, go into the Web tab and enable "Force HTTPS"
# so you don't get a redirect URI mismatch.

# Then copy the client_key and secret to this file

SOCIAL_AUTH_GITHUB_KEY = 'a2bbd33156603d7e06f1'
SOCIAL_AUTH_GITHUB_SECRET = '31af2915298d3a9eaa2d444c5ad6a485287e8bc5'

from django.contrib.auth import views as auth_views
try:
    from . import github_settings
    social_login = 'registration/login_social.html'
    urlpatterns.insert(0,
        path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
    )
    print('Using',social_login,'as the login template')
except:
    print('Using registration/login.html as the login template')
