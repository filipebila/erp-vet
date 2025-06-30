# middleware/debug_host.py

class PrintHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("🌐 Host recebido no middleware:", request.get_host())
        return self.get_response(request)