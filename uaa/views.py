import email
from multiprocessing import context
from django.shortcuts import render,redirect,redirect,get_object_or_404
from django.urls import path
from . models import REgisterdMember,User,DailyTip
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import Group
from .decorators import admin_only, allowed_users, manager_only, unauthenticated_user
from book.models import RequestedBook,Book,MaximumBookLimit
from datetime import time

# Create your views here.
def LoginView(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        Password = request.POST.get('password')
        
        try: 
            user_obj = User.objects.filter(email=email).first()
            if user_obj is None:
                messages.info(request,'Email not found')
                return redirect('login_url')
            
            user = authenticate(request, email=email, password=Password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    messages.success(request,'your now logged in !!')
                    return redirect('dashboard_url')
                
                else:
                    messages.success(request,'your account is blocked')
                    return redirect('login_url')
                
            else:
                messages.warning(request,"Invalid username or password")
                return redirect('login_url')
            
        except Exception as e:
            print(e)
    
    context = {}
    return render(request,"login.html",context)


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def RegistrationNoView(request):
    registationNumberObject = REgisterdMember.objects.all()
    
    context = {"registationNumberData":registationNumberObject}
    return render(request,"auth/registrationNo.html", context)


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def AddRegNoView(request):
    if request.method == "POST":
        RegNo = request.POST.get('RegNumber')
        
        try:
            createRegNoObject = REgisterdMember.objects.create(regNo=RegNo)
            createRegNoObject.save()
            
            messages.success(request,'reg-Number, added')
            return redirect('registrationNoView_url')

        except Exception as e:
            print(e) 
        
    context = {}
    return render(request,"auth/addRegNo.html", context)


def RegisterView(request):
    
    if request.method == 'POST':
        regNo = request.POST.get('regNo')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        try: 
            if not REgisterdMember.objects.filter(regNo=regNo).first():
                messages.info(request,'Registration Number Doest Not Exist')
                return redirect('/register')
                
            if User.objects.filter(username=regNo).first():
                messages.info(request,'Username is already taken')
                return redirect('/register')
        
            if User.objects.filter(email=email).first():
                messages.info(request,'Email is already taken')
                return redirect('/register')
            
            if password != password1:
                messages.info(request,'password does not match')
                return redirect('/register')
            
            if len(password) < 8:
                messages.info(request, 'password, 8 mixed characters required')
                return redirect('/register')
                
            else:
                user_obj = User.objects.create_user(username=regNo, email=email,password=password)
                user_obj.save()
                
                grp = Group.objects.get(name="student")
                user= User.objects.get(username=regNo)
                user.groups.add(grp)

                return redirect('login_url')
            
        except Exception as e:
            print(e)
    
    context = {}
    return render(request,"auth/register.html",context)

@unauthenticated_user
@admin_only
def AddUserView(request):
    
    if request.method == 'POST':
        regNo = request.POST.get('regNo')
        email = request.POST.get('email')
        password = str(regNo)+'tipm'
        
        try: 
            if not REgisterdMember.objects.filter(regNo=regNo).first():
                messages.info(request,'Registration Number Doest Not Exist')
                return redirect('/addUser')
                
            if User.objects.filter(username=regNo).first():
                messages.info(request,'Username is already taken')
                return redirect('/addUser')
        
            if User.objects.filter(email=email).first():
                messages.info(request,'Email is already taken')
                return redirect('/addUser')
                
            else:
                user_obj = User.objects.create_user(username=regNo, email=email,password=password)
                user_obj.save()
                
                grp = Group.objects.get(name="stuff")
                user= User.objects.get(username=regNo)
                user.groups.add(grp)
                # messages.info(request,'created succesfully')

                return redirect('allUsers_url')
            
        except Exception as e:
            print(e)
    
    context = {}
    return render(request,"auth/addUser.html",context)

@unauthenticated_user
@admin_only
def UpdateUserView(request,pk):
    updateUserObject = User.objects.get(id=pk)
    
    if request.method == 'POST':
        email = request.POST.get('email')
    
        try:
            if User.objects.filter(email=email).first():
                messages.info(request,'Email is already taken')
                return redirect('allUsers_url')
                    
            updateUserObject.email = email
            updateUserObject.save()
            
            messages.info(request,'updated succesfully')
            return redirect('allUsers_url')
    
        except Exception as e:
            print(e) 
    
    context = {"updateUserData":updateUserObject}
    return render(request,"auth/updateUser.html",context)


@unauthenticated_user
def DashboardView(request):
    
    try:
        DailyTipObject = DailyTip.objects.all().order_by('-createdAt')[:5]
        requestedBookNumberObject = RequestedBook.objects.filter(status=True,isPending=True).count()
        takenBookNumberObject = RequestedBook.objects.filter(status=True,isTaken=True).count()
        bookHavingNumberObject = RequestedBook.objects.filter(userId=request.user.id,status=True,isTaken=True).count()
        totalBookObject = Book.objects.all().count()
        totalAvailableBookObject = str(totalBookObject-takenBookNumberObject)
        
        mmn = MaximumBookLimit.objects.all().first()
        dysn = int(mmn.days)
        
        notReturnedBookObject = RequestedBook.objects.filter(status=True,isTaken=True)
        NotReturnedOnTimeBookList = 0
        for n in notReturnedBookObject:
            if n.noDays > dysn:
                NotReturnedOnTimeBookList += 1
            else:
                pass
        
        totalNotificationsObject = str(requestedBookNumberObject + takenBookNumberObject)
        toDayTimeObject = time
    
    except Exception as e:
        print(e) 
    
    context = {"DailyTipData":DailyTipObject,
               "requestedBookNumber":requestedBookNumberObject,
               "toDay":toDayTimeObject,
               "bookHavingNumber":bookHavingNumberObject,
               "takenBookNumber":takenBookNumberObject,
               "totalNotifications":totalNotificationsObject,
               "totalBook":totalBookObject,
               "NotReturnedOnTime":NotReturnedOnTimeBookList,
               "totalAvailableBook":totalAvailableBookObject}
    return render(request,"auth/dashboard.html",context)


@unauthenticated_user
def ProfileView(request):
    try:
        myCredentials = User.objects.get(id=request.user.id)
        myRole = request.user.groups.all()[0].name
    
    except Exception as e:
        print(e) 
        
    context = {"myCredential":myCredentials,"my_role":myRole}
    return render(request,"auth/profile.html",context)


@unauthenticated_user
def UpdateProfileView(request):
    
    try:
        updateProfile = User.objects.get(id=request.user.id)
        if request.method == 'POST' and 'Image' in request.FILES:
            FirstName = request.POST.get('FirstName')
            LastName = request.POST.get('LastName')
            PhoneNumber = request.POST.get('PhoneNumber')
            NidaNumber = request.POST.get('NidaNumber')
            profile = request.FILES
            profileImage = profile['Image']
            Bod = request.POST.get('Bod')
            genderValue = request.POST.get('genderValue')
            
        
            if len(FirstName) < 4:
                messages.info(request,'First Name, Is too short')
                return redirect('/profile')
            
            if len(LastName) < 4:
                messages.info(request,'Last Name, Is too short')
                return redirect('/profile')
            
            if len(PhoneNumber) < 10 or len(PhoneNumber) > 10:
                messages.info(request,'Invalid phone number format')
                return redirect('/profile')
        
        
            updateProfile.first_name = FirstName
            updateProfile.last_name = LastName
            updateProfile.phone_number = PhoneNumber
            updateProfile.nida_no = NidaNumber
            updateProfile.dob = Bod
            updateProfile.gender = genderValue
            updateProfile.profileImage = profileImage
            updateProfile.save()
            
            messages.info(request,'Your Profile Is Updated')
            return redirect('/profile')
    
    except Exception as e:
        print(e) 

@unauthenticated_user
def AllUsersView(request):
    allUSerObject = User.objects.filter(is_superuser=False)

    context = {"allUserList":allUSerObject}
    return render(request,"auth/allUsers.html",context)


@unauthenticated_user
def UpdatePasswordView(request):
    userUpdateObject = User.objects.get(id=request.user.id)
    
    if request.method == "POST":
        password = request.POST.get('Password')
        
        try:
            if password is not None:
                userUpdateObject.set_password(password)
                userUpdateObject.save()
                
                messages.info(request,'password, Updated')
                return redirect('dashboard_url')
            
            else:
                messages.info(request,'Error, Occured')
                return redirect('profile_url')
        
        except Exception as e:
            print(e) 
        
    return redirect('profile_url')


@unauthenticated_user
def ForgotPasswordView(request):
    if request.method == "POST":
        email = request.POST.get('Email')
        username = request.POST.get('RegistrationNumber')
        lastName = request.POST.get('LastName')
        password = request.POST.get('Password')
        
        try:
            userObjectPass = User.objects.filter(email=email,username=username,last_name=lastName).first()
            
            if userObjectPass:
                if len(password) >= 8:
                    userObjectPass.set_password(password)
                    userObjectPass.save()
                
                    messages.info(request,'password, set')
                    return redirect('login_url')
                else:
                    messages.info(request,'8 characters, pass-required')
                    return redirect('forgotPasswordView_url')
                
            else:
                messages.info(request,'Wrong credintials || concert librarian')
                return redirect('forgotPasswordView_url')
        
        except Exception as e:
            print(e) 
        
    context = {}
    return render(request,"auth/forgotpassword.html",context)


@unauthenticated_user
@admin_only
def ResetPasswordView(request):
    
    try:
        resetPass = get_object_or_404(User,pk=request.GET.get('user_id'))
        
        regNo = resetPass.username
        password = str(regNo)+'tipm'
        
        resetPass.set_password(password)
        resetPass.save()
        
        messages.info(request,'password, set')
        return redirect('allUsers_url')  

    except Exception as e:
        print(e) 


@unauthenticated_user
@admin_only
def UserStatusView(request):
    
    try:
        userStatusObject = get_object_or_404(User,pk=request.GET.get('userStatus_id'))
        
        userStatusObject.is_active = not userStatusObject.is_active
        userStatusObject.save()
        return redirect('allUsers_url')

    except Exception as e:
        print(e) 

@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def TipButtonView(request):
    
    context = {}
    return render(request, 'auth/addtip.html', context)


@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def TipView(request):
    
    try:
        if request.method == 'POST':
            tip = request.POST.get('Tips')
            
            if tip is not None:
                tipObject = DailyTip.objects.create(content=tip)
                tipObject.save()
                return redirect('dashboard_url')
            
            else:
                return redirect('dashboard_url')
            
        return redirect('dashboard_url')
    
    except Exception as e:
        print(e) 

@unauthenticated_user
@allowed_users(allowed_roles=['manager','admin'])
def ManageTipsView(request):
    tipsObject = DailyTip.objects.filter(status=True)
    
    context = {"tipsObjectData":tipsObject}
    return render(request, 'auth/manage_tips.html', context)

@unauthenticated_user
@admin_only
def DelateTipsView(request, pk):
    try:
        getTipsObject = DailyTip.objects.get(id=pk)
        getTipsObject.delete()
        return redirect('manageTip_url')

    except Exception as e:
        print(e) 

@unauthenticated_user
def LogoutView(request):
    logout(request)
    return redirect('login_url')

#password reset+++++++++
# def Password_reset(request):
#     return render(request, 'foggoten_password.html')


