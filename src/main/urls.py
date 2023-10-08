from django.contrib import admin
from django.urls import path, include
from apps.users.views import UserLoginView, RegisterView, activate_view
from apps.blog.views import BlogView, HomeView, ArticleView
from apps.shop.views import ProductListView, ProductDetailView, AddCartView, CartView, UpdateCartView, RemoveCartItemView, create_gallery
from main import settings
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', ProductListView.as_view(), name='shop'),
    path('cart/', CartView.as_view(), name='cart'),
    path('', HomeView.as_view(), name='home'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('blog/<int:pk>', ArticleView.as_view(), name='article'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('add_to_cart/<int:product_id>/', AddCartView.as_view(), name='add_to_cart'),
    path('change_password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('add-to-cart/', AddCartView.as_view(), name='add_to_cart'),
    path('update-cart/', UpdateCartView.as_view(), name='update_cart'),
    path('remove-cart-item/<int:item_id>', RemoveCartItemView.as_view(), name='remove_cart_item'),
    path('add_item/', create_gallery, name='add'),

    # auth
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/", activate_view, name="activate"),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
