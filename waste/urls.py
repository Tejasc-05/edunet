from django.urls import path
from . import views

app_name = 'waste'

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard and main views
    path('dashboard/', views.index_view, name='dashboard'),
    path('reports/', views.user_reports, name='user_reports'),
    path('statistics/', views.get_statistics, name='statistics'),
    
    # Category details
    path('biodegradable/', views.category_detail, {'category_name': 'biodegradable'}, name='biodegradable'),
    path('plastic/', views.category_detail, {'category_name': 'plastic'}, name='plastic'),
    path('ewaste/', views.category_detail, {'category_name': 'ewaste'}, name='ewaste'),
    path('metal/', views.category_detail, {'category_name': 'metal'}, name='metal'),
    path('glass/', views.category_detail, {'category_name': 'glass'}, name='glass'),
    path('hazardous/', views.category_detail, {'category_name': 'hazardous'}, name='hazardous'),
    
    # Waste report
    path('add-report/', views.add_waste_report, name='add_report'),
    
    # Camera scanning
    path('camera/', views.camera_scan, name='camera_scan'),
    path('api/classify/', views.classify_waste_api, name='classify_api'),
    
    # Points and Coupons
    path('coupons/', views.coupons_view, name='coupons'),
    path('coupons/redeem/', views.redeem_coupon, name='redeem_coupon'),
    path('my-coupons/', views.my_coupons_view, name='my_coupons'),
]
