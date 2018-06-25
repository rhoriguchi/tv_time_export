ERROR_MESSAGES = [
    'This user does not exist',
    'You did not give the correct password for this username'
]


class ErrorHandler(object):
    @staticmethod
    def check_response(response):
        content = str(response.content)
        for error_message in ERROR_MESSAGES:
            if error_message in content:
                raise ValueError('Tv Time returned error: %s' % error_message)
