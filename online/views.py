from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.db.models import Q
from uaa.decorators import admin_only, allowed_users, manager_only, unauthenticated_user
from online.models import EBook,ReadeBook
from book.models import Category
from django.http import FileResponse,Http404,HttpResponse
import os

# Create your views here.
@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def OnlineView(request):
    EBookObjectList = EBook.objects.filter(status=True)
    
    context = {"EBookObject":EBookObjectList}
    return render(request,"online/onlinePage.html",context)   

@unauthenticated_user
@admin_only
def EditEBookView(request, pk):
    
    bookCategoryObject = Category.objects.all()
    editEBookObject = EBook.objects.filter(id=pk).first()
    
    if request.method == "POST":
        categoryId = request.POST.get('categoryId')
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        yearOfPublication = request.POST.get('yearOfPublication')
        
        try:
            editEBookObject.categoryId_id = categoryId
            editEBookObject.createdBy_id=request.user.id 
            editEBookObject.title = title
            editEBookObject.author = author
            editEBookObject.publisher = publisher
            editEBookObject.yearOfPublication = yearOfPublication
            editEBookObject.save()
            
            messages.info(request,'sucessfully, Updated')
            return redirect('onlineView_url')
    
        except Exception as e:
            print(e)
    
    context = {"categoty_id":bookCategoryObject,"editEBookObjectData":editEBookObject}
    return render(request,"online/onlineEditEBook.html",context)


@unauthenticated_user
@admin_only
def SoftDeleteEBookView(request): 
    try:
        SoftDeleteEBookObject = get_object_or_404(EBook,pk=request.GET.get('eBook_id'))
        SoftDeleteEBookObject.status = not SoftDeleteEBookObject.status
        SoftDeleteEBookObject.save()
        return redirect('onlineView_url')

    except Exception as e:
        print(e)
        

@unauthenticated_user
@allowed_users(allowed_roles=['stuff','student'])
def AllEBooksView(request):
    
    categotyIdObject = Category.objects.all()
    
    try:
        if 'q' in request.GET:
            q = request.GET['q']
            #data = Book.objects.filter(title__icontains=q)
            multiple_data = Q(Q(title__icontains=q) |             
                            Q(author__icontains=q) | 
                            Q(publisher__icontains=q) | 
                            Q(yearOfPublication__icontains=q) | 
                            Q(categoryId__id__icontains=q))
            
            ebookObject = EBook.objects.filter(multiple_data,status=True)
        
        else:
            ebookObject = EBook.objects.filter(status=True)
        
    except FileNotFoundError:
        raise Http404
    
    context = {'ebook':ebookObject,'categoty_id':categotyIdObject}
    return render(request,'online/onlineAlleBooks.html', context)


@unauthenticated_user
@admin_only
def CreateeBookView(request):
    bookCategoryObject = Category.objects.all()
    
    if request.method == "POST" and 'coverPageeBook' in request.FILES and 'eBook' in request.FILES:
        categoryId = request.POST.get('categoryId')
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        yearOfPublication = request.POST.get('yearOfPublication')
        
        coverPagee = request.FILES
        coverPageeBook = coverPagee['coverPageeBook']
        eBookFile = request.FILES
        eBook = eBookFile['eBook']
        
        try:
            eBookCreateObject = EBook.objects.create(
                createdBy_id=request.user.id,
                categoryId_id=categoryId,
                title=title,
                author=author,
                publisher=publisher,
                yearOfPublication=yearOfPublication,
                coverPageeBook=coverPageeBook,
                eBookFile=eBook
            )
            
            eBookCreateObject.save()
            messages.info(request,'sucessfully, Created')
            return redirect('onlineView_url')
        
        except FileNotFoundError:
            raise Http404
    
    context = {"categoty_id":bookCategoryObject}
    return render(request,"online/createebook.html",context)


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def ReadeBookView(request, pk):
    try:
        eBookObject = EBook.objects.get(id=pk)
        
        with open(str(eBookObject.eBookFile.path), 'rb') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="eBook.pdf"'
            return response
        pdf.closed
    
    except FileNotFoundError:
        raise Http404


@unauthenticated_user
@allowed_users(allowed_roles=['stuff','student'])
def VieweBookView(request, pk):
    try:
        VieweBookObject = EBook.objects.get(id=pk)
        readeBookObject = ReadeBook.objects.filter(bookId=pk).first()
        
        if readeBookObject:
            readeBookObject.readNo += 1
            readeBookObject.save()
        else:
            saveReadeBookData = ReadeBook.objects.create(
                bookId_id=pk,
            )
            saveReadeBookData.save()
        
        with open(str(VieweBookObject.eBookFile.path), 'rb') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="eBook.pdf"'
            return response
        pdf.closed
    
    except FileNotFoundError:
        raise Http404


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def ReadeBookStatusView(request):
    readeBookObject = ReadeBook.objects.filter(status=True).order_by("-readNo")
    
    context = {"readeBookData":readeBookObject}
    return render(request,'online/readeBookStatus.html', context)