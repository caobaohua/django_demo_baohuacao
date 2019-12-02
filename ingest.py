from django.core.management.base import BaseCommand, CommandError
import os
import csv
from demo_app.models import Publisher, Source, RevenueRecord
import datetime

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)


    def handle(self, *args, **options):
        file = options['file']
        if not os.path.exists(file):
            raise CommandError("%s doesnt exist." % file)
        self.stdout.write(self.style.SUCCESS('Successfully read file "%s"' % file))
        with open(file, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            fields_name = list(next(reader))
            self.stdout.write(" ".join(fields_name))
            objects_counter = [0] * 3
            for row in reader:
                date, pub_name, source, clicks, revenue = tuple(row)
                self.stdout.write(" ".join([date, pub_name, source, clicks, revenue]))
                try:
                    Publisher_Obj = Publisher.objects.get(name=pub_name)
                except Publisher.DoesNotExist:
                    Publisher_Obj = Publisher(name=pub_name)
                    Publisher_Obj.save()
                    objects_counter[0] += 1
                    self.stdout.write('Created a new publisher record.')
                try:
                   Source_Obj = Source.objects.get(name=source)
                except Source.DoesNotExist:
                    Source_Obj = Source(name=source)
                    Source_Obj.save()
                    objects_counter[1] += 1
                    self.stdout.write('Created a new source record.')
                Publisher_Obj = Publisher.objects.get(name=pub_name)
                Source_Obj = Source.objects.get(name=source)
                clicks, revenue = int(clicks), float(revenue)
                year, month, day = tuple([int(i) for i in date.split("-")])
                date = datetime.date(year, month, day)
                revenue_record = RevenueRecord(date=date, publisher=Publisher_Obj, source=Source_Obj, clicks=clicks, revenue=revenue)
                revenue_record.save()
                objects_counter[2] += 1
                self.stdout.write('Created a new revenue record.')
            self.stdout.write("Created %s publisher records, %s source records, and %s revenue records" % tuple(objects_counter))