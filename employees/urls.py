from django.urls import path, include
from employees import api_views, views as emp_view
from organizations import views as org_views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'employees', viewset=api_views.EmployeeViewSet, basename='employees')
router.register(r'admin_users', viewset=api_views.AdminUserViewSet, basename='admin_users')
router.register(r'organizatons', org_views.OrganizationViewSet, basename='organizations')

urlpatterns = [
    path('', emp_view.landing_page, name='landing_page'),
    path('signUp/', emp_view.signup, name='signUp'),
    path('login/', emp_view.login_view, name='login'),
    path('logout/', emp_view.logout_view, name='logout'),
    path('profileUpdate/', emp_view.profile_update, name='profile_update'),
    path('createOrg/', emp_view.org_dashboard, name="create_org"),
    path('org/createBranch/', emp_view.create_branch, name="create_branch"),
    path('org/branch/<int:branch_id>/', emp_view.branch_dashboard, name="branch_dashboard"),
    path('updateEmployee/<int:emp_id>/', emp_view.update_employee, name="update_employee"),
    path('archiveEmployee/<int:emp_id>/', emp_view.archive_employee, name="archive_employee"),
    path('forgotPassword/', emp_view.forgot_password, name='forgot_password'),
    path('resetToken/', emp_view.confirm_password_reset_token, name='reset_token'),
    path('resetPassword/', emp_view.reset_password, name='reset_password'),

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
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
