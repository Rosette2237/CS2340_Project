from django.shortcuts import render
def index(request):
    template_data = {}
    template_data['title'] = "Maps"
    return render(request, 'maps/index.html', {'template_data':template_data})