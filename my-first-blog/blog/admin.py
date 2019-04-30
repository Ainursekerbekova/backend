from django.contrib import admin
from .models import needforvideo
from .models import feedback
from .models import product
from .models import OrderItem
from .models import Order
from .models import kolvo
from .models import Type

admin.site.register(needforvideo)
admin.site.register(feedback)
admin.site.register(product)
admin.site.register(Type)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(kolvo)