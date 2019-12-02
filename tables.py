# add your table herei
import django_tables2 as tables
from .models import RevenueRecord
import datetime


class RevenueRecordTable(tables.Table):
    class Meta:
        model = RevenueRecord
        # template_name = "django_tables2/bootstrap.html"
        fields = ("date", "revenue__sum", "clicks__sum")

    # date = tables.LinkColumn('date_view', args=[tables.A('date')])
    date = tables.Column(linkify=('date_view',{'date':tables.A('date')}))
    revenue__sum = tables.Column()

    def render_revenue__sum(self, value):
        return '{:0.2f}'.format(value)


class DateRevenueTable(tables.Table):
    revenue__sum = tables.Column()

    class Meta:
        model = RevenueRecord
        fields = ("name", "revenue__sum", "clicks__sum")

    name = tables.Column(linkify=('publisher_view', {'publisher': tables.A('publisher'), 'date': tables.A('date')}))

    def render_revenue__sum(self, value):
        return '{:0.2f}'.format(value)


class PublisherRevenueTable(tables.Table):
    class Meta:
        model = RevenueRecord
        fields = ("source_name", "revenue__sum", "clicks__sum")

    revenue__sum = tables.Column()

    def render_revenue__sum(self, value):
        return '{:0.2f}'.format(value)