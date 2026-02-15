from django.shortcuts import render
from jobs.models import Job

def index(request):
    template_data = {}
    template_data['title'] = "Maps"
    template_data['locations'] = list(
        Job.objects.values('id', 'location_lat', 'location_long', 'title', 'location')
    )

    return render(request, 'maps/index.html', {'template_data':template_data})
