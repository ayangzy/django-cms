
from pickle import NONE
from unicodedata import name
from django.shortcuts import render, redirect
from account.models import *
from account.forms import OrderForm, CreateUserForm, CustomerForm
from account.filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from account.decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
@unauthenticated_user
def register(request):
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
               
                messages.success(request, f'Account was successfully created for {username}' )
                return redirect('login_page')
        context = {
            'form': form
        }
        return render(request, "accounts/register.html", context)

@unauthenticated_user
def loginPage(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
        
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.warning(request, 'Invalid credentials')
        context = {}
        return render(request, "accounts/login.html", context)

def logout_user(request):
    logout(request)
    return redirect('login_page')

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    print('ORDERS:', orders)
    
    context = {'orders':orders, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending}
    
    return render(request, "accounts/user.html", context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('account_settings')
    context = {
        'form': form
    }
    return render(request, "accounts/account_settings.html", context)


@login_required(login_url='login_page')
@admin_only
def index(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'customers': customers,
        'orders': orders,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, "accounts/dashboard.html", context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", { 'products': products})

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    orders = customer.order_set.all()
    customer_total_order = orders.count()
    my_filter  = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'customer_total_order': customer_total_order,
        'my_filter': my_filter
    }
    
    return render(request, "accounts/customer.html", context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def create_order(request):
    form = OrderForm()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {
        'form':form
    }
    return render(request, "accounts/order_form.html", context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {
        'form':form
    }
    return render(request, "accounts/order_form.html", context)
 
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])   
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect("/")
    context = {
        'order': order
    }
    return render(request, "accounts/delete.html", context)


    