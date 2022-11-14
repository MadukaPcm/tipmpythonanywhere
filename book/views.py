from multiprocessing import context
from urllib import request
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from . models import Book,RequestedBook,Category,MaximumBookLimit
from uaa.decorators import admin_only, allowed_users, manager_only, unauthenticated_user
from uaa.models import User
from datetime import date
from datetime import datetime

# Create your views here.  @allowed_users(allowed_roles=['stuff','student'])
@unauthenticated_user
@allowed_users(allowed_roles=['stuff','student'])
def BookView(request):
    categotyIdObject = Category.objects.all()
    
    try:
        if 'q' in request.GET:
            q = request.GET['q']
            #data = Book.objects.filter(title__icontains=q)
            multiple_data = Q(Q(bookNumber__icontains=q) |
                            Q(title__icontains=q) |             
                            Q(author__icontains=q) | 
                            Q(isbn__icontains=q) | 
                            Q(publisher__icontains=q) | 
                            Q(placeOfPublication__icontains=q) | 
                            Q(yearOfPublication__icontains=q) | 
                            Q(description__icontains=q) | 
                            Q(categoryId__id__icontains=q))
            
            bookObject = Book.objects.filter(multiple_data,status=True)
        
        else:
            bookObject = Book.objects.filter(status=True)
        
    except Exception as e:
        print(e) 
    
    context = {'book':bookObject,'categoty_id':categotyIdObject}
    return render(request,'books/allBooks.html', context)

@unauthenticated_user
@admin_only
def CreateBookView(request):
    bookCategoryObject = Category.objects.all()
    
    if request.method == "POST" and 'coverPageImage' in request.FILES:
        categoryId = request.POST.get('categoryId')
        bookNumber = request.POST.get('bookNumber')
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        publisher = request.POST.get('publisher')
        placeOfPublication = request.POST.get('placeOfPublication')
        yearOfPublication = request.POST.get('yearOfPublication')
        coverPage = request.FILES
        coverPageImage = coverPage['coverPageImage']
        description = request.POST.get('description')
    
        try:
            bookCreateObject = Book.objects.create(
                            categoryId_id=categoryId,
                            createdBy_id=request.user.id,
                            bookNumber=bookNumber,
                            title=title,
                            author=author,
                            isbn=isbn,
                            publisher=publisher,
                            placeOfPublication=placeOfPublication,
                            yearOfPublication=yearOfPublication,
                            coverPageImage=coverPageImage,
                            description=description
                        )
            bookCreateObject.save()
            print(coverPageImage)
            messages.info(request,'sucessfully, Created')
            return redirect('manageBookView_url')
    
        except Exception as e:
            print(e) 
    
    context = {"categoty_id":bookCategoryObject}
    return render(request,'books/createBook.html', context)


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def ManageBookView(request):
    bookObject = Book.objects.filter(status=True)

    context = {"bookObjectData":bookObject}
    return render(request,'books/manageBook.html', context) 


@unauthenticated_user
def ActionViewBookView(request,pk):
    viewBookObject = Book.objects.get(id=pk)

    context = {"ViewbookData":viewBookObject}
    return render(request,'books/actionsViewBook.html', context)

@unauthenticated_user
@admin_only
def ActionUpdateBookView(request,pk):
    bookCategoryObject = Category.objects.all()
    updateBookObject = Book.objects.filter(id=pk).first()
    
    if request.method == "POST" and 'coverPageImage' in request.FILES:
        categoryId = request.POST.get('categoryId')
        bookNumber = request.POST.get('bookNumber')
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        publisher = request.POST.get('publisher')
        placeOfPublication = request.POST.get('placeOfPublication')
        yearOfPublication = request.POST.get('yearOfPublication')
        coverPage = request.FILES
        CoverPageImage = coverPage['coverPageImage']
        description = request.POST.get('description')
        
        try:
            updateBookObject.categoryId_id = categoryId
            updateBookObject.createdBy_id=request.user.id 
            updateBookObject.bookNumber = bookNumber
            updateBookObject.title = title
            updateBookObject.author = author
            updateBookObject.isbn = isbn
            updateBookObject.publisher = publisher
            updateBookObject.placeOfPublication = placeOfPublication
            updateBookObject.yearOfPublication = yearOfPublication
            updateBookObject.coverPageImage = CoverPageImage
            updateBookObject.description = description
            updateBookObject.save()
            
            messages.info(request,'sucessfully, Updated')
            return redirect('manageBookView_url')
    
        except Exception as e:
            print(e)

    context = {"categoty_id":bookCategoryObject,"updateBookObjectData":updateBookObject}
    return render(request,'books/actionsUpdateBook.html', context)

@unauthenticated_user
@admin_only
def ActionDeleteBookView(request):
    try:
        deleteBook = get_object_or_404(Book,pk=request.GET.get('delete_id'))
        deleteBook.status = not deleteBook.status
        deleteBook.save()
        return redirect('manageBookView_url')

    except Exception as e:
        print(e)


@unauthenticated_user
def RequestBookView(request,pk):
    getBookObject = Book.objects.get(id=pk)
    
    context = {"getBook":getBookObject}        
    return render(request,'books/requestBook.html',context)


@unauthenticated_user
@allowed_users(allowed_roles=['stuff','student'])
def RequestingBookView(request):
    
    try:
        userGroup = request.user.groups.all()[0].name
        blockStatus = RequestedBook.objects.filter(userId=request.user.id,status=False).values()
        userBookNumberRequest = RequestedBook.objects.filter(userId=request.user.id,isTaken=True).count()
        requestStatus = RequestedBook.objects.filter(userId=request.user.id,isPending=True).values()
        reportStatus = RequestedBook.objects.filter(userId=request.user.id,isApproved=True).values()
        myDate = request.user.dob
        # tookStatus = RequestedBook.objects.filter(userId=request.user.id,isTaken=True).values()
        mn = MaximumBookLimit.objects.all().first()
        stfn = str(mn.stuff)
        stdn = str(mn.student)
        dysn = int(mn.days)
        
        if request.method == "POST":
            bookId = request.POST.get('bookId')
            issueDate = request.POST.get('issueDate')
            dueDate = request.POST.get('dueDate')
            
            dt1 = datetime.strptime(issueDate, "%Y-%m-%d")
            dt2 = datetime.strptime(dueDate, "%Y-%m-%d")
            
            dayNo = (dt2 - dt1).days
            
            if not myDate:
                messages.info(request,'update your profile')
                return redirect('/profile')
            
            if blockStatus:
                messages.info(request,"Your Request Was Blocked")
                return redirect('Book_url')
            
            elif requestStatus:
                messages.info(request,"having pending request")
                return redirect('Book_url')
            
            elif reportStatus:
                messages.info(request,"were approved to take a book,")
                return redirect('Book_url')
            
            elif RequestedBook.objects.filter(bookId=bookId,isREturned=False).values():
                messages.info(request,"taken or ready requested")
                return redirect('Book_url')
            
        
            elif str(issueDate) < str(date.today()):
                messages.info(request,"Invalid issue date")
                return redirect('Book_url')
            
            elif dayNo > dysn:
                messages.info(request,"Date, out of range")
                return redirect('Book_url')
            
            else:
                if userGroup == "stuff":
                    if str(userBookNumberRequest) < stfn:
                        saveBookRequestObject = RequestedBook.objects.create(
                            userId_id=request.user.id,
                            bookId_id=bookId,
                            issueDate=issueDate,
                            dueDate=dueDate
                        )
                        saveBookRequestObject.save()
                        messages.info(request,'request sent')
                        return redirect('Book_url')
                        
                    elif str(userBookNumberRequest) == stfn:
                        messages.info(request,'Reached Max No,')
                        return redirect('Book_url') 
                    
                    else:
                        messages.info(request,"you can't request at all,")
                        return redirect('Book_url') 
                    
                elif userGroup == "student":
                    if str(userBookNumberRequest) < stdn:
                        saveBookRequestObject = RequestedBook.objects.create(
                        userId_id=request.user.id,
                        bookId_id=bookId,
                        issueDate=issueDate,
                        dueDate=dueDate
                        )
                        saveBookRequestObject.save()
                        
                        messages.info(request,'request sent')
                        return redirect('Book_url')
                        
                    elif str(userBookNumberRequest) == stdn:
                        messages.info(request,'Reached Max No,')
                        return redirect('Book_url') 
                    
                    else:
                        messages.info(request,"you can't request at all")
                        return redirect('Book_url') 
                
                else:
                    messages.info(request,"Errors occured")
                    return redirect('Book_url')

        return redirect('Book_url')

    except Exception as e:
        print(e) 


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def IssuedBookView(request):
    
    try:
        pendingApprovdBookObject = RequestedBook.objects.filter(
            Q(status=True),
            Q(isPending=True) | Q(isApproved=True)
        )
    
    except Exception as e:
        print(e) 
    
    context = {"pendingApprovdBook":pendingApprovdBookObject}
    return render(request,'books/issuedBook.html',context)


@unauthenticated_user
@admin_only
def VerifyPedingView(request):
    
    try:
        verifyRequest = get_object_or_404(RequestedBook,pk=request.GET.get('verify_id'))
        verifyRequest.isPending = not verifyRequest.isPending
        verifyRequest.isApproved = not verifyRequest.isApproved
        verifyRequest.save()
        return redirect('issuedBookView_url')

    except Exception as e:
        print(e)
    

@unauthenticated_user
@admin_only
def ApproveVerifiedView(request):
    
    try:
        approveRequest = get_object_or_404(RequestedBook,pk=request.GET.get('approve_id'))
        approveRequest.isApproved = not approveRequest.isApproved
        approveRequest.isTaken = not approveRequest.isTaken 
        approveRequest.save()
        return redirect('issuedBookView_url')

    except Exception as e:
        print(e) 


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def BorrowedBookView(request):
    
    try:
        borrowedBookObject = RequestedBook.objects.filter(status=True,isTaken=True)
        mnn = MaximumBookLimit.objects.all().first()
        dysn = int(mnn.days)
        
        BorrowedBookList = []
        for nnn in borrowedBookObject:
            if nnn.noDays <= dysn:
                BorrowedBookList.append(nnn)
            else:
                pass
        
    except Exception as e:
        print(e) 
    
    context = {"borrowedBookL":BorrowedBookList}
    return render(request,'books/BorrowedBookOnTime.html',context)


@unauthenticated_user
@admin_only
def GetBorrowedBookView(request,pk):
    getBorrowedBookObject = RequestedBook.objects.get(id=pk)
    
    context = {"getBorrowedBook":getBorrowedBookObject}
    return render(request,'books/getBorrowedBookOnTime.html',context)


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def ReturnedBookView(request):
    returnedBookObject = RequestedBook.objects.filter(status=True,isREturned=True)
    
    context = {"returnedBook":returnedBookObject}
    return render(request,'books/returnedBook.html',context)


@unauthenticated_user
@admin_only
def GetReturnedBookView(request,pk):
    getReturnedBookObject = RequestedBook.objects.get(id=pk)
    
    context = {"getReturnedBook":getReturnedBookObject}
    return render(request,'books/getReturnedBook.html',context)


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def NotReturnedBookView(request):
    
    try:
        notReturnedBookObject = RequestedBook.objects.filter(status=True,isTaken=True)
        m = MaximumBookLimit.objects.all().first()
        dysn = int(m.days)
        
        NotReturnedOnTimeBookList = []
        for nn in notReturnedBookObject:
            if nn.noDays > dysn:
                NotReturnedOnTimeBookList.append(nn)
            else:
                pass
        
    except Exception as e:
        print(e) 
    
    context = {"notReturnedBook":NotReturnedOnTimeBookList}
    return render(request,'books/notReturnedBook.html',context)


@unauthenticated_user
@admin_only
def GetNotReturnedBookView(request,pk):
    getNotReturnedBookObject = RequestedBook.objects.get(id=pk)
    
    context = {"getNotReturnedBook":getNotReturnedBookObject}
    return render(request,'books/getNotReturnedBook.html',context)


@unauthenticated_user
@allowed_users(allowed_roles=['admin'])
def ApproveReturnView(request):
    
    try:
        approveReturnObject = get_object_or_404(RequestedBook,pk=request.GET.get('return_id'))
        approveReturnObject.isTaken = not approveReturnObject.isTaken
        approveReturnObject.isREturned = not approveReturnObject.isREturned 
        approveReturnObject.save()
        return redirect('returnedBookView_url')

    except Exception as e:
        print(e)

#Views about book status taken by a user specifically:
@unauthenticated_user
@allowed_users(allowed_roles=['stuff','student'])
def BooksPendingView(request):
    
    try:
        booksPendingObject = RequestedBook.objects.filter(
            status=True,
            userId=request.user.id,
            isPending=True
        )
    
    except Exception as e:
        print(e)
    
    context = {"booksPendingData":booksPendingObject}
    return render(request,'books/booksPending.html',context)

@unauthenticated_user
@allowed_users(allowed_roles=['stuff','student'])
def BooksApprovedView(request):
    
    try:
        booksApprovedObject = RequestedBook.objects.filter(
            status=True,
            userId=request.user.id,
            isApproved=True
        )
    
    except Exception as e:
        print(e) 
    
    context = {"booksApprovedData":booksApprovedObject}
    return render(request,'books/booksApproved.html',context)

@unauthenticated_user
@allowed_users(allowed_roles=['stuff','student'])
def BooksITookView(request):
    
    try:
        booksITookViewObject = RequestedBook.objects.filter(
            status=True,
            userId=request.user.id,
            isTaken=True
        )
    
    except Exception as e:
        print(e) 
    
    context = {"booksITookData":booksITookViewObject}
    return render(request,'books/booksITook.html',context)


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def CategoryBookView(request):
    CategoryBookViewObject = Category.objects.all()
    
    context = {"categoryBook":CategoryBookViewObject}
    return render(request,'books/manageBookCategory.html',context)


@unauthenticated_user
@admin_only
def CreateCategoryBookView(request):
    if request.method == "POST":
        category = request.POST.get('Category')
        
        try:
            if Category != "":
                createCategory = Category(
                    categoryName=category,
                    createdBy_id=request.user.id,
                    
                )
                createCategory.save()
                messages.info(request,'Category added,')
                return redirect('categoryBookView_url')
            
            else:
                messages.info(request,'error occured,')
                return redirect('categoryBookView_url')
        
        except Exception as e:
            print(e) 
    
    context = {}
    return render(request,'books/createCategory.html',context)


@unauthenticated_user
@admin_only
def UpdateCategoryBookView(request,pk):
    updateCategoryObject = Category.objects.get(pk=pk)
    
    if request.method == "POST":
        category = request.POST.get('Category')
        
        try:
            if Category != "":
                updateCategoryObject.categoryName = category
                updateCategoryObject.createdBy_id = request.user.id
                updateCategoryObject.save()
                
                messages.info(request,'Category updated,')
                return redirect('categoryBookView_url')
            
            else:
                messages.info(request,'error occured,')
                return redirect('categoryBookView_url')
        
        except Exception as e:
            print(e) 
    
    context = {"updateCategory":updateCategoryObject}
    return render(request,'books/updateCategory.html',context)


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def MaxBookLimitView(request):
    maxBookLimitObject = MaximumBookLimit.objects.all().first()
    
    context = {"maxBookLimit":maxBookLimitObject}
    return render(request,'books/maxBookLimit.html',context)


@unauthenticated_user
@admin_only
def updateMaxBookLimitView(request,pk):
    maxBookLimitObject = MaximumBookLimit.objects.get(id=pk)
    
    if request.method == "POST":
        
        try:
            Stuff = request.POST.get('stuff')
            Student = request.POST.get('student') 
            Days = request.POST.get('days')
            
            if len(Stuff) == 1 and len(Student) == 1:
                maxBookLimitObject.stuff = Stuff
                maxBookLimitObject.student = Student 
                maxBookLimitObject.days = Days
                maxBookLimitObject.save()
                
                # messages.info(request,'updated,')
                return redirect('maxBookLimitView_url')
            
            else:
                # messages.info(request,'error occured,')
                return redirect('maxBookLimitView_url')
        
        except Exception as e:
            print(e) 
    
    context = {"maxBookLimit":maxBookLimitObject}
    return render(request,'books/updateMaxBookLimit.html',context)
  
        
        
        
        