import datetime
import random
from django.core.management.base import BaseCommand
from app.models import CustomUser, Staff

first_name = [
    'Prof. Amadou',
    'M. Abd.Rahman',
    'Doc. Saliou',
    'M. Hamza',
    'M. Abdoulaye'
]

last_name = [
    'Dicko',
    'Ag',
    'Haidara',
    'Boniface',
    'Aliou'
]

adresse = [
    'Secteur 1, Gao',
    'Secteur 2, Gao',
    'Secteur 3, Gao',
    'Secteur 4, Gao',
    'Chateau, Gao'
]

telephone = [
    '78459632',
    '85659856',
    '65236589',
    '95468956',
    '87456325'
]

def generate_first_name():
    index = random.randint(0, 4)
    return first_name[index]

def generate_last_name():
    index = random.randint(0, 4)
    return last_name[index]

def generate_adresse():
    index = random.randint(0, 4)
    return adresse[index]

def generate_telephone():
    index = random.randint(0, 4)
    return int(telephone[index])


def generate_create_date():
    year = 2023
    month = random.randint(1, 6)
    day = random.randint(1, 28)
    return datetime.date(year, month, day)

def generate_modified_date():
    year = 2023
    month = random.randint(1, 6)
    day = random.randint(1, 28)
    return datetime.date(year, month, day)

# telephone = generate_telephone()
# print(type(telephone))

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         'file_name', type=str, help='Staff creation txt file'
    #     )
    help='Staff creation txt file'


    def handle(self, *args, **kwargs):
        first_name = generate_first_name()
        last_name = generate_last_name()
        adresse = generate_adresse()
        date_cree = generate_create_date()
        date_modifie = generate_modified_date()

        user = CustomUser(            
            first_name = first_name,
            last_name = last_name,
            email = f'{first_name}.{last_name}@technosup.ml',
            username = last_name,
            user_type = 'STAFF'
        )

        if CustomUser.objects.filter(username=last_name).exists() == False:
            user.set_password('admin001')
            user.save()

        staff = Staff(
            user = CustomUser.objects.get(username=last_name),
            adresse = adresse,
            sexe = 'Male',
            telephone = telephone,
            date_cree = date_cree,
            date_modifie = date_modifie
        )

        staff.save()
        

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
