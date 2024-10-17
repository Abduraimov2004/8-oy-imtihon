from django.urls import path

from . import user

from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='all-products'),

    # Categories
    path('categories/', CategoryListView.as_view(), name='all-categories'),
    path('category/<slug:category_slug>/', CategoryProductListView.as_view(), name='category-products'),
    path('category/add-category/', CategoryCreateView.as_view(), name='add-category'),
    path('category/<slug:category_slug>/delete/', CategoryDeleteView.as_view(), name='delete-category'),
    path('category/<slug:slug>/edit/', CategoryUpdateView.as_view(), name='edit-category'),


    path('product/detail/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:id>/edit/', ProductUpdateView.as_view(), name='edit-product'),
    path('product/<int:product_id>/delete/', ProductDeleteView.as_view(), name='delete-product'),

    path('attribute-key/', AttributeKeyListView.as_view(), name='all-attribute-keys'),
    path('attribute-value/', AttributeValueListView.as_view(), name='all-attribute-values'),

    path('token-auth/', CustomAuthToken.as_view(), name='token-auth'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('login/', user.UserLoginApiView.as_view(), name='login'),
    path('logout/', user.UserLogoutApiView.as_view(), name='logout'),
]
