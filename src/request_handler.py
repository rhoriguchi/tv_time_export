import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from src.error_handler import ErrorHandler

PAGE_URL = 'https://www.tvtime.com/'


class RequestHandler(object):
    def __init__(self, username, password):
        self._session = requests.Session()
        self._username = username
        self._password = password
        self._profile_id = None

    def login(self):
        url = urljoin(PAGE_URL, 'signin')

        data = {'username': self._username, 'password': self._password}
        response = self._session.post(url, data=data)

        ErrorHandler.check_response(response)
        soup = BeautifulSoup(response.content, 'html.parser')

        for link in soup.find_all('a'):
            match = re.search('^.*/user/(\d*)/profile$', link.get('href'))
            if match is not None and match.group(1) is not None:
                self._profile_id = match.group(1)

    def logout(self):
        url = urljoin(PAGE_URL, 'signout')
        self._session.get(url)

    def get_data(self):
        url = urljoin(PAGE_URL, ('user/%s/profile' % self._profile_id))
        response = self._session.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.)
