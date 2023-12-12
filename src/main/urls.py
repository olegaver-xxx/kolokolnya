from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

# from apps.shop.services import confirm_payment
from apps.users.views import UserLoginView, RegisterView, activate_view
from apps.blog.views import BlogView, HomeView, ArticleView, AddArticle
from apps.users.views import ProfileView, update_user
from apps.shop.views import ProductListView, ProductDetailView, AddCartView, CartView, UpdateCartView, \
    RemoveCartItemView, create_gallery, ContactView, OrderListView, payment_event, RecordsView, \
    RemoveRecord, OrderDetailView, OrderDetail, MakeOrder, make_order, PayedOrdersView, CompleteOrder, \
    CompletedOrdersView  # , AddRecordView
from apps.utils.views import PreferencesView, MainView
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/prefs/', PreferencesView.as_view(), name='admin_prefs'),
    path('admin/', admin.site.urls),
    path('shop/', ProductListView.as_view(), name='shop'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit', update_user, name='edit'),
    path('profile/history', OrderListView.as_view(), name='history'),
    path('cart/', CartView.as_view(), name='cart'),
    path('rec/', RecordsView.as_view(), name='records'),
    path('order/', MakeOrder.as_view(), name='make_order'),
    path('make-order/', make_order, name='make_order_submit'),
    # path('search/', SearchView.as_view(), name='search_results'),
    path('', HomeView.as_view(), name='home'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('blog/<int:pk>', ArticleView.as_view(), name='article'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('add_to_cart/<int:product_id>/', AddCartView.as_view(), name='add_to_cart'),
    # path('add-record/', AddRecordView.as_view(), name='add_record'),
    path('change_password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('add-to-cart/', AddCartView.as_view(), name='add_to_cart'),
    # path('tags-resluts/', TagsFilteringView.as_view(), name='tags'),
    path('update-cart/', UpdateCartView.as_view(), name='update_cart'),
    path('remove-cart-item/<int:item_id>', RemoveCartItemView.as_view(), name='remove_cart_item'),
    path('remove-rec-item/<int:rec_id>', RemoveRecord.as_view(), name='del_rec'),
    # path('add_item/', create_gallery, name='add'),
    # path('add_article/', AddArticle.as_view(), name='add_art'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # auth
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", RegisterView.as_view(), name="register"),
    re_path("activate/.*", activate_view, name="activate"),
    path('payment-success/', TemplateView.as_view(template_name='payment-success.html'), name='payment-success'),
    # path('test_home/', TemplateView.as_view(template_name='index.html'), name='test-home'),
    path('test_home/', MainView.as_view(), name='test-home'),
    path('payment-event/', payment_event, name='payment-event'),
    path('history/', TemplateView.as_view(template_name='history.html'), name='town_history'),
    path('attractions/', TemplateView.as_view(template_name='attractions.html'), name='attractions'),
    # path('test/', TemplateView.as_view(template_name='order_detail.html'), name='test_link'),
    path('test/<int:pk>', OrderDetail.as_view(), name='order_detail'),
    path('complete_order/', payment_event, name='complete'),
    path('complete/', CompleteOrder.as_view(), name='complete_order'),
    path('payed-orders/', PayedOrdersView.as_view(), name='payed_list'),
    path('completed_orders/', CompletedOrdersView.as_view(), name='completed_list'),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

