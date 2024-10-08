from django.urls import path
from .  import views

urlpatterns = [
    path('', views.sign_up, name= 'sign_up'),
    path('sign-in', views.sign_in , name='sign_in'),
    path('home-page', views.home_page, name= 'home_page'),
    path('create-account', views.create_account, name ='create_account'),
    path('enter-account', views.enter_account, name='enter_account'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('book-session', views.book_session , name ='book_session'),
    path('create-session', views.create_session, name='create_session'),
    path('session-details-page/<int:session_id>', views.session_details_page, name='session_details_page'),
    path('update-session/<int:session_id>', views.update_session, name= 'update_session' ),
    path('delete-session/<int:session_id>', views.delete_session , name='delete_session')
    
    
    
]
