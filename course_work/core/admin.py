from django.contrib import admin

from .forms import SubCategoryForm
from .models import AdvUser, SuperCategory, SubCategory, Bb, AddiionalImage

# Register your models here.
class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (('username', 'email'), ('first_name', 'last_name'), \
                ('is_staff', 'is_superuser'), \
                'groups', 'user_permissions', \
                ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')


class SubCategoryInline(admin.TabularInline):
    model = SubCategory


class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ('super_category',)
    inlines = (SubCategoryInline,)


class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm


class AddiionalImageInline(admin.TabularInline):
    model = AddiionalImage


class BbAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'content', 'author', 'created_at')
    fields = (('category', 'author'), 'title', 'content', 'price', 'contacts', \
                'image', 'is_active')
    inlines = (AddiionalImageInline,)


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(SuperCategory, SuperCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Bb, BbAdmin)
