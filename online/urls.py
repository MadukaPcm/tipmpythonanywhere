from django.urls import path
from . import views

#paths for account app. 
urlpatterns = [
    path('',views.OnlineView, name='onlineView_url'),
    path('editEBook/<str:pk>',views.EditEBookView, name='editEBookView_url'),
    path('softDeleteEBook/',views.SoftDeleteEBookView, name='softDeleteEBookView_url'),
    path('allEBooks/', views.AllEBooksView, name='allEBooks_url'),
    path('createeBook/',views.CreateeBookView, name='createeBook_url'),
    path('readeBook/<str:pk>',views.ReadeBookView, name='readeBook_url'),  
    path('vieweBook/<str:pk>',views.VieweBookView, name='vieweBook_url'),
    path('readeBookView/',views.ReadeBookStatusView, name='readeBookView_url'),
]