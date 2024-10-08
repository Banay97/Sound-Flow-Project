from django.shortcuts import render, redirect
from .models import User, Session
from django.contrib import messages
import bcrypt

# Create your views here.
#-- Sign Up render page
def sign_up(request):
    return render(request, 'SignUpPage.html')

#--Sign in render page
def sign_in(request):
    return render(request, 'SignInPage.html')

#--Create account function 
def create_account(request):
    if request.method =='POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='signup')
            return redirect('sign_up')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            
            user = User.objects.create(first_name = first_name, last_name=last_name, email = email, password = hashed_password)
            request.session['user_id'] = user.id
            return redirect('home_page')
    return redirect('sign_up')

#-- Enter account function 
def enter_account(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email =email).first()
        
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['user_id'] = user.id
            messages.success(request, 'You successfully Sign in')
            return redirect('home_page')
        else:
            messages.error(request, "Invalid Email or Password!", extra_tags='signin')
            redirect('sign_in')

    return redirect('sign_in')

#--Home Page render pager
def home_page(request):
    user_id = request.session.get('user_id')
    user =User.objects.get(id=user_id)
    sessions = Session.objects.all()
    return render(request, 'HomePage.html', {'user':user , 'sessions':sessions} )

def sign_out(request):
    if request.method == 'POST':
        request.session.flush()
        return redirect('sign_in')
    return render(request, 'SignInPage.html')

#-- Book Session render page
def book_session(request):
    return render(request, 'BookSession.html')

# -- Create Session function 
def create_session(request):
    if request.method == 'POST':
        user = None
        errors = Session.objects.session_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('book_session')
        else:
            artist_name = request.POST['artist_name']
            session_date = request.POST['session_date']
            duration = request.POST['duration']
            genre = request.POST['genre']
            notes = request.POST['notes']
            
            if 'user_id' not in request.session:
                messages.error(request, "You must be logged in to book a session")
                return redirect('sign_in')
            user = User.objects.get(id = request.session['user_id'])
            session = Session.objects.create(artist_name=artist_name, session_date=session_date,duration=duration,genre=genre, notes=notes, created_by = user)
            session.save()
            messages.success(request, 'Session created successfully!')
            return redirect('home_page')
    user = User.objects.get(id = request.session['user_id'])
    return render(request, 'bookSession.html', {'session': {}, 'user':user})

#-- Session Details render page
def session_details_page(request, session_id):
    user_id = request.session.get('user_id')
    user =User.objects.get(id=user_id)
    session = Session.objects.filter(id=session_id).first()
    return render(request, 'SessionDetailsPage.html', {'user':user, 'session':session} )

def update_session(request, session_id):
    session = Session . objects.filter(id= session_id).first()
    if not session:
        messages.error(request, 'Session not found.')
        return redirect('home_page')
    user =None
    
    if request.method =='POST':
        if 'user_id' not in request.session:
            messages.error(request, 'You must be logged in to update a session.')
            return redirect('sign_in')
        
        user = User.objects.get(id= request.session['user_id'])
        
        errors = Session.objects.session_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, 'UpdateSession.html', {'user': user, 'session': session})
        
        session.artist_name = request.POST['artist_name']
        session.session_date = request.POST['session_date']
        session.duration = request.POST['duration']
        session.genre = request.POST['genre']
        session.notes = request.POST['notes']
        
        session.save()
        messages.success(request, "Session updated successfully")
        return render(request, 'SessionDetailsPage.html', {'user': user, 'session': session})
    
    user = User.objects.get(id= request.session['user_id'])
    return render(request, 'UpdateSession.html', {'user':user , 'session':session})
        
def delete_session(request, session_id):
    if request.method == 'POST':
        session = Session.objects.filter(id= session_id).first()
        session.delete()
        messages.success(request, "Session deleted successfully")
        return redirect('home_page')
    return redirect('home_page')


    
                
        
        
                
                
            

