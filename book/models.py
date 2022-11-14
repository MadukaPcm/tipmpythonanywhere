from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext as _
import uuid
from uaa.models import User
import datetime

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    categoryName = models.CharField(max_length=20,blank=True,null=True)
    createdBy = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="user_category_creator",blank=True,null=True)
    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)

    class Meta: 
            ordering = ['-createdAt']
    
    def __str__(self):
        return self.categoryName
    
class MaximumBookLimit(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    stuff = models.CharField(max_length=1,null=True,blank=True)
    student = models.CharField(max_length=1,null=True,blank=True)
    days = models.CharField(max_length=1,null=True,blank=True)
    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)

    class Meta: 
            ordering = ['-createdAt']
    
    def __str__(self):
        return self.stuff
    

class Book(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    categoryId = models.ForeignKey(Category,on_delete=models.DO_NOTHING,related_name="category",blank=True,null=True)
    createdBy = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="user_book_creator",blank=True,null=True)
    bookNumber = models.CharField(max_length=50,blank=True,null=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    author = models.CharField(max_length=50,blank=True,null=True)
    isbn = models.CharField(max_length=50,blank=True,null=True)
    publisher = models.CharField(max_length=50,blank=True,null=True)
    placeOfPublication = models.CharField(max_length=60,blank=True,null=True)
    yearOfPublication = models.CharField(max_length=50,blank=True,null=True)
    coverPageImage = models.FileField(upload_to='coverPageImages', validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg'])])
    description = models.CharField(max_length=255,blank=True,null=True)  
    status = models.BooleanField(default=True)    
    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
    
    class Meta: 
        ordering = ['-createdAt']
    
    def __str__(self):
        return self.title
    
    
class RequestedBook(models.Model):
    # id = models.AutoField(primary_key=True)
    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True,primary_key=True)
    userId = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_book_requestor",blank=True,null=True)
    bookId = models.ForeignKey(Book,on_delete=models.CASCADE,related_name="book",blank=True,null=True)
    issueDate = models.DateField()
    dueDate = models.DateField()
    status = models.BooleanField(default=True)
    isApproved = models.BooleanField(default=False)
    isPending = models.BooleanField(default=True)
    isTaken = models.BooleanField(default=False)
    isREturned = models.BooleanField(default=False)
    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
    
    class Meta: 
        ordering = ['-updatedAt'] 
    
    def __str__(self):
        return str(self.bookId.title)
    
    @property
    def noDays(self):
        return ((datetime.date.today()) - self.issueDate).days
    
#dealing with online library----

    
    
        
    