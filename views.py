from django.shortcuts import render
from django.views import View
from .models import Publisher, Source, RevenueRecord
from django.db.models import Sum
from .tables import *
from django_tables2 import RequestConfig
# from django.http import HttpResponse


class IndexView(View):
    def get(self, request):
        table = RevenueRecordTable(RevenueRecord.objects.values('date')\
                .annotate(Sum('revenue')).annotate(Sum('clicks')))
        RequestConfig(request).configure(table)
        return render(request, 'index_template.html', {'table': table})


def date_view(request, date):

    DateRevenueObjects = RevenueRecord.objects.filter(date=date).values('publisher')\
            .annotate(Sum('revenue')).annotate(Sum('clicks'))
    for obj in DateRevenueObjects:
        obj['date'] = date
        obj['name'] = Publisher.objects.get(pk=obj['publisher']).name
        # return HttpResponse(str(obj))
    table = DateRevenueTable(DateRevenueObjects)
    RequestConfig(request).configure(table)
    return render(request, 'date_template.html', {'table': table})


def publisher_view(request, publisher, date):
    PublisherRevenueObjects = RevenueRecord.objects.filter(date=date, publisher=publisher).values('source')\
            .annotate(Sum('revenue')).annotate(Sum('clicks'))
    for obj in PublisherRevenueObjects:
        obj['source_name'] = Source.objects.get(pk=obj['source']).name
    table = PublisherRevenueTable(PublisherRevenueObjects)
    return render(request, 'publisher_template.html', {'table': table})
    # return HttpResponse('<html><head></head><body>publisher: %s, date: %s</body></html>' % (publisher, date))
