from datetime import datetime

from django.apps import apps

from fabpricetracker.celery import app

from scrapper.cardmarket_scrapper import scrap_cm

RELEASE_DATE_BREAKPOINT = "2022-02-04"

ALPHA_SETS = ['WTR', 'ARC']

PITCH_MAP = {'1': 'Red', '2': 'Yellow', '3': 'Blue'}

CORE_SETS = ['WTR', 'ARC', 'CRU', 'MON', 'ELE', 'EVR', 'UPR', 'DYN',
             'OUT', 'DTD', 'EVO', 'HVY', 'MST']


@app.task
def scrap_cm_card(card_printing_pk):
    print_obj = apps.get_model('cards.cardprinting').objects.get(pk=card_printing_pk)
    result_dict = {}
    printing_set_obj = print_obj.set
    card_obj = print_obj.card
    printing_edition_obj = print_obj.edition
    set_name_rf = '-'.join(printing_set_obj.name.split(' '))
    card_name_rf = '-'.join(card_obj.name.split(' '))
    if printing_set_obj.setprinting_set.values()[0]['initial_release_date'] \
            < datetime.strptime(RELEASE_DATE_BREAKPOINT, '%Y-%m-%d').date():
        if printing_set_obj.id in ALPHA_SETS:
            attr_dict = {'set_name': set_name_rf,
                         'card_edition_name': printing_edition_obj.name,
                         'card_name': card_name_rf,
                         'set_id': print_obj.id,
                         'alpha_print': True,
                         'foiling': print_obj.foiling.id, }
            if printing_edition_obj.id != 'A':
                attr_dict['printing_edition'] = printing_edition_obj.id
        else:
            attr_dict = {'set_name': set_name_rf,
                         'card_edition_name': printing_edition_obj.name,
                         'printing_edition': printing_edition_obj.id,
                         'card_name': card_name_rf,
                         'set_id': print_obj.id,
                         'old_print': True,
                         'foiling': print_obj.foiling.id, }
    # TODO pitch should be included for scrapping lower rarity cards
    else:
        foiling = print_obj.foiling
        attr_dict = {'set_name': set_name_rf,
                     'card_name': card_name_rf,
                     'old_print': False,
                     'foiling': foiling.name if foiling.name != 'Standard' else 'Regular', }
    scrapped_card_info = scrap_cm(**attr_dict)
    if not scrapped_card_info:
        return card_printing_pk
    result_dict[0] = scrapped_card_info
    return str(result_dict)
