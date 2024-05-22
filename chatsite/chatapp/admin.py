from django.contrib import admin

import chatapp.models as model

# Register your models here.

admin.site.register(model.RoomModel)
admin.site.register(model.MessagesModel)