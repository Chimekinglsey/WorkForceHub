from cgitb import handler
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

    # Admin User urls
    path('signUp/', emp_view.signup, name='signUp'),
    path('login/', emp_view.login_view, name='login'),
    path('logout/', emp_view.logout_view, name='logout'),
    path('profileUpdate/', emp_view.profile_update, name='profile_update'),

    # Delegate admin urls
    path('accountSettings/', emp_view.profile_settings, name='profile_settings'),
    path('uploadBranchDocs/', emp_view.upload_documents, name='upload_branch_docs'),

    # Dashboard urls
    # path('createOrg/', emp_view.org_dashboard, name="create_org"),
    path('orgDashboard/', emp_view.org_dashboard, name='org_dashboard'),
    path('org/createBranch/', emp_view.create_branch, name="create_branch"),
    path('org/branch/<int:branch_id>/', emp_view.branch_dashboard, name="branch_dashboard"),
    path('org/deleteBranch/<int:branch_id>/', emp_view.delete_branch, name="delete_branch"),
    path('org/updateBranch/<int:branch_id>/', emp_view.update_branch, name="update_branch"),
    path('org/deleteOrg/<str:org_id>/', emp_view.delete_organization, name="delete_organization"),


    # Delegate and promoted delegates urls
    path('org/createDelegate/', emp_view.create_delegate, name="create_delegate"),
    path('org/updateDelegate/<int:delegate_id>/', emp_view.update_branch, name="update_delegate"),
    path('org/suspendDelegate/<int:delegate_id>/', emp_view.suspend_delegate, name="suspend_delegate"),
    path('org/activateDelegate/<int:delegate_id>/', emp_view.activate_delegate, name="activate_delegate"),
    path('org/promoteDelegate/<int:delegate_id>/', emp_view.promote_delegate, name="promote_delegate"),
    path('org/demoteAdmin/<int:admin_id>/', emp_view.demote_admin, name="demote_admin"),
    path('org/suspendAdmin/<int:admin_id>/', emp_view.suspend_admin, name="suspend_admin"),
    path('org/activateAdmin/<int:admin_id>/', emp_view.restore_admin, name="restore_admin"),

 
    # Employee Management
    path('updateEmployee/<str:emp_id>/', emp_view.update_employee, name="update_employee"),
    path('archiveEmployee/<str:emp_id>/', emp_view.archive_employee, name="archive_employee"),
    path('deleteEmployee/<str:emp_id>/', emp_view.delete_employee, name="delete_employee"),
    path('restoreArchive/<str:emp_id>/', emp_view.restore_archive, name='restore_archive'),
    path('org/deleteDelegate/<int:delegate_id>/', emp_view.delete_delegate, name="delete_delegate"),

    # Leave Management
    path('leaveRequest/', emp_view.leave_request, name='leave_request'),
    path('manageLeaveRequest/<int:leave_id>/', emp_view.manage_leave_request, name="manage_leave_request"),

    # Payroll Management
    path('createPayroll/', emp_view.create_payroll, name='create_payroll'),
    path('updatePayroll/<int:payroll_id>/', emp_view.update_payroll, name='update_payroll'),
    path('payrollDetail/<int:payroll_id>/', emp_view.payroll_detail, name='payroll_detail'),
    path('payrollList/', emp_view.payroll_list, name='payroll_list'),
    path('deletePayroll/<int:payroll_id>/', emp_view.delete_payroll, name='delete_payroll'),
    path('payrollHistory/<int:emp_id>/', emp_view.payroll_history, name='payroll_history'),

    # Performance Management
    path('employeePerformance/<str:emp_id>/', emp_view.performance_dashboard, name='performance_dashboard'),
    path('performanceReview/<int:emp_id>/', emp_view.performance_review, name='performance_review'),
    path('updatePerformance/<int:performance_id>/', emp_view.update_performance_review, name='update_performance'),
    path('deletePerformance/<int:performance_id>/', emp_view.delete_performance_review, name='delete_performance'),


    # Transfer Management
    path('transferRequest/', emp_view.transfer_request, name='transfer_request'),
    path('cancelTransfer/<int:transfer_id>/', emp_view.cancel_transfer_request, name='cancel_transfer'),
    path('manageTransferRequest/<int:transfer_id>/', emp_view.manage_transfer_request, name='manage_transfer_request'),


    # Reports and statistics
    path('branch/reports/<int:branch_id>/', emp_view.create_report, name='create_report'),
    path('branch/updateReport/<int:report_id>/', emp_view.update_report, name='update_report'),
    path('statistics/', emp_view.statistics, name='statistics'),


    # Finance URL
    path('finance/<int:branch_id>/', emp_view.finance_report, name='finance_dashboard'),
    path('finance/report/<int:branch_id>/<str:type>/', emp_view.finance_report, name='finance_report'),

    # Password urls for admin
    path('changePassword/', emp_view.change_password, name='change_password'), # used by both admin and delegate with can_change_password privilege
    path('forgotPassword/', emp_view.forgot_password, name='forgot_password'),
    path('resetPasswordToken/<str:email>/', emp_view.confirm_password_reset_token, name='reset_token'),
    path('resetPassword/<str:email>/', emp_view.reset_password, name='reset_password'),
    path('resetDelegatePassword/', emp_view.reset_delegate_password, name='reset_delegate_password'),



    # Footer urls
    path('quickGuide/', emp_view.quick_guide, name='quick_guide'),
    path('about/', emp_view.about, name='about'),
    path('terms/', emp_view.terms, name='terms'),
    path('privacy/', emp_view.privacy, name='privacy'),
    path('faq/', emp_view.faq, name='faq'),
    path('developers/', emp_view.developers, name='developers'),


    # set favicon
    path('favicon.ico/', emp_view.favicon, name='favicon'),


    # API URLS
    path('api/', org_views.WorkforceHubAPI.as_view(), name='workforcehub-api-root'),
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
if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
