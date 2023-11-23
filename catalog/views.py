from django.shortcuts import render
from .models import CarBrand, CarModel
from .forms import BrandSelectionForm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


URL = 'https://auto.ru/catalog/cars/'


def show_brand_models(request):
    """
    This function renders a template with a form that allows you to select
    a brand name and get a list of related models.
    :param request: Django request object.
    :return: render function with parameters.
    """
    form = BrandSelectionForm()
    if request.method == 'POST':
        form = BrandSelectionForm(request.POST)
        if form.is_valid():
            selected_car_brand = form.cleaned_data['name']
            brand_id = CarBrand.objects.get(name=selected_car_brand).id
            return render(request, 'catalog/brand_models.html', {
                'form': form,
                'brand_id': brand_id,
                'model_list': CarModel.objects.filter(brand=brand_id)
            })
    return render(request, 'catalog/brand_models.html', {
        'form': form,
    })


def update_brand_models(request):
    """
    This function deletes all car brands and models from database. Then it
    parses the site and retrieves a list of car brands. For each brand, a
    list of models is collected. The obtained brands and models are recorded
    in the database.
    :param request: Django request object.
    :return: render function.
    """
    CarBrand.objects.all().delete()
    driver = get_driver()
    driver.get(URL)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    all_brands = soup.findAll('a', class_='Link_color_black')[30:381]

    for brand in all_brands:
        brand_name = brand.text.strip()
        brand_url = brand.get('href')

        for _ in range(10):
            models = get_models_from_url(brand_url)
            if models:
                break

        try:
            new_brand = CarBrand.objects.create(name=brand_name)
            for model_name in models:
                CarModel.objects.create(name=model_name, brand=new_brand)
        except Exception as e:
            print(e)

    return render(request, 'catalog/update_brand_models.html')


def get_models_from_url(url):
    """
    This function receives a link, collects matching models from the brand page and returns a list of models.
    :param url: (str). Link to the brand page with a list of models.
    :return: list of str. This is a list of collected models from given url.
    """
    driver = get_driver()
    driver.get(url)

    try:
        button = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'ModelListingFilters__button-X9Tof'))
        )
        button.click()
    except:
        print(f'nothing to click on {url}')

    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    all_models = soup.findAll('div', class_='ModelListingFilterSearchListItem-mEC55')
    model_list = []

    for model in all_models:
        model_list.append(model.text)
    return model_list


def get_driver():
    """
    This function sets the settings for the webdriver and returns it.
    :return: webdriver object
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver
