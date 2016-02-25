from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('oneliners')


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'valid', 'likes')
    list_filter = ('text', 'valid', 'likes')


for model_name, model in app.models.items():
    exclude = ['baseuser_groups', 'baseuser_user_permissions']
    if model_name == 'quote':
        admin.site.register(model, QuoteAdmin)
    elif model_name not in exclude:
        admin.site.register(model)
