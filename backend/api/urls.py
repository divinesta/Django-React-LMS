from api import views as api_views
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
      # Aunthentication Endpoints

      path('user/token/', api_views.MyTokenObtainPairView.as_view()),
      path('user/token/refresh/', TokenRefreshView.as_view()),
      path('user/register/', api_views.RegisterView.as_view()),
      path('user/password-reset/<email>/', api_views.PasswordResetEmailVerifyAPIView.as_view()),
      path('user/password-change/', api_views.PasswordChangeAPIView.as_view()),
      
      # Core Endpoints
      path('course/category/', api_views.CategoryListAPIView.as_view()),
      path('course/course-list/', api_views.CourseListAPIView.as_view()),
      path('course/course-detail/<slug>/', api_views.CourseDetailAPIView.as_view()),
      path('course/cart/', api_views.CartAPIView.as_view()),
      path('course/cart-list/<cart_id>/', api_views.CartlistAPIView.as_view()),
      path('course/cart-item-delete/<cart_id>/<item_id>/', api_views.CartItemDeleteAPIView.as_view()),
]