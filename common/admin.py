from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import(
    User,
    Coin,
    WalletAddress,
)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    """Coin Admine."""

    list_display = ['name', 'code', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['name', 'code', 'is_active']


@admin.register(WalletAddress)
class WalletAddressAdmin(admin.ModelAdmin):
    """WalletAddress Admin."""

    list_display = ['username', 'address', 'coin', 'is_active']
    search_fields = ['username', 'username', 'coin']
    ordering = ['username', 'address', 'coin', 'is_active']
