from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from book.models import Category
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext as _
import uuid
from uaa.models import User


# Create your models here.
class EBook(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    createdBy = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="user_eBook_creator",blank=True,null=True)
    categoryId = models.ForeignKey(Category,on_delete=models.DO_NOTHING,related_name="category_e_Book",blank=True,null=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    author = models.CharField(max_length=50,blank=True,null=True)
    publisher = models.CharField(max_length=50,blank=True,null=True)
    yearOfPublication = models.CharField(max_length=50,blank=True,null=True)
    coverPageeBook = models.FileField(upload_to='coverPageImages', validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg'])]) 
    eBookFile = models.FileField(null=True, blank=True,upload_to='onlineeBook', validators=[FileExtensionValidator(['pdf'])])
    status = models.BooleanField(default=True) 
    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
    
    class Meta: 
        ordering = ['-createdAt']
    
    def __str__(self):
        return self.title
    
class ReadeBook(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    bookId = models.ForeignKey(EBook,on_delete=models.CASCADE,related_name="readEbook",blank=True,null=True)
    readNo = models.IntegerField(default=1,blank=True)
    status = models.BooleanField(default=True) 
    
    updatedAt = models.DateField(auto_now=True)
    
    class Meta: 
        ordering = ['-updatedAt']
    
    def __str__(self):
        return str(self.readNo)
