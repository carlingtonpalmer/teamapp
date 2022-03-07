from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, ProductCategory, ProductSubCategory, ConfirmEmailNew #, Profile

# Register your models here.

#class UserProfileInline(admin.StackedInline):
#    model = Profile
#    can_delete = False


class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields' : ('email', 'password1', 'password2', 'first_name', 'last_name')
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
#    inlines = (UserProfileInline,)


class ProductCategoryAdmin(admin.ModelAdmin):# new changes 14/02/202
    list_display = ('title', 'image_tag', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(User, UserAdmin)
#admin.site.register(ProductCategory)
admin.site.register(ProductCategory, ProductCategoryAdmin)# new changes 14/02/202
admin.site.register(ProductSubCategory)
admin.site.register(ConfirmEmailNew)

# admin.site.register(Profile)



