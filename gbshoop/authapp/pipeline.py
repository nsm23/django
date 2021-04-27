from django.contrib.sites import requests
from social_core.exceptions import AuthForbidden
import urllib.request
from authapp.models import GbUserProfile, Gbuser


def save_user_profile(backend, user, response, *args, **kwargs):
    print(response)
    if backend.name == "google_oauth2":
        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.gbuserprofile.gender = GbUserProfile.MALE
            else:
                user.gbuserprofile.gender = GbUserProfile.FEMALE

        if 'tagline' in response.keys():
            user.gbuserprofile.tagline = response['tag']

        if 'about_me' in response.keys():
            user.gbuserprofile.about_me = response['about_me']

        if 'picture' in response.keys():
            pic = response.requests.get(url)
            out = open('media/avatars/use.jpg', 'wb')
            out.write(pic.content)
            out.close()

        if 'ageRange' in response.keys():
            minAge = response['ageRange']['min']
            if int(minAge) < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
        user.save()
