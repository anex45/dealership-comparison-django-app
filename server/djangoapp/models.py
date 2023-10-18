from django.db import models
from django.utils.timezone import now
from django.conf import settings

class CarMake(models.Model):
    '''Car Make
    '''
    car_make_name = models.CharField(max_length=500)
    car_make_description = models.CharField(max_length=1000)
    def __str__(self):
        return self.car_make_name

class CarModel(models.Model):
    '''CarModel
    '''
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    car_model_name = models.CharField(max_length=500)
    car_model_year = models.DateField(default=now)

    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    CAR_TYPES = [(SEDAN, 'Sedan'), (SUV, 'SUV'), (WAGON, 'WAGON')]

    car_model_type = models.CharField(max_length=100, choices=CAR_TYPES)

    def __str__(self):
        return self.car_model_name
        
# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
