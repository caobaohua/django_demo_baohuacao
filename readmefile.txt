# AIM Django Demo Project Report
Baohua Cao

SECTION I: SETUP DEV AND DATABASE, DEMO SQL
SECTION II: DEV CODING AND BUILD WEB / ADMIN
FINAL OUTPUT:
http://ec2-54-186-83-10.us-west-2.compute.amazonaws.com:8000/
http://ec2-54-186-83-10.us-west-2.compute.amazonaws.com:8000/admin/




SECTION I: SETUP DEV AND DATABASE, DEMO SQL

1.Create an AWS EC2 instance.
2.Install software packages and updates.
3.Setup virtualenv with python3
source myenv/bin/activate
4.Git clone: 
git clone https://github.com/michaelb87/aim-recruiting-django.git
5.Install requirements.txt
pip install -r requirements.txt
Fixed software bundles installation issues.
6.Make migrations
(myenv) [root@ip-172-31-31-17 aim-recruiting-django]# python manage.py makemigrations
Migrations for 'demo_app':
  demo_app/migrations/0001_initial.py
    - Create model Publisher
    - Create model Source
- Create model RevenueRecord
(myenv) [root@ip-172-31-31-17 aim-recruiting-django]# python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, demo_app, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying demo_app.0001_initial... OK
  Applying sessions.0001_initial... OK



  1) Write a custom django admin command to ingest demo data eg. `python manage.py ingest demo_data.csv`

(myenv) [ec2-user@ip-172-31-31-17 aim-recruiting-django]$vim demo_app/management/commands/ingest.py

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
                                                                                 

(myenv) [ec2-user@ip-172-31-31-17 aim-recruiting-django]$ python manage.py ingest "demo_data.csv"
Successfully read file "demo_data.csv"
date pub_name source clicks revenue
2019-10-01 micha google 138 49.68
Created a new publisher record.
Created a new source record.
Created a new revenue record.
2019-10-01 mark yahoo 263 231.44
Created a new publisher record.
Created a new source record.
Created a new revenue record.
2019-10-01 melanie google 374 179.52
Created a new publisher record.
Created a new revenue record.
2019-10-01 logan yahoo 492 403.44
Created a new publisher record.
Created a new revenue record.
2019-10-02 micha yahoo 134 127.75
Created a new revenue record.
2019-10-02 mark google 278 239.08
Created a new revenue record.
2019-10-02 melanie yahoo 478 22.31
Created a new revenue record.
2019-10-02 logan google 285 134.90
Created a new revenue record.
2019-10-03 micha google 325 244.83
Created a new revenue record.
2019-10-03 mark google 73 13.14
Created a new revenue record.
2019-10-03 melanie google 100 94.67
Created a new revenue record.
2019-10-03 logan google 424 330.72
Created a new revenue record.
2019-10-04 micha google 489 65.20
Created a new revenue record.
2019-10-04 mark google 244 92.72
Created a new revenue record.
2019-10-04 melanie google 213 210.16
Created a new revenue record.
2019-10-04 logan yahoo 84 6.16
Created a new revenue record.
2019-10-05 micha yahoo 420 282.80
Created a new revenue record.
2019-10-05 mark yahoo 421 140.33
Created a new revenue record.
2019-10-05 melanie yahoo 239 184.83
Created a new revenue record.
2019-10-05 logan yahoo 181 20.51
Created a new revenue record.
2019-10-06 micha yahoo 103 4.81
Created a new revenue record.
2019-10-06 mark google 494 55.99
Created a new revenue record.
2019-10-06 melanie google 331 88.27
Created a new revenue record.
2019-10-06 logan google 368 318.93
Created a new revenue record.
2019-10-07 micha google 210 65.80
Created a new revenue record.
2019-10-07 mark yahoo 147 128.38
Created a new revenue record.
2019-10-07 melanie yahoo 108 59.76
Created a new revenue record.
2019-10-07 logan yahoo 31 20.25
Created a new revenue record.
2019-10-08 micha google 353 298.87
Created a new revenue record.
2019-10-08 mark yahoo 44 26.69
Created a new revenue record.
2019-10-08 melanie google 117 67.08
Created a new revenue record.
2019-10-08 logan google 271 231.25
Created a new revenue record.
2019-10-09 micha yahoo 111 90.28
Created a new revenue record.
2019-10-09 mark google 364 283.92
Created a new revenue record.
2019-10-09 melanie google 475 85.50
Created a new revenue record.
2019-10-09 logan yahoo 49 26.79
Created a new revenue record.
2019-10-10 micha google 231 107.80
Created a new revenue record.
2019-10-10 mark google 158 122.19
Created a new revenue record.
2019-10-10 melanie google 69 40.48
Created a new revenue record.
2019-10-10 logan google 201 61.64
Created a new revenue record.
2019-10-11 micha yahoo 188 159.17
Created a new revenue record.
2019-10-11 mark yahoo 48 9.28
Created a new revenue record.
2019-10-11 melanie google 206 145.57
Created a new revenue record.
2019-10-11 logan google 129 100.62
Created a new revenue record.
2019-10-12 micha yahoo 109 86.47
Created a new revenue record.
2019-10-12 mark yahoo 161 156.71
Created a new revenue record.
2019-10-12 melanie yahoo 375 27.50
Created a new revenue record.
2019-10-12 logan yahoo 467 62.27
Created a new revenue record.
2019-10-13 micha google 37 22.94
Created a new revenue record.
2019-10-13 mark google 371 262.17
Created a new revenue record.
2019-10-13 melanie google 38 1.27
Created a new revenue record.
2019-10-13 logan yahoo 307 151.45
Created a new revenue record.
2019-10-14 micha google 86 36.12
Created a new revenue record.
2019-10-14 mark google 147 23.52
Created a new revenue record.
2019-10-14 melanie yahoo 114 23.56
Created a new revenue record.
2019-10-14 logan google 376 300.80
Created a new revenue record.
2019-10-15 micha google 378 221.76
Created a new revenue record.
2019-10-15 mark yahoo 261 212.28
Created a new revenue record.
2019-10-15 melanie google 295 116.03
Created a new revenue record.
2019-10-15 logan yahoo 221 184.17
Created a new revenue record.
2019-10-16 micha yahoo 316 107.44
Created a new revenue record.
2019-10-16 mark yahoo 164 106.05
Created a new revenue record.
2019-10-16 melanie yahoo 241 17.67
Created a new revenue record.
2019-10-16 logan yahoo 432 118.08
Created a new revenue record.
2019-10-17 micha google 418 415.21
Created a new revenue record.
2019-10-17 mark google 300 176.00
Created a new revenue record.
2019-10-17 melanie yahoo 103 6.87
Created a new revenue record.
2019-10-17 logan yahoo 138 29.44
Created a new revenue record.
2019-10-18 micha yahoo 413 19.27
Created a new revenue record.
2019-10-18 mark yahoo 307 36.84
Created a new revenue record.
2019-10-18 melanie google 217 47.74
Created a new revenue record.
2019-10-18 logan yahoo 275 157.67
Created a new revenue record.
2019-10-19 micha google 465 365.80
Created a new revenue record.
2019-10-19 mark yahoo 270 61.20
Created a new revenue record.
2019-10-19 melanie yahoo 255 212.50
Created a new revenue record.
2019-10-19 logan yahoo 45 16.80
Created a new revenue record.
2019-10-20 micha google 138 129.72
Created a new revenue record.
2019-10-20 mark google 498 169.32
Created a new revenue record.
2019-10-20 melanie google 340 156.40
Created a new revenue record.
2019-10-20 logan google 207 38.64
Created a new revenue record.
2019-10-21 micha google 483 460.46
Created a new revenue record.
2019-10-21 mark google 169 140.83
Created a new revenue record.
2019-10-21 melanie google 217 65.10
Created a new revenue record.
2019-10-21 logan google 490 392.00
Created a new revenue record.
2019-10-22 micha yahoo 51 31.62
Created a new revenue record.
2019-10-22 mark yahoo 434 2.89
Created a new revenue record.
2019-10-22 melanie yahoo 209 30.65
Created a new revenue record.
2019-10-22 logan yahoo 144 128.64
Created a new revenue record.
2019-10-23 micha google 109 88.65
Created a new revenue record.
2019-10-23 mark yahoo 499 182.97
Created a new revenue record.
2019-10-23 melanie google 384 17.92
Created a new revenue record.
2019-10-23 logan google 186 100.44
Created a new revenue record.
2019-10-24 micha yahoo 162 114.48
Created a new revenue record.
2019-10-24 mark yahoo 142 107.92
Created a new revenue record.
2019-10-24 melanie google 106 46.64
Created a new revenue record.
2019-10-24 logan google 105 87.50
Created a new revenue record.
2019-10-25 micha google 245 238.47
Created a new revenue record.
2019-10-25 mark google 293 220.73
Created a new revenue record.
2019-10-25 melanie yahoo 366 43.92
Created a new revenue record.
2019-10-25 logan google 112 11.20
Created a new revenue record.
2019-10-26 micha yahoo 214 179.76
Created a new revenue record.
2019-10-26 mark google 323 94.75
Created a new revenue record.
2019-10-26 melanie google 66 36.08
Created a new revenue record.
2019-10-26 logan google 437 142.75
Created a new revenue record.
2019-10-27 micha google 260 195.87
Created a new revenue record.
2019-10-27 mark google 138 47.84
Created a new revenue record.
2019-10-27 melanie yahoo 365 46.23
Created a new revenue record.
2019-10-27 logan yahoo 124 83.49
Created a new revenue record.
2019-10-28 micha google 298 282.11
Created a new revenue record.
2019-10-28 mark google 350 39.67
Created a new revenue record.
2019-10-28 melanie yahoo 318 154.76
Created a new revenue record.
2019-10-28 logan yahoo 247 189.37
Created a new revenue record.
2019-10-29 micha google 44 13.79
Created a new revenue record.
2019-10-29 mark yahoo 310 155.00
Created a new revenue record.
2019-10-29 melanie yahoo 146 127.51
Created a new revenue record.
2019-10-29 logan yahoo 492 357.52
Created a new revenue record.
2019-10-30 micha yahoo 41 24.60
Created a new revenue record.
2019-10-30 mark google 329 149.15
Created a new revenue record.
2019-10-30 melanie google 46 38.33
Created a new revenue record.
2019-10-30 logan yahoo 457 237.64
Created a new revenue record.
2019-10-31 micha yahoo 463 450.65
Created a new revenue record.
2019-10-31 mark google 376 82.72
Created a new revenue record.
2019-10-31 melanie yahoo 97 73.07
Created a new revenue record.
2019-10-31 logan yahoo 312 255.84
Created a new revenue record.
Created 4 publisher records, 2 source records, and 124 revenue records

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| django_demo        |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)

mysql> use django_demo;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+----------------------------+
| Tables_in_django_demo      |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| demo_app_publisher         |
| demo_app_revenuerecord     |
| demo_app_source            |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
+----------------------------+
13 rows in set (0.01 sec)

mysql> select * from demo_app_publisher;
+----+---------+
| id | name    |
+----+---------+
|  5 | micha   |
|  6 | mark    |
|  7 | melanie |
|  8 | logan   |
+----+---------+
4 rows in set (0.00 sec)

mysql> select * from demo_app_source;
+----+--------+
| id | name   |
+----+--------+
|  1 | google |
|  2 | yahoo  |
+----+--------+
2 rows in set (0.00 sec)

mysql> select * from demo_app_revenuerecord
    -> ;
+-----+------------+--------+---------+--------------+-----------+
| id  | date       | clicks | revenue | publisher_id | source_id |
+-----+------------+--------+---------+--------------+-----------+
|   1 | 2019-10-01 |    138 |   49.68 |            5 |         1 |
|   2 | 2019-10-01 |    263 |  231.44 |            6 |         2 |
|   3 | 2019-10-01 |    374 |  179.52 |            7 |         1 |
|   4 | 2019-10-01 |    492 |  403.44 |            8 |         2 |
|   5 | 2019-10-02 |    134 |  127.75 |            5 |         2 |
|   6 | 2019-10-02 |    278 |  239.08 |            6 |         1 |
|   7 | 2019-10-02 |    478 |   22.31 |            7 |         2 |
|   8 | 2019-10-02 |    285 |   134.9 |            8 |         1 |
|   9 | 2019-10-03 |    325 |  244.83 |            5 |         1 |
|  10 | 2019-10-03 |     73 |   13.14 |            6 |         1 |
|  11 | 2019-10-03 |    100 |   94.67 |            7 |         1 |
|  12 | 2019-10-03 |    424 |  330.72 |            8 |         1 |
|  13 | 2019-10-04 |    489 |    65.2 |            5 |         1 |
|  14 | 2019-10-04 |    244 |   92.72 |            6 |         1 |
|  15 | 2019-10-04 |    213 |  210.16 |            7 |         1 |
|  16 | 2019-10-04 |     84 |    6.16 |            8 |         2 |
|  17 | 2019-10-05 |    420 |   282.8 |            5 |         2 |
|  18 | 2019-10-05 |    421 |  140.33 |            6 |         2 |
|  19 | 2019-10-05 |    239 |  184.83 |            7 |         2 |
|  20 | 2019-10-05 |    181 |   20.51 |            8 |         2 |
|  21 | 2019-10-06 |    103 |    4.81 |            5 |         2 |
|  22 | 2019-10-06 |    494 |   55.99 |            6 |         1 |
|  23 | 2019-10-06 |    331 |   88.27 |            7 |         1 |
|  24 | 2019-10-06 |    368 |  318.93 |            8 |         1 |
|  25 | 2019-10-07 |    210 |    65.8 |            5 |         1 |
|  26 | 2019-10-07 |    147 |  128.38 |            6 |         2 |
|  27 | 2019-10-07 |    108 |   59.76 |            7 |         2 |
|  28 | 2019-10-07 |     31 |   20.25 |            8 |         2 |
|  29 | 2019-10-08 |    353 |  298.87 |            5 |         1 |
|  30 | 2019-10-08 |     44 |   26.69 |            6 |         2 |
|  31 | 2019-10-08 |    117 |   67.08 |            7 |         1 |
|  32 | 2019-10-08 |    271 |  231.25 |            8 |         1 |
|  33 | 2019-10-09 |    111 |   90.28 |            5 |         2 |
|  34 | 2019-10-09 |    364 |  283.92 |            6 |         1 |
|  35 | 2019-10-09 |    475 |    85.5 |            7 |         1 |
|  36 | 2019-10-09 |     49 |   26.79 |            8 |         2 |
|  37 | 2019-10-10 |    231 |   107.8 |            5 |         1 |
|  38 | 2019-10-10 |    158 |  122.19 |            6 |         1 |
|  39 | 2019-10-10 |     69 |   40.48 |            7 |         1 |
|  40 | 2019-10-10 |    201 |   61.64 |            8 |         1 |
|  41 | 2019-10-11 |    188 |  159.17 |            5 |         2 |
|  42 | 2019-10-11 |     48 |    9.28 |            6 |         2 |
|  43 | 2019-10-11 |    206 |  145.57 |            7 |         1 |
|  44 | 2019-10-11 |    129 |  100.62 |            8 |         1 |
|  45 | 2019-10-12 |    109 |   86.47 |            5 |         2 |
|  46 | 2019-10-12 |    161 |  156.71 |            6 |         2 |
|  47 | 2019-10-12 |    375 |    27.5 |            7 |         2 |
|  48 | 2019-10-12 |    467 |   62.27 |            8 |         2 |
|  49 | 2019-10-13 |     37 |   22.94 |            5 |         1 |
|  50 | 2019-10-13 |    371 |  262.17 |            6 |         1 |
|  51 | 2019-10-13 |     38 |    1.27 |            7 |         1 |
|  52 | 2019-10-13 |    307 |  151.45 |            8 |         2 |
|  53 | 2019-10-14 |     86 |   36.12 |            5 |         1 |
|  54 | 2019-10-14 |    147 |   23.52 |            6 |         1 |
|  55 | 2019-10-14 |    114 |   23.56 |            7 |         2 |
|  56 | 2019-10-14 |    376 |   300.8 |            8 |         1 |
|  57 | 2019-10-15 |    378 |  221.76 |            5 |         1 |
|  58 | 2019-10-15 |    261 |  212.28 |            6 |         2 |
|  59 | 2019-10-15 |    295 |  116.03 |            7 |         1 |
|  60 | 2019-10-15 |    221 |  184.17 |            8 |         2 |
|  61 | 2019-10-16 |    316 |  107.44 |            5 |         2 |
|  62 | 2019-10-16 |    164 |  106.05 |            6 |         2 |
|  63 | 2019-10-16 |    241 |   17.67 |            7 |         2 |
|  64 | 2019-10-16 |    432 |  118.08 |            8 |         2 |
|  65 | 2019-10-17 |    418 |  415.21 |            5 |         1 |
|  66 | 2019-10-17 |    300 |     176 |            6 |         1 |
|  67 | 2019-10-17 |    103 |    6.87 |            7 |         2 |
|  68 | 2019-10-17 |    138 |   29.44 |            8 |         2 |
|  69 | 2019-10-18 |    413 |   19.27 |            5 |         2 |
|  70 | 2019-10-18 |    307 |   36.84 |            6 |         2 |
|  71 | 2019-10-18 |    217 |   47.74 |            7 |         1 |
|  72 | 2019-10-18 |    275 |  157.67 |            8 |         2 |
|  73 | 2019-10-19 |    465 |   365.8 |            5 |         1 |
|  74 | 2019-10-19 |    270 |    61.2 |            6 |         2 |
|  75 | 2019-10-19 |    255 |   212.5 |            7 |         2 |
|  76 | 2019-10-19 |     45 |    16.8 |            8 |         2 |
|  77 | 2019-10-20 |    138 |  129.72 |            5 |         1 |
|  78 | 2019-10-20 |    498 |  169.32 |            6 |         1 |
|  79 | 2019-10-20 |    340 |   156.4 |            7 |         1 |
|  80 | 2019-10-20 |    207 |   38.64 |            8 |         1 |
|  81 | 2019-10-21 |    483 |  460.46 |            5 |         1 |
|  82 | 2019-10-21 |    169 |  140.83 |            6 |         1 |
|  83 | 2019-10-21 |    217 |    65.1 |            7 |         1 |
|  84 | 2019-10-21 |    490 |     392 |            8 |         1 |
|  85 | 2019-10-22 |     51 |   31.62 |            5 |         2 |
|  86 | 2019-10-22 |    434 |    2.89 |            6 |         2 |
|  87 | 2019-10-22 |    209 |   30.65 |            7 |         2 |
|  88 | 2019-10-22 |    144 |  128.64 |            8 |         2 |
|  89 | 2019-10-23 |    109 |   88.65 |            5 |         1 |
|  90 | 2019-10-23 |    499 |  182.97 |            6 |         2 |
|  91 | 2019-10-23 |    384 |   17.92 |            7 |         1 |
|  92 | 2019-10-23 |    186 |  100.44 |            8 |         1 |
|  93 | 2019-10-24 |    162 |  114.48 |            5 |         2 |
|  94 | 2019-10-24 |    142 |  107.92 |            6 |         2 |
|  95 | 2019-10-24 |    106 |   46.64 |            7 |         1 |
|  96 | 2019-10-24 |    105 |    87.5 |            8 |         1 |
|  97 | 2019-10-25 |    245 |  238.47 |            5 |         1 |
|  98 | 2019-10-25 |    293 |  220.73 |            6 |         1 |
|  99 | 2019-10-25 |    366 |   43.92 |            7 |         2 |
| 100 | 2019-10-25 |    112 |    11.2 |            8 |         1 |
| 101 | 2019-10-26 |    214 |  179.76 |            5 |         2 |
| 102 | 2019-10-26 |    323 |   94.75 |            6 |         1 |
| 103 | 2019-10-26 |     66 |   36.08 |            7 |         1 |
| 104 | 2019-10-26 |    437 |  142.75 |            8 |         1 |
| 105 | 2019-10-27 |    260 |  195.87 |            5 |         1 |
| 106 | 2019-10-27 |    138 |   47.84 |            6 |         1 |
| 107 | 2019-10-27 |    365 |   46.23 |            7 |         2 |
| 108 | 2019-10-27 |    124 |   83.49 |            8 |         2 |
| 109 | 2019-10-28 |    298 |  282.11 |            5 |         1 |
| 110 | 2019-10-28 |    350 |   39.67 |            6 |         1 |
| 111 | 2019-10-28 |    318 |  154.76 |            7 |         2 |
| 112 | 2019-10-28 |    247 |  189.37 |            8 |         2 |
| 113 | 2019-10-29 |     44 |   13.79 |            5 |         1 |
| 114 | 2019-10-29 |    310 |     155 |            6 |         2 |
| 115 | 2019-10-29 |    146 |  127.51 |            7 |         2 |
| 116 | 2019-10-29 |    492 |  357.52 |            8 |         2 |
| 117 | 2019-10-30 |     41 |    24.6 |            5 |         2 |
| 118 | 2019-10-30 |    329 |  149.15 |            6 |         1 |
| 119 | 2019-10-30 |     46 |   38.33 |            7 |         1 |
| 120 | 2019-10-30 |    457 |  237.64 |            8 |         2 |
| 121 | 2019-10-31 |    463 |  450.65 |            5 |         2 |
| 122 | 2019-10-31 |    376 |   82.72 |            6 |         1 |
| 123 | 2019-10-31 |     97 |   73.07 |            7 |         2 |
| 124 | 2019-10-31 |    312 |  255.84 |            8 |         2 |
+-----+------------+--------+---------+--------------+-----------+
124 rows in set (0.00 sec)




 2) 
show a table with the following columns:
    - date
    - sum(revenue)
    - sum(clicks)


| date      | total_revenue  | total_clicks    |
| 2019-10-01 |        864.08 |         1267 |
| 2019-10-02 |        524.04 |         1175 |
| 2019-10-03 |        683.36 |          922 |
| 2019-10-04 |        374.24 |         1030 |
| 2019-10-05 |        628.47 |         1261 |
| 2019-10-06 |        468.00 |         1296 |
| 2019-10-07 |        274.19 |          496 |
| 2019-10-08 |        623.89 |          785 |
| 2019-10-09 |        486.49 |          999 |
| 2019-10-10 |        332.11 |          659 |
| 2019-10-11 |        414.64 |          571 |
| 2019-10-12 |        332.95 |         1112 |
| 2019-10-13 |        437.83 |          753 |
| 2019-10-14 |        384.00 |          723 |
| 2019-10-15 |        734.24 |         1155 |
| 2019-10-16 |        349.24 |         1153 |
| 2019-10-17 |        627.52 |          959 |
| 2019-10-18 |        261.52 |         1212 |
| 2019-10-19 |        656.30 |         1035 |
| 2019-10-20 |        494.08 |         1183 |
| 2019-10-21 |       1058.39 |         1359 |
| 2019-10-22 |        193.80 |          838 |
| 2019-10-23 |        389.98 |         1178 |
| 2019-10-24 |        356.54 |          515 |
| 2019-10-25 |        514.32 |         1016 |
| 2019-10-26 |        453.34 |         1040 |
| 2019-10-27 |        373.43 |          887 |
| 2019-10-28 |        665.91 |         1213 |
| 2019-10-29 |        653.82 |          992 |
| 2019-10-30 |        449.72 |          873 |
| 2019-10-31 |        862.28 |         1248 |

 3) 
show another table with the following columns:
    - publisher name
    - sum(revenue)
    - sum(clicks)

| publisher   | total_revenue   | total_clicks   |
| micha   |       4982.18 |         7432 |
| mark    |       3771.72 |         8376 |
| melanie  |       2467.90 |         7008 |
| logan    |       4700.92 |         8089 |

show another table with the following columns:
- publisher name
- date
    - sum(revenue) by date
    - sum(clicks) by date


| publisher    | date     | total_revenue   | total_clicks    |
| micha   | 2019-10-01 |         49.68 |          138 |
| micha   | 2019-10-02 |        127.75 |          134 |
| micha   | 2019-10-03 |        244.83 |          325 |
| micha   | 2019-10-04 |         65.20 |          489 |
| micha   | 2019-10-05 |        282.80 |          420 |
| micha   | 2019-10-06 |          4.81 |          103 |
| micha   | 2019-10-07 |         65.80 |          210 |
| micha   | 2019-10-08 |        298.87 |          353 |
| micha   | 2019-10-09 |         90.28 |          111 |
| micha   | 2019-10-10 |        107.80 |          231 |
| micha   | 2019-10-11 |        159.17 |          188 |
| micha   | 2019-10-12 |         86.47 |          109 |
| micha   | 2019-10-13 |         22.94 |           37 |
| micha   | 2019-10-14 |         36.12 |           86 |
| micha   | 2019-10-15 |        221.76 |          378 |
| micha   | 2019-10-16 |        107.44 |          316 |
| micha   | 2019-10-17 |        415.21 |          418 |
| micha   | 2019-10-18 |         19.27 |          413 |
| micha   | 2019-10-19 |        365.80 |          465 |
| micha   | 2019-10-20 |        129.72 |          138 |
| micha   | 2019-10-21 |        460.46 |          483 |
| micha   | 2019-10-22 |         31.62 |           51 |
| micha   | 2019-10-23 |         88.65 |          109 |
| micha   | 2019-10-24 |        114.48 |          162 |
| micha   | 2019-10-25 |        238.47 |          245 |
| micha   | 2019-10-26 |        179.76 |          214 |
| micha   | 2019-10-27 |        195.87 |          260 |
| micha   | 2019-10-28 |        282.11 |          298 |
| micha   | 2019-10-29 |         13.79 |           44 |
| micha   | 2019-10-30 |         24.60 |           41 |
| micha   | 2019-10-31 |        450.65 |          463 |
| mark    | 2019-10-01 |        231.44 |          263 |
| mark    | 2019-10-02 |        239.08 |          278 |
| mark    | 2019-10-03 |         13.14 |           73 |
| mark    | 2019-10-04 |         92.72 |          244 |
| mark    | 2019-10-05 |        140.33 |          421 |
| mark    | 2019-10-06 |         55.99 |          494 |
| mark    | 2019-10-07 |        128.38 |          147 |
| mark    | 2019-10-08 |         26.69 |           44 |
| mark    | 2019-10-09 |        283.92 |          364 |
| mark    | 2019-10-10 |        122.19 |          158 |
| mark    | 2019-10-11 |          9.28 |           48 |
| mark    | 2019-10-12 |        156.71 |          161 |
| mark    | 2019-10-13 |        262.17 |          371 |
| mark    | 2019-10-14 |         23.52 |          147 |
| mark    | 2019-10-15 |        212.28 |          261 |
| mark    | 2019-10-16 |        106.05 |          164 |
| mark    | 2019-10-17 |        176.00 |          300 |
| mark    | 2019-10-18 |         36.84 |          307 |
| mark    | 2019-10-19 |         61.20 |          270 |
| mark    | 2019-10-20 |        169.32 |          498 |
| mark    | 2019-10-21 |        140.83 |          169 |
| mark    | 2019-10-22 |          2.89 |          434 |
| mark    | 2019-10-23 |        182.97 |          499 |
| mark    | 2019-10-24 |        107.92 |          142 |
| mark    | 2019-10-25 |        220.73 |          293 |
| mark    | 2019-10-26 |         94.75 |          323 |
| mark    | 2019-10-27 |         47.84 |          138 |
| mark    | 2019-10-28 |         39.67 |          350 |
| mark    | 2019-10-29 |        155.00 |          310 |
| mark    | 2019-10-30 |        149.15 |          329 |
| mark    | 2019-10-31 |         82.72 |          376 |
| melanie | 2019-10-01 |        179.52 |          374 |
| melanie | 2019-10-02 |         22.31 |          478 |
| melanie | 2019-10-03 |         94.67 |          100 |
| melanie | 2019-10-04 |        210.16 |          213 |
| melanie | 2019-10-05 |        184.83 |          239 |
| melanie | 2019-10-06 |         88.27 |          331 |
| melanie | 2019-10-07 |         59.76 |          108 |
| melanie | 2019-10-08 |         67.08 |          117 |
| melanie | 2019-10-09 |         85.50 |          475 |
| melanie | 2019-10-10 |         40.48 |           69 |
| melanie | 2019-10-11 |        145.57 |          206 |
| melanie | 2019-10-12 |         27.50 |          375 |
| melanie | 2019-10-13 |          1.27 |           38 |
| melanie | 2019-10-14 |         23.56 |          114 |
| melanie | 2019-10-15 |        116.03 |          295 |
| melanie | 2019-10-16 |         17.67 |          241 |
| melanie | 2019-10-17 |          6.87 |          103 |
| melanie | 2019-10-18 |         47.74 |          217 |
| melanie | 2019-10-19 |        212.50 |          255 |
| melanie | 2019-10-20 |        156.40 |          340 |
| melanie | 2019-10-21 |         65.10 |          217 |
| melanie | 2019-10-22 |         30.65 |          209 |
| melanie | 2019-10-23 |         17.92 |          384 |
| melanie | 2019-10-24 |         46.64 |          106 |
| melanie | 2019-10-25 |         43.92 |          366 |
| melanie | 2019-10-26 |         36.08 |           66 |
| melanie | 2019-10-27 |         46.23 |          365 |
| melanie | 2019-10-28 |        154.76 |          318 |
| melanie | 2019-10-29 |        127.51 |          146 |
| melanie | 2019-10-30 |         38.33 |           46 |
| melanie | 2019-10-31 |         73.07 |           97 |
| logan   | 2019-10-01 |        403.44 |          492 |
| logan   | 2019-10-02 |        134.90 |          285 |
| logan   | 2019-10-03 |        330.72 |          424 |
| logan   | 2019-10-04 |          6.16 |           84 |
| logan   | 2019-10-05 |         20.51 |          181 |
| logan   | 2019-10-06 |        318.93 |          368 |
| logan   | 2019-10-07 |         20.25 |           31 |
| logan   | 2019-10-08 |        231.25 |          271 |
| logan   | 2019-10-09 |         26.79 |           49 |
| logan   | 2019-10-10 |         61.64 |          201 |
| logan   | 2019-10-11 |        100.62 |          129 |
| logan   | 2019-10-12 |         62.27 |          467 |
| logan   | 2019-10-13 |        151.45 |          307 |
| logan   | 2019-10-14 |        300.80 |          376 |
| logan   | 2019-10-15 |        184.17 |          221 |
| logan   | 2019-10-16 |        118.08 |          432 |
| logan   | 2019-10-17 |         29.44 |          138 |
| logan   | 2019-10-18 |        157.67 |          275 |
| logan   | 2019-10-19 |         16.80 |           45 |
| logan   | 2019-10-20 |         38.64 |          207 |
| logan   | 2019-10-21 |        392.00 |          490 |
| logan   | 2019-10-22 |        128.64 |          144 |
| logan   | 2019-10-23 |        100.44 |          186 |
| logan   | 2019-10-24 |         87.50 |          105 |
| logan   | 2019-10-25 |         11.20 |          112 |
| logan   | 2019-10-26 |        142.75 |          437 |
| logan   | 2019-10-27 |         83.49 |          124 |
| logan   | 2019-10-28 |        189.37 |          247 |
| logan   | 2019-10-29 |        357.52 |          492 |
| logan   | 2019-10-30 |        237.64 |          457 |
| logan   | 2019-10-31 |        255.84 |          312 |

 4) 
show a table with the following columns:
    - source
    - sum(revenue)
    - sum(clicks)

| source   | total_revenue  | total_clicks    |
| google   |       9204.97 |        16797 |
| yahoo   |       6717.75 |        14108 |

show a table with the following columns:
    - publisher
    - source
    - sum(revenue)
    - sum(clicks)

| publisher | source  | total_revenue  | total_clicks    |
| micha   | yahoo  |       1679.10 |         2725 |
| micha   | google  |       3303.08 |         4707 |
| mark    | yahoo  |       1557.98 |         3471 |
| mark    | google  |       2213.74 |         4905 |
| melanie | yahoo   |       1031.14 |         3414 |
| melanie | google  |       1436.76 |         3594 |
| logan   | yahoo  |       2449.53 |         4498 |
| logan   | google  |       2251.39 |         3591 |




Setting up development environment issues and fixes:

......

  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/django/db/backends/mysql/base.py", line 36, in <module>
    raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3.

Update the mysqlclient version to fix this and update the __init__.py under the project:
import pymysql 
pymysql.install_as_MySQLdb()

Commented out the version check from the base.py file:
Fixed:
Vim python3.7/site-packages/django/db/backends/mysql/base.py

34 version = Database.version_info
 35 #if version < (1, 3, 13):
 36 #    raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you     have %s.' % Database.__version__)
 37 

File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/django/db/backends/mysql/operations.py", line 146, in last_executed_query
    query = query.decode(errors='replace')
AttributeError: 'str' object has no attribute 'decode'

Fixed:

140     def last_executed_query(self, cursor, sql, params):
141         # With MySQLdb, cursor objects have an (undocumented) "_executed"
142         # attribute where the exact query sent to the database is saved.
143         # See MySQLdb/cursors.py in the source distribution.
144         query = getattr(cursor, '_executed', None)
145         if query is not None:
146             query = query.encode(errors='replace')	
# decode modified to encode
147         return query

Reset mysql root password by using mysql safe mode to access the mysql database.


SECTION II: DEV CODING AND BUILD WEB / ADMIN

1.Create Admin
(myenv) [ec2-user@ip-172-31-31-17 aim-recruiting-django]$ python manage.py createsuperuser
Username (leave blank to use 'ec2-user'): admin
Email address: caobaohua@gmail.com
Password:
Password (again):
Superuser created successfully.

2.Enable AWS EC2 Security Group for Remote Access
Open 8000 for TCP in ec2 instance’s security group
Custom TCP Rule		TCP		8000 	0.0.0.0/0

3.Run Django Server:
(myenv) [ec2-user@ip-172-31-31-17 aim-recruiting-django]$ python manage.py runserver 0.0.0.0:8000
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 27, 2019 - 01:38:05
Django version 2.2.7, using settings 'demo.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
[27/Nov/2019 01:38:08] "GET / HTTP/1.1" 200 126
[27/Nov/2019 01:41:48] "GET / HTTP/1.1" 200 167

4.Remotely Access Main Home-Page from Browsers:
http://ec2-54-186-83-10.us-west-2.compute.amazonaws.com:8000/
Or
http://54.186.83.10:8000/

5.Remotely Access Admin System from Browsers:
http://ec2-54-186-83-10.us-west-2.compute.amazonaws.com:8000/admin/
http://54.186.83.10:8000/admin/
User: admin
Password: smiletolife

6.Collect Static Files of JS, HTML, CSS, IMAGES
(myenv) [ec2-user@ip-172-31-31-17 aim-recruiting-django]$ python manage.py collectstatic

You have requested to collect static files at the destination
location as specified in your settings:

    /home/ec2-user/aim-recruiting-django/static

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: yes

7.Restart Django Server 
(myenv) [ec2-user@ip-172-31-31-17 aim-recruiting-django]$ python manage.py runserver 0.0.0.0:8000
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 27, 2019 - 11:27:14
Django version 2.2.7, using settings 'demo.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.

8.Add Routings
Update urls.py to add routings as follows:
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('date_view/<str:date>/', views.date_view, name='date_view'),
    path('publisher_view/<int:publisher>/<str:date>/',views.publisher_view, 			name='publisher_view'),
]

9.Add Views
Update views.py to add new data processing logic as follows:
from django.shortcuts import render
from django.views import View
from .models import Publisher, Source, RevenueRecord
from django.db.models import Sum
from .tables import *
from django_tables2 import RequestConfig
#from django.http import HttpResponse

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
        #return HttpResponse(str(obj))
    table = DateRevenueTable(DateRevenueObjects)
    RequestConfig(request).configure(table)
    return render(request, 'date_template.html', {'table': table})

def publisher_view(request, publisher, date):
    PublisherRevenueObjects = RevenueRecord.objects.filter(date=date,publisher=publisher).values('source')\
            .annotate(Sum('revenue')).annotate(Sum('clicks'))
    for obj in PublisherRevenueObjects:
        obj['source_name'] = Source.objects.get(pk=obj['source']).name
    table = PublisherRevenueTable(PublisherRevenueObjects)
    return render(request, 'publisher_template.html', {'table': table})
#return HttpResponse('<html><head></head><body>publisher: %s, date: %s</body></html>' % (publisher, date))

10.Add Django tables2
Add django tables2 to use the new djang’s tables2 template for table rendering, ordering and pagination as follows:

# add your table herei
import django_tables2 as tables
from .models import RevenueRecord
import datetime

class RevenueRecordTable(tables.Table):
    class Meta:
        model = RevenueRecord
        #template_name = "django_tables2/bootstrap.html"
        fields = ("date", "revenue__sum", "clicks__sum")

    #date = tables.LinkColumn('date_view', args=[tables.A('date')])
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

11.Add Templates
Add html templates to render the front-end html pages and tables as follows:

{% load render_table from django_tables2 %}
<!doctype html>
<html>
    <head>
        <title>Demo Page</title>
    </head>
    <body>
        {% render_table table %}
    </body>
</html>

{% load render_table from django_tables2 %}
<!doctype html>
<html>
    <head>
        <title>Daily Revenue Page</title>
    </head>
    <body>
        {% render_table table %}
    </body>
</html>

{% load render_table from django_tables2 %}
<!doctype html>
<html>
    <head>
        <title>Publisher Daily Revenue Page</title>
    </head>
    <body>
        {% render_table table %}
    </body>
</html>

12. Collect Static Files and Run Django Server to update the web system
(myenv) [ec2-user@ip-172-31-31-17 aim-recruiting-django]$ python manage.py collectstatic
(myenv) [ec2-user@ip-172-31-31-17 aim-recruiting-django]$ python manage.py runserver 0.0.0.0:8000
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 27, 2019 - 13:19:34
Django version 2.2.7, using settings 'demo.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.

13.Open browsers and test
http://ec2-54-186-83-10.us-west-2.compute.amazonaws.com:8000/
http://ec2-54-186-83-10.us-west-2.compute.amazonaws.com:8000/admin/

http://54.186.83.10:8000/
http://54.186.83.10:8000/admin/login/?next=/admin/
