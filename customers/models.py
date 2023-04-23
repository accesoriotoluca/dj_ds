from django.db import models

class Customer(models.Model):

    name = models.CharField(max_length=120)
    
    #upload_to='customers': inside the media customer we´ve another folder called customers where to keep images
    logo = models.ImageField(upload_to='customers', default='no_picture.png')

    #string representation of particular object
    def __str__(self):
        return str(self.name)