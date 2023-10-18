from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    '''CarModelInline
    '''
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    '''CarModelAdmin
    '''
    fields = ["car_make", "dealer_id", "car_model_name", "car_model_year", "car_model_type"]

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    '''CarMakeAdmin
    '''
    inlines = [CarModelInline]
# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
