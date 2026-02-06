from django.shortcuts import render
def index(request):
    template_data = {}
    template_data['title'] = "Home Page"
    return render(request, 'home/index.html', {'template_data':template_data})