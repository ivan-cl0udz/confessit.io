from django.shortcuts import render, get_object_or_404
from django.db import models
from django.views.decorators.cache import cache_page
from django.views.generic import ListView,CreateView,DetailView,View,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from .models import Comment,Confession,Profile
from .forms import ConfessionForm, RegisterForm, ProfileUpdateForm,CommentForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import  Http404
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
@cache_page(30)
class HomePage(ListView):
    model = Confession
    template_name = 'core/home.html'
    def get_queryset(self):
        base_qs = (
            Confession.objects.filter(
                created_at__gt=(timezone.now() - timedelta(days=3))
            )
            .select_related("user")
            .prefetch_related("comments", "favourites")
        )
        if self.request.user.is_authenticated:
            queryset = base_qs.filter(
                models.Q(is_approved=True) | models.Q(user=self.request.user)
            )
        else:
            queryset = base_qs.filter(is_approved=True)
        return queryset.only('title', 'description', 'created_at', 'user', 'is_approved')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['unapproved_confessions'] = Confession.objects.filter(
                user=self.request.user,
                is_approved=False,
            )
            context['liked_confession_ids'] = list(
                self.request.user.favourite_confessions.values_list('id', flat=True)
            )
        else:
            context['unapproved_confessions'] = Confession.objects.none()
            context['liked_confession_ids'] = []
        return context
class MakeConfession(LoginRequiredMixin, CreateView):
    model = Confession
    form_class = ConfessionForm
    login_url = 'login'
    template_name = 'core/create_confession.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
@cache_page(30)
class ConfessionDetails(DetailView):
    model = Confession
    template_name = 'core/confession_detail.html'
    context_object_name = 'post_object'
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("user")
            .prefetch_related("comments", "comments__user", "favourites")
        )
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            self.object.comments.add(comment)
            return redirect(self.object.get_absolute_url())
        messages.error(request, 'Form data is incorrect')
        return self.render_to_response(self.get_context_data(comment_form=form))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = kwargs.get('comment_form', CommentForm())
        context['comments'] = self.object.comments.all()
        context['comment_count'] = context['comments'].count()
        context['favourite_count'] = self.object.favourites.count()
        context['is_favourited'] = (
            self.request.user.is_authenticated
            and self.object.favourites.filter(id=self.request.user.id).exists()
        )
        return context
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'core/register.html'
    model = User
    success_url = '/login'
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.ERROR(request,'Username or Password is invalid!')
    else:
        form = AuthenticationForm()
    return render(request,'core/login.html',context={'form':form})
@cache_page(30)
class MyConfessions(LoginRequiredMixin, ListView):
    model = Confession
    template_name = 'core/my_confession.html'
    def get_queryset(self):
        queryset = (
            Confession.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related("comments", "favourites")
            .only('title', 'created_at', 'user')
        )
        return queryset
    login_url = 'login'
def delete_confession(request,confess_id):
    confess_obj = Confession.objects.get(id = confess_id)
    if confess_obj:
        confess_obj.delete()
        return redirect('my_confessions')
    else:
        raise Http404
    

def logout_view(request):
    logout(request)
    return redirect('home')

@cache_page(30)
class ProfileView(DetailView):
    model = User
    template_name = 'core/profile.html'
    context_object_name = 'user'

    def get_queryset(self):
        return super().get_queryset().select_related("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.object)
        context['profile'] = profile
        context['is_owner'] = self.request.user.is_authenticated and self.request.user == self.object
        context['confession_count'] = Confession.objects.filter(user=self.object).count()
        return context

def search_views(request):
    query = request.GET.get('q')
    filtering = Confession.objects.filter(title__icontains=query,is_approved=True).only('title','description','created_at','user')
    
    return render(request, 'core/search_results.html', context={'filtered_products': filtering})

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'core/change_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})
@login_required(login_url='login')
def add_comment_to_post(request,confession_id):
    post_object = Confession.objects.get_or_create(id=confession_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            post_object.comments.add(comment)

    
@login_required(login_url='login')
def like_dislike_post(request, confession_id):
    confession = get_object_or_404(Confession, id=confession_id)
    if confession.favourites.filter(id=request.user.id).exists():
        confession.favourites.remove(request.user)
    else:
        confession.favourites.add(request.user)
    is_favourited = confession.favourites.filter(id=request.user.id).exists()
    if request.headers.get('HX-Request') == 'true':
        return render(
            request,
            'core/partials/like_button.html',
            {'confession': confession, 'is_favourited': is_favourited},
        )
    return redirect(request.META.get('HTTP_REFERER', confession.get_absolute_url()))
