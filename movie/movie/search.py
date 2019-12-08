from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

text = """<form method="post" action="/add/">
    <input type="text" name="like" value="{}"> + <input type="text" name="b" value="{}">
    <input type="submit" value="submit"> <input type="text" value="{}">
</form>"""


@csrf_exempt
def index(request):
    if 'a' in request.POST:
        a = str(request.POST['like'])
        b = str(request.POST['b'])
    else:
        a = "no"
        b = "no"
    return HttpResponse(text.format(a,b,a+b))