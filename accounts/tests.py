from django.test import TestCase

# # Create your tests here.
# import json

# f = open('accounts\diagnosis_codes2.json', 'r').read()
# j = json.loads(f)

# list_out = []
# list_added = []
# for i in j:
#     is_continued = False
#     for co in list_added:
#         if i.get('descr') == co:is_continued = True
#     if is_continued:
#         continue
#     list_out.append({
#         "code": i.get('code'),
#         "depth": i.get('depth'),
#         "href": i.get('href'),
#         "descr": i.get('descr')
#     })
#     list_added.append(i.get('descr'))

# open('accounts\diagnosis_codes3.json', 'w').write(json.dumps(list_out))


def get_discont_original_price(price, discont):
    price = (price/ (100-discont))*100
    return price
