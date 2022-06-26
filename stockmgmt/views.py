from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm, StockHistorySearchForm, \
    ReorderLevelForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Stock, StockHistory
import csv
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    title = 'Welcome: This is the Home Page'
    form = 'Welcome: This is the Home Page'
    context = {
        "title": title,
        "test": form,
    }
    return redirect('/stock/v1/list_item/')


@login_required(login_url='/stock/v1/accounts/login/')
def list_item(request):
    title = 'List of Items'
    queryset = Stock.objects.all()
    form = StockSearchForm(request.POST or None)
    context = {
        "title": title,
        "form": form,
        "queryset": queryset,
    }
    if request.method == 'POST':
        if form['category'].value() != '' or form['item_name'].value() != '':

            queryset = queryset.filter(
                Q(item_name__icontains=form['item_name'].value()),
                Q(category__iexact=form['category'].value()
                  ))

            if form['export_to_CSV'].value():
                return extracted_to_csv(queryset)
        else:
            queryset = Stock.objects.all()

        context = {
            "form": form,
            "title": title,
            "queryset": queryset,
        }

    return render(request, "list_item.html", context)


# TODO Rename this here and in `list_item`
def extracted_to_csv(queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
    writer = csv.writer(response)
    writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
    instance = queryset
    for stock in instance:
        writer.writerow([stock.category, stock.item_name, stock.quantity])
    return response


@login_required(login_url='/stock/v1/accounts/login/')
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/stock/v1/list_item')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_item.html", context)


@login_required(login_url='/stock/v1/accounts/login/')
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Updated')
            return redirect('/stock/v1/list_item')

    context = {
        'form': form
    }
    return render(request, 'add_item.html', context)


@login_required(login_url='/stock/v1/accounts/login/')
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Item Deleted Successfully ')
        return redirect('/stock/v1/list_item')
    return render(request, 'delete_items.html')


@login_required(login_url='/stock/v1/accounts/login/')
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)


@login_required(login_url='/stock/v1/accounts/login/')
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user.first_name)
        messages.success(request, f"Issued SUCCESSFULLY. {str(instance.quantity)} {str(instance.item_name)}s now left "
                                  f"in Store")
        instance.save()
        return redirect(f'/stock/v1/stock_detail/{str(instance.id)}')

    context = {"title": f'Issue {str(queryset.item_name)}', "queryset": queryset, "form": form,
               "username": f'Issue By: {str(request.user)}'}

    return render(request, "add_item.html", context)


@login_required(login_url='/stock/v1/accounts/login/')
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, f"Received SUCCESSFULLY. {str(instance.quantity)} {str(instance.item_name)}s now in "
                                  f"Store")
        return redirect(f'/stock/v1/stock_detail/{str(instance.id)}')
    context = {"title": f'Receive {str(queryset.item_name)}', "instance": queryset, "form": form,
               "username": f'Receive By: {str(request.user)}'}

    return render(request, "add_item.html", context)


@login_required(login_url='/stock/v1/accounts/login/')
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, f"Reorder level for {str(instance.item_name)} is updated to "
                                  f"{str(instance.reorder_level)}")

        return redirect(f"/stock/v1/stock_detail/{pk}/")
    context = {
        "instance": queryset,
        "form": form,
    }
    return render(request, "add_item.html", context)


@login_required(login_url='/stock/v1/accounts/login/')
def list_history(request):
    header = 'LIST OF ITEMS'
    form = StockHistorySearchForm(request.POST or None)
    queryset = StockHistory.objects.all()
    context = {
        "form": form,
        "header": header,
        "queryset": queryset,
    }

    if request.method == 'POST':
        if form['category'].value() != '' or form['item_name'].value() != '':

            queryset = queryset.filter(
                Q(category__iexact=form['category'].value()) ,
                Q(item_name__icontains=form['item_name'].value())

            )

            if form['export_to_CSV'].value():
                return extracted_to_csv2(queryset)

        else:
            queryset = StockHistory.objects.all()

        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }

    return render(request, "list_history.html", context)


def extracted_to_csv2(queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
    writer = csv.writer(response)
    writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY', 'ISSUE QUANTITY',
                     'RECEIVE QUANTITY', 'RECEIVE BY', 'ISSUE BY', 'LAST UPDATED'])
    instance = queryset
    for stock in instance:
        writer.writerow([stock.category, stock.item_name, stock.quantity, stock.issue_quantity,
                         stock.receive_quantity, stock.receive_by, stock.issue_by, stock.last_updated])
    return response
