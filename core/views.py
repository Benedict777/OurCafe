from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError

from .models import MenuItem, Order, Table
from .forms import MenuItemForm, OrderForm, RegisterForm, TableForm


def home(request):
    context = {
        'menu_count': MenuItem.objects.count(),
        'table_count': Table.objects.count(),
        'latest_items': MenuItem.objects.filter(is_available=True)[:3],
    }
    return render(request, 'core/home.html', context)


# ---------- MENU: to'liq CRUD ----------
def menu_list(request):
    items = MenuItem.objects.all()
    return render(request, 'core/menu_list.html', {'items': items})


def menu_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    return render(request, 'core/menu_detail.html', {'item': item})


@login_required
def menu_create(request):
    form = MenuItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Taom qo'shildi!")
        return redirect('menu_list')
    return render(request, 'core/menu_form.html', {'form': form, 'title': "Yangi taom qo'shish"})


@login_required
def menu_update(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    form = MenuItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, "Taom yangilandi!")
        return redirect('menu_detail', pk=item.pk)
    return render(request, 'core/menu_form.html', {'form': form, 'title': "Taomni tahrirlash"})


@login_required
def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Taom o'chirildi!")
        return redirect('menu_list')
    return render(request, 'core/confirm_delete.html', {'object': item, 'back': 'menu_list'})


# ---------- STOLLAR: to'liq CRUD ----------
def table_list(request):
    tables = Table.objects.all()
    return render(request, 'core/table_list.html', {'tables': tables})


@login_required
def table_create(request):
    form = TableForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Stol qo'shildi!")
        return redirect('table_list')
    return render(request, 'core/menu_form.html', {'form': form, 'title': "Yangi stol qo'shish"})


@login_required
def table_update(request, pk):
    table = get_object_or_404(Table, pk=pk)
    form = TableForm(request.POST or None, instance=table)
    if form.is_valid():
        form.save()
        messages.success(request, "Stol yangilandi!")
        return redirect('table_list')
    return render(request, 'core/menu_form.html', {'form': form, 'title': "Stolni tahrirlash"})


@login_required
def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method == 'POST':
        try:
            table.delete()
            messages.success(request, "Stol o'chirildi!")
        except ProtectedError:
            messages.error(request, "Bu stolga buyurtmalar bog'langan, o'chirib bo'lmaydi.")
        return redirect('table_list')
    return render(request, 'core/confirm_delete.html', {'object': table, 'back': 'table_list'})


# ---------- BUYURTMALAR: to'liq CRUD (login kerak) ----------
def get_order_or_403(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not request.user.is_staff and order.user != request.user:
        raise PermissionDenied
    return order


@login_required
def order_list(request):
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    return render(request, 'core/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_order_or_403(request, pk)
    return render(request, 'core/order_detail.html', {'order': order})


@login_required
def order_create(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.user = request.user
        order.save()
        form.save_m2m()
        messages.success(request, "Buyurtma yaratildi!")
        return redirect('order_detail', pk=order.pk)
    return render(request, 'core/order_form.html', {'form': form, 'title': "Yangi buyurtma"})


@login_required
def order_update(request, pk):
    order = get_order_or_403(request, pk)
    form = OrderForm(request.POST or None, instance=order)
    if form.is_valid():
        form.save()
        messages.success(request, "Buyurtma yangilandi!")
        return redirect('order_detail', pk=order.pk)
    return render(request, 'core/order_form.html', {'form': form, 'title': "Buyurtmani tahrirlash"})


@login_required
def order_delete(request, pk):
    order = get_order_or_403(request, pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Buyurtma o'chirildi!")
        return redirect('order_list')
    return render(request, 'core/confirm_delete.html', {'object': order, 'back': 'order_list'})


# ---------- AUTENTIFIKATSIYA ----------
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Ro'yxatdan o'tdingiz!")
        return redirect('home')
    return render(request, 'registration/register.html', {'form': form})