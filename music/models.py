from django.db import models
from django.core.validators import FileExtensionValidator
# from django.core.exceptions import ValidationError
# Create your models here.
class Album(models.Model):
    title=models.CharField(max_length=100,null=False,help_text='album title')
    artist=models.CharField(max_length=100,help_text='album artist')
    genre=models.CharField(max_length=50,help_text='album genre')
    year=models.DateField(help_text='Enter year in yyyy-mm-dd format')
    image=models.FileField(validators=[FileExtensionValidator(['jpg','png'])],default='')
    # image=models.ImageField(width_field=200,height_field=300,validators=image_validate)
    # for image size validator
    # def image_validate(self,image):
    #     max_height=200 #in pixel
    #     max_width=300
    #     height=image.file.height
    #     width=image.file.width
    #     if width>max_width or height>max_height:
    #         raise ValidationError("Height or width is larger than what is allowed")  
   
    def __str__(self):
        return self.title

class Song(models.Model):
    al_id=models.ForeignKey(Album,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,null=False,help_text='song title')  
    artist=models.CharField(max_length=100,help_text='song artist')      
    genre=models.CharField(max_length=20,help_text='song genre')
    sfile=models.FileField(validators=[FileExtensionValidator(['mp3','aac'])])
    image=models.FileField(validators=[FileExtensionValidator(['jpg','png'])],default='')

    def __str__(self):
        return self.title