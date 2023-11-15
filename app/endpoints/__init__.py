from app.endpoints.classifier_module import classifier_router
from app.endpoints.for_tests import test_router

all_routes = [
    test_router,
    classifier_router
]

__all__ = [
    'all_routes'
]
