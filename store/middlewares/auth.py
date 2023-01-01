


def Auth_middleware(get_response):

    def middleware(request):
        print('middleware')
        response = get_response(request)
        return response

    return middleware