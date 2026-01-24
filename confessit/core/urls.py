from django.urls import path
from core import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/<int:pk>/',views.ProfileView.as_view(),name='profile'),
    path('',views.HomePage.as_view(),name='home'),
    path('confessions/new/',views.MakeConfession.as_view(),name='confession_create'),
    path('confession/<int:pk>/',views.ConfessionDetails.as_view(),name='confession_detail'),
    path('confession/<int:confession_id>/like/',views.like_dislike_post,name='confession_like'),
    path('confession/<int:confession_id>/report/',views.report,name='confession_report'),
    path('comment/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),
    path('my-confessions/',views.MyConfessions.as_view(),name='my_confessions'),
    path('confession/<int:confess_id>/delete/',views.delete_confession,name='confession_delete'),
    path('search_results/',views.search_views,name='search'),
    path('change-profile/',views.UpdateProfileView.as_view(),name='change_profile'),
    path('liked-confessions/',views.Liked_Confessions.as_view(),name='liked_confessions'),
    path('confessions/', views.AllConfessions.as_view(), name='all_confessions'),
    path('ads.txt', views.ads_txt, name='ads_txt'),
    path('terms/', views.terms_view, name='terms'),
    
]
