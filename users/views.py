from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.views.generic import View, TemplateView
from .models import CustomUser


### https://stackoverflow.com/questions/34035244/creating-login-and-logout-class-based-views-in-django-1-8


class LoginView(View):
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/login/")

        return render(request, "/")

    def get(self, request):
        return render(request, "login.html", {"form": CustomUserCreationForm()})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/login/")


# Sign Up View
class SignUpView(FormView):
    template_name = "signup.html"
    success_url = reverse_lazy("login")

    def get(self, request):
        # form = CustomUserCreationForm()
        return render(request, self.template_name, {"form": CustomUserCreationForm()})

    def post(self, request):
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                # user = form.save()
                # username = form.cleaned_data.get("username")
                data = form.cleaned_data
                user = CustomUser.objects.create_user(
                    username=data["username"], password=data["password"]
                )
                login(request, user)
                return HttpResponseRedirect("/login/")

            else:
                for msg in form.error_messages:
                    print(form.error_messages[msg])

                return render(
                    request=request,
                    template_name="signup.html",
                    context={"form": form},
                )
