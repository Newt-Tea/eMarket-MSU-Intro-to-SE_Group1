from django.contrib import admin
from .models import *

# For product display within user page
from django.utils.html import format_html
from django.urls import reverse


# User Admin display
class UserAdmin(admin.ModelAdmin):
    # How data is displayed when clicking on user
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'password', 'user_type', 'date_joined', 'last_login', ),
        }),
        ('User Pending', {
            'fields': ('pending', ),
        }),
    )

    readonly_fields = ('password', 'date_joined', 'last_login', 'ProductSet')

    def get_fieldsets(self, request, obj=None):
        # Get the default fieldsets
        fieldsets = super().get_fieldsets(request, obj)
        
        # Check if the user_type is 'seller' to add the "Seller Products" fieldset
        if obj.user_type == 'seller':
            # Append the Seller Products fieldset
            fieldsets += (
                ('Seller Products', {
                    'fields': ('ProductSet', ),
                }),
            )
        
        return fieldsets

    # How Users are displayed in the list
    list_display = ('username', 'user_type', 'formattedUserID', 'pending')
    list_editable = ('pending', )

    # Filter and search functionality
    list_filter = ('user_type', 'pending')
    search_fields = ('username', )

    # Instead of being displayed as 'pk', displays as 'User ID'
    def formattedUserID(self, obj):
        return obj.pk
    formattedUserID.short_description = 'User ID'
    formattedUserID.admin_order_field = 'pk'

    # In the admin dashboard, display a list of connected product links that go to each product's page
    def ProductSet(self,obj):
        product_links = [format_html('<a href="{}">{}</a>', reverse('admin:app_product_change', args=[product.id]), product.name) for product in obj.products.all()]
        return format_html(", ".join(product_links))
    ProductSet.short_description = 'Listed Products'

# Product Admin display
class ProductAdmin(admin.ModelAdmin):
    # How data is displayed when clicking on Product
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'price', 'stock', 'date_created', ),
        }),
        ('Seller Information', {
            'fields': ('seller_username', ),
        }),
    )
    readonly_fields = ('date_created', )

    # How Products are displayed in the list
    list_display = ('name', 'price', 'stock', 'formattedProductID', )

    # Search functionality
    search_fields = ('name', )

    # Instead of being displayed as 'pk', displays as 'Product ID'
    def formattedProductID(self, obj):
        return obj.pk
    formattedProductID.short_description = 'Product ID'
    formattedProductID.admin_order_field = 'pk'

# Cart Admin display
class CartAdmin(admin.ModelAdmin):
    pass

# CartProduct Admin display
class CartProductAdmin(admin.ModelAdmin):
    pass

# Order Admin display
class OrderAdmin(admin.ModelAdmin):
    pass




# Registered models
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Order, OrderAdmin)