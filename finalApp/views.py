from django.shortcuts import render

# Create your views here.
def listing_list(request):
    return render(request, 'finalApp/listing_list.html', {})