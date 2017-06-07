from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from whitelist.models import Whitelisted


class WhitelistedModelAdmin(ModelAdmin):
    model = Whitelisted
    menu_label = 'Whitelisted players'
    menu_icon = 'user'
    menu_order = 200
    list_display = (
        'username', 'email', 'uuid', 'submitted_on', 'approved', 'approved_on')
    list_filter = ('submitted_on', 'approved', 'approved_on',)
    search_fields = ('username', 'email', 'uuid')


modeladmin_register(WhitelistedModelAdmin)
