from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tracking import views as tracking_views
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'), 
    path('post-login-redirect/', tracking_views.post_login_redirect, name='post_login_redirect'),
    path('', include('tracking.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)