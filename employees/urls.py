from django.urls import path, include
from employees import api_views, views as emp_view
from organizations import views as org_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'employees', viewset=api_views.EmployeeViewSet, basename='employees')
router.register(r'admin_users', viewset=api_views.AdminUserViewSet, basename='admin_users')
router.register(r'organizatons', org_views.OrganizationViewSet, basename='organizations')

urlpatterns = [
    path('', emp_view.landing_page, name='landing_page'),
    path('signUp/', emp_view.signup, name='signUp'),
    path('login/', emp_view.login, name='login'),
    path('forgot_password/', emp_view.forgot_password, name='forgot_password'),
    path('reset_token/', emp_view.confirm_password_reset_token, name='reset_token'),
    path('reset_password/', emp_view.reset_password, name='reset_password'),
    path('logout/', emp_view.logout, name='logout'),

    # API URLS
    path('api/', include(router.urls)),
    path('employees/<int:pk>/', api_views.EmployeeDetailViewSet.as_view(), name='employee-detail'),
    path('adminusers/<int:pk>/', api_views.AdminUserDetailViewSet.as_view(), name='adminuser-detail'),
    path('organizations/<int:pk>/', org_views.OrganizationViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='organization-detail'),
]
