from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline para editar el perfil del usuario desde el admin de User"""
    model = UserProfile
    fields = ('rol', 'telefono', 'foto_perfil', 'activo', 'fecha_creacion', 'ultima_conexion')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion', 'ultima_conexion')


class UserAdmin(BaseUserAdmin):
    """Extiende el UserAdmin de Django para incluir el perfil"""
    inlines = (UserProfileInline,)


# Desregistra el UserAdmin por defecto y registra el personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'rol', 'telefono', 'activo', 'fecha_creacion')
    list_filter = ('rol', 'activo', 'fecha_creacion')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'rol')
        }),
        ('Datos de Contacto', {
            'fields': ('telefono',)
        }),
        ('Perfil', {
            'fields': ('foto_perfil', 'activo')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_modificacion', 'ultima_conexion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Nombre Completo'
