import random
import string

from core.models import ProductCategory, WorkCategory, Product, Work, Testimonial

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

adjectives = ['Sleek', 'Durable', 'Portable', 'Innovative', 'Stylish', 'Eco-friendly', 'Affordable', 'High-quality',
              'Versatile']
nouns = ['Phone', 'Laptop', 'Backpack', 'Headphones', 'Speaker', 'Watch', 'Camera', 'Tablet', 'Keyboard']


def generate_product_name():
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return adjective + " " + noun


def generate_product_description(name):
    return "This is a description of the {} product.".format(name)


def generate_product_price():
    return round(random.uniform(10, 1000), 2)


def generate_product_visible():
    return random.choice([True, False])


def generate_random_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


def generate_unique_sku():
    while True:
        sku = generate_random_string()
        if not Product.objects.filter(sku=sku).exists():
            return sku


def generate_product_category():
    categories = ProductCategory.objects.all()
    return random.choice(categories)


for i in range(50):
    name = generate_product_name()
    description = generate_product_description(name)
    price = generate_product_price()
    visible = generate_product_visible()
    sku = generate_unique_sku()
    category = generate_product_category()

    product = Product(
        name=name,
        description=description,
        price=price,
        visible=visible,
        sku=sku,
        category=category
    )
    product.save()

images = ['works/producto10.jpeg', 'works/producto1.jpeg', 'works/producto3.jpeg', 'works/producto4.jpeg',
          'works/producto5.jpeg']
adjectives = ['Sleek', 'Durable', 'Portable', 'Innovative', 'Stylish', 'Eco-friendly', 'Affordable', 'High-quality',
              'Versatile']
nouns = ['Sculpture', 'Painting', 'Drawing', 'Photograph', 'Print', 'Collage', 'Mosaic', 'Tapestry']


def generate_work_name():
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return adjective + " " + noun


def generate_work_description(name):
    return "This is a description of the {} work.".format(name)


def generate_work_category():
    categories = WorkCategory.objects.all()
    return random.choice(categories)


for i in range(50):
    name = generate_work_name()
    description = generate_work_description(name)
    category = generate_work_category()

    work = Work(
        name=name,
        description=description,
        category=category,
        image=random.choice(images)
    )
    work.save()

names = ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve', 'Frank', 'Grace', 'Heidi']
testimonials = ['Great work!', 'Amazing!', 'Incredible!', 'Fantastic!', 'Beautiful!', 'Stunning!', 'Impressive!',
                'Marvelous!']


def generate_testimonial_name():
    return random.choice(names)


def generate_testimonial_testimonial():
    return random.choice(testimonials)


def generate_testimonial_work():
    works = Work.objects.all()
    return random.choice(works)


for i in range(50):
    name = generate_testimonial_name()
    testimonial = generate_testimonial_testimonial()
    work = generate_testimonial_work()

    testimonial = Testimonial(
        name=name,
        testimonial=testimonial,
        work=work
    )
    testimonial.save()

for testimonial in Testimonial.objects.all()[:20]:
    testimonial.url = "https://www.engimov.pt/es/contactos"
    testimonial.save()
