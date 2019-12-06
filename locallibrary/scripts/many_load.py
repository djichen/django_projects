import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load

from unesco.models import Site, Category, States, Region, Iso

def run():
    fhand = open('unesco/whc-sites-2018-clean.csv')
    reader = csv.reader(fhand)

    Site.objects.all().delete()
    Category.objects.all().delete()
    States.objects.all().delete()
    Region.objects.all().delete()
    Iso.objects.all().delete()


    # Format
    # jane@tsugi.org,I,Python
    # ed@tsugi.org,L,Python

    for row in reader:
        print(row)

        c, created = Category.objects.get_or_create(name=row[7])
        s, created = States.objects.get_or_create(name=row[8])
        r, created = Region.objects.get_or_create(name=row[9])
        i, created = Iso.objects.get_or_create(name=row[10])
        #lo, created = Longitude.objects.get_or_create(name=float(row[4]))
        #la, created = Latitude.objects.get_or_create(name=float(row[5]))
        #a, created = Area_hectares.objects.get_or_create(name=float(row[6]))
        n = row[0]
        try:
            y = int(row[3])
        except:
            y = None

        try:
            loo = float(row[4])
        except:
            loo = None

        try:
            laa = float(row[5])
        except:
            laa = None

        try:
            aa = float(row[6])
        except:
            aa = None

        si = Site(name = n,description=row[1],justification = row[2], year = y, category = c, states = s, region = r, iso = i,longitude = loo, latitude = laa, area_hectares = aa)
        si.save()
