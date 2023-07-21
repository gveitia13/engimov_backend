import random

from core.models import ProductCategory, WorkCategory

prefixes = ['Super', 'Ultra', 'Mega', 'Hyper', 'Extreme', 'Turbo', 'Max', 'Pro', 'Elite']
suffixes = ['Tech', 'Gear', 'Wear', 'Style', 'Trend', 'Fashion', 'Zone', 'Mart', 'Shop']

def generate_coherent_category_name():
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    return prefix + suffix

categories = [generate_coherent_category_name() for i in range(22)]
for c in categories:
    category = ProductCategory(name=c)
    category.save()

categories = [generate_coherent_category_name() for i in range(22)]
for c in categories:
    category = WorkCategory(name=c)
    category.save()
