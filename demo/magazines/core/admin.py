from django.contrib import admin

import core.models


admin.site.register((
    core.models.Magazine,
    core.models.Article,
))
