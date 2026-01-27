
class CoreMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Avant la vue
        print(f"Requête entrante : {request.method} {request.path}")
        print(f"IP : {request.META.get('REMOTE_ADDR')}")

        response = self.get_response(request)   # → passe à la vue ou middleware suivant
        # Après la vue
        print(f"Réponse envoyée : {response.status_code}")

        return response