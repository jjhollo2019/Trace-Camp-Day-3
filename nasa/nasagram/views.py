from django.shortcuts import render
from django.http import HttpResponse
import requests
from datetime import datetime
from nasagram.models import NasaComment
from django.shortcuts import redirect

# Create your views here.
def date_selector(request):
    return render(request, 'date_picker.html')

def nasa_detail(request, id):
    nasa_comment = NasaComment.objects.get(id = id)
    return render(request, 'detail_view.html', {'nasa_comment': nasa_comment})

def nasa_create(request):
    if(request.method == "POST"):
        print(request.POST)
        # This is the date object we are creating from the date_string
        date = datetime.strptime(request.POST.get('date_selected', '2018-01-01'), "%Y-%m-%d").date()
        # Now we create the object
        nasa_comment = NasaComment.objects.create(
            rating = request.POST.get('rating', 0),
            favorite = request.POST.get('favorite', False) == "on",
            comment = request.POST.get('comment_section', ''),
            image_url = request.POST.get('url', ''),
            date = date,
        )
        return redirect(f'/nasa/comment/detail/{nasa_comment.id}')
    elif(request.method == "GET"):
        # We need to get the date from the query parameters and the picture from Nasa
        date = request.GET.get("date_selected", "")
        api_key = "oMrH77hL0IcYFpEAYw6HpzxULiro2VX2jGy9CIMV"
        r = requests.get(f'https://api.nasa.gov/planetary/apod?date={date}&api_key={api_key}')
        url = r.json()["url"]
        # render the image and form
        return render(request, 'create_comment.html', {'picture':url})
    else:
        return HttpResponse("Error, How did you get here?")

def nasa_list(request):
    nasa_comment = NasaComment.objects.all()
    return render(request, 'comment_list.html', { 'nasa_comments': nasa_comment })