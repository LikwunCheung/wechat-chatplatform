from django.utils.deprecation import MiddlewareMixin


class CrosMeddleware(MiddlewareMixin):

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS, POST, PUT'
        response['Access-Control-Allow-Headers'] = '*'
        response['Access-Control-Max-Age'] = 7200
        return response