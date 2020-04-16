from django.urls import include, path
from rest_framework import routers
from . import views

table_list = views.TableViewSet.as_view({'get': 'list'})
table_detail = views.TableViewSet.as_view({'get': 'retrieve'})

router = routers.DefaultRouter()
router.register(r'tables', views.TableViewSet, basename='table')
router.register(r'tablerows', views.TableRowViewSet)
router.register(r'tableresults', views.TableResultViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]