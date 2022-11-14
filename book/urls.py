from django.urls import path
from . import views

#paths for account app.
urlpatterns = [
    path('',views.BookView, name='Book_url'),
    path('createBook/',views.CreateBookView, name='createBook_url'),
    path('manageBookView/',views.ManageBookView, name='manageBookView_url'), 
    
    path('actionViewBook/<str:pk>',views.ActionViewBookView, name='actionViewBook_url'),
    path('actionUpdateBookView/<str:pk>',views.ActionUpdateBookView, name='actionUpdateBookView_url'),
    path('actionDeleteBookView/',views.ActionDeleteBookView, name='actionDeleteBookView_url'),
    
    path('requestBook/<str:pk>',views.RequestBookView, name="RequestBook_url"),
    path('requestingBookView/', views.RequestingBookView, name='requestingBookView_url'),
    
    path('issuedBookView/', views.IssuedBookView, name='issuedBookView_url'),
    path('verifyPedingView/', views.VerifyPedingView, name='verifyPedingView_url'),
    path('approveVerifiedView/', views.ApproveVerifiedView, name='approveVerifiedView_url'),
    
    path('borrowedBookView/', views.BorrowedBookView, name='borrowedBookView_url'),
    path('getBorrowedBookView/<str:pk>', views.GetBorrowedBookView, name='getBorrowedBookView_url'),
    
    path('returnedBookView/', views.ReturnedBookView, name='returnedBookView_url'),
    path('getReturnedBookView/<str:pk>', views.GetReturnedBookView, name='getReturnedBookView_url'),
    
    path('notReturnedBookView/', views.NotReturnedBookView, name='notReturnedBookView_url'),
    path('getNotReturnedBookView/<str:pk>', views.GetNotReturnedBookView, name='getNotReturnedBookView_url'),
    path('approveReturnView/', views.ApproveReturnView, name='approveReturnView_url'),
    
    #Views about book status taken by a user specifically:
    path('booksPendingView/', views.BooksPendingView, name='booksPendingView_url'),
    path('booksApprovedView/', views.BooksApprovedView, name='booksApprovedView_url'),
    path('booksITookView/', views.BooksITookView, name='booksITookView_url'), 

    path('categoryBookView/', views.CategoryBookView, name='categoryBookView_url'),
    path('createCategoryBookView/', views.CreateCategoryBookView, name='createCategoryBookView_url'),
    path('updateCategoryBookView/<str:pk>', views.UpdateCategoryBookView, name='updateCategoryBookView_url'),
    
    path('maxBookLimitView/', views.MaxBookLimitView, name='maxBookLimitView_url'),
    path('updateMaxBookLimitView/<str:pk>', views.updateMaxBookLimitView, name='updateMaxBookLimitView_url'),
]