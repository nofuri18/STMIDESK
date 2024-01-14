from django.shortcuts import render, redirect
# Create your views here.
# views.py

# Views Register
from .forms import UserAdminCreationForm
def register(request):
    form = UserAdminCreationForm()
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Tambahkan role yang dipilih oleh pengguna
            role = form.cleaned_data['role']
            if role:
                user.roles.add(role)

            return redirect('login')

    return render(request, 'register.html', {'form': form})

# Views Login
from django.contrib.auth import authenticate, login
from .forms import LoginForm
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None and user.check_password(password):
                login(request, user)
                return redirect('test')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def test_view(request):
    return render(request, 'test.html')
