from django.http import HttpResponse
from django.shortcuts import redirect

def regauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admincontrol')
            # if request.user.groups.all()[0].name == "superadmin" or request.user.groups.all()[0].name == "admin":
            #     return redirect('controlhome')
            if request.user.groups.all()[0].name == "admin":
                return redirect('/adminc/')

            if request.user.groups.all()[0].name == "planshet":
                return redirect('planshet')

            if request.user.groups.all()[0].name == "navbat":
                return redirect('nazariynavbat')
            # return redirect('homepage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("login")
    return wrapper_func


def superuserallow(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            return redirect('user_logout')
        else:
            return redirect('homepage')
    return wrapper_func

def adminallow(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if the user has any groups
            user_groups = request.user.groups.all()
            if user_groups.exists() and user_groups[0].name == "admin":
                return view_func(request, *args, **kwargs)
            return redirect('logout')  # Or another appropriate redirect based on your application logic
        else:
            return redirect('homepage')
    return wrapper_func
# def adminallow(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             if request.user.groups.all()[0].name == "admin":
#                 return view_func(request, *args, **kwargs)
#             return redirect('logout')
#         else:
#             return redirect('homepage')
#     return wrapper_func
# def adminallow(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             if request.user.groups.all()[0].name == "admin" or request.user.is_superuser or request.user.groups.all()[0].name == "manager":
#                 return view_func(request, *args, **kwargs)
#             return redirect('logout')
#         else:
#             return redirect('homepage')
#     return wrapper_func
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # print("working", allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not allowed enter this site")
        return wrapper_func
    return decorator

# def student_only(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         group = None
#         if request.user.groups.exists():
#             group = request.user.groups.all()[0].name
#         if group == "student":
#             return view_func(request, *args, **kwargs)
#         if group == "teacher":
#             return redirect("homepage")
#     return wrapper_func
