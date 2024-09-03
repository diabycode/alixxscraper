import time
import re
from pathlib import Path
import sys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver 
from selenium.common.exceptions import NoSuchElementException

from constants import BASE_URL, DOWNLOAD_PATH


def wait_for_element(driver, search_by, search_value, timeout=10, 
                     not_found_text="Élément introuvable"):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((search_by, search_value))
        )
    except TimeoutException:
        print(f"!!Warning [{driver.current_url.split('?')[0]}]:", not_found_text)
        element = None
    return element


def _get_product_pricing(driver):
    current_price = wait_for_element(driver, By.CLASS_NAME, "price--current--I3Zeidd", not_found_text="Prix produit introuvable") 
    if current_price:
        current_price = re.search(r"\$(\d+\.\d+)", current_price.text.strip())
    return current_price.group(1) if current_price else ""


def _get_product_keywords(driver):
    keywords = []
    keywords_dom = wait_for_element(driver, By.CLASS_NAME, "cross-link--crossLink--D6lKnhz", not_found_text="Mots clés produit introuvable")
    if keywords_dom:
        keys_a = keywords_dom.find_elements(By.TAG_NAME, "a")
        for key in keys_a:
            keywords.append(key.text.strip())
    return keywords


def _get_product_images(driver):
    images = []
    images_wrapper = wait_for_element(driver, By.ID, "nav-description", not_found_text="Images produit introuvable")
    if images_wrapper:
        t = 0
        while t < 5:
            try:
                images_wrapper.find_element(By.TAG_NAME, "button").click()
                time.sleep(5)
                images_found = images_wrapper.find_elements(By.CSS_SELECTOR, "img") 
                if images_found:
                    for image in images_found:
                        images.append(image.get_attribute("src"))
            except:
                pass

            if images:
                break
            time.sleep(3)
            t += 1
    return images


def _get_product_variants(driver):
    variants = []

    # wrapper
    variants_dom = wait_for_element(
        driver=driver, 
        search_by=By.CLASS_NAME, 
        search_value="sku-item--wrap--t9Qszzx", 
        not_found_text="Variantes produit introuvable"
    )
    
    if variants_dom:
        varient_element_list = variants_dom.find_elements(By.CLASS_NAME, "sku-item--property--HuasaIz") 
        for variant in varient_element_list:
            product_variant = {}
            v_name = variant.find_element(By.CLASS_NAME, "sku-item--title--Z0HLO87").text.strip()
            product_variant["name"] = v_name
            
            v_values = []
            v_values_dom = variant.find_element(By.CLASS_NAME, "sku-item--skus--StEhULs") \
                            .find_elements(By.TAG_NAME, "div")
            for v in v_values_dom:
                try:
                    value = v.find_element(By.TAG_NAME, "img").get_attribute("src")
                except NoSuchElementException:
                    v_values.append(v.text.strip())
                else:
                    v_values.append(value)
            product_variant["values"] = v_values
        
            variants.append(product_variant)
    return variants


def get_product_infos(driver: WebDriver, product_url: str) -> dict:
    driver.get(product_url)
    product_infos = {}
    title = wait_for_element(driver, By.TAG_NAME, "h1", not_found_text="Produit introuvable")
    if not title:
        return product_infos
    product_infos["title"] = title.text.strip() if title else ""
    product_infos["pricing"] = _get_product_pricing(driver)
    product_infos["variants"] = _get_product_variants(driver)
    product_infos["keywords"] = _get_product_keywords(driver)
    product_infos["images"] = _get_product_images(driver)
    return product_infos


def _get_store_id_through_url(url: str):
    # https://fr.aliexpress.com/store/{id}/
    store_id = re.search(r"store/(\d+)", url)
    if store_id:
        return store_id.group(1)


def _get_store_products_url(driver: WebDriver, store_url: str, limit: int | None = None) -> list:
    starting_title = "\nRécupération des produits de la boutique : " + store_url
    if limit:
        starting_title += f"\nLimité à {limit} produits"
    print(starting_title)

    product_list = []
    store_id = _get_store_id_through_url(store_url)
    if not store_id:
        return product_list
    url = BASE_URL + "store/" + store_id + "/pages/all-items.html"
    driver.get(url)

    # pagination
    pagignation_wrapper = wait_for_element(driver, By.XPATH, "//*[@id=\"right\"]/div/div[4]/div", not_found_text="Pagination introuvable")
    if pagignation_wrapper:
        current_page = pagignation_wrapper.get_attribute("currentpage")
        total_pages = pagignation_wrapper.get_attribute("totalpage")
        current_page = int(current_page) if current_page and current_page.isdigit() else 1
        total_pages = int(total_pages) if total_pages and total_pages.isdigit() else 1
        if current_page > total_pages:
            current_page = 1
            total_pages = 1
    else:
        total_pages = 1
        current_page = 1

    while True:
        if current_page > total_pages:
            break
        
        products_wrapper = wait_for_element(driver, By.XPATH, "//*[@id=\"right\"]/div/div[3]", not_found_text="Produits introuvable")
        if products_wrapper:
            products = products_wrapper.find_elements(By.TAG_NAME, "a")
            for product in products:
                product_url = product.get_attribute("href")
                product_list.append(product_url)
                if limit and len(product_list) >= limit:
                    break
            if limit and len(product_list) >= limit:
                break

        next_btn = wait_for_element(driver, By.XPATH, "//*[@id=\"right\"]/div/div[4]/div/div[6]", not_found_text="Bouton suivant introuvable")
        if next_btn:
            next_btn.click()
            time.sleep(5)
            current_page += 1
        else:
            break
    
    if len(product_list) == 0:
        print("0 produit trouvé!")
        sys.exit(1)
    return product_list


def get_store_products(driver: WebDriver, store_url: str, limit: int | None = None, 
                       saved: bool = False, output: str="products.csv") -> list:
    product_urls = _get_store_products_url(driver, store_url, limit=limit)
    if limit:
        product_urls = product_urls[:limit]

    print(len(product_urls), "produit(s) trouvé(s).")

    products = []
    for url in product_urls:
        product = get_product_infos(driver, url)
        if product and saved:
            _write_products_to_csv([product], output)
            products.append(product)
    return products


def flat_list(nested_list):
    flated_list = []
    for i in nested_list:
        if type(i) == list:
            flated_list.extend(flat_list(i))
        else:
            flated_list.append(i)
    return flated_list


def _write_products_to_csv(products: list, csv_file_name: str):
    DOWNLOAD_PATH.mkdir(exist_ok=True)
    csv_file = DOWNLOAD_PATH / csv_file_name
    if not csv_file.exists():
        csv_file.touch()

    # csv heading if not exists
    if not csv_file.read_text():
        with open(csv_file, "w") as f:
            f.write("title,pricing,variants,keywords,images")

    with open(csv_file, "a") as f:
        for product in products:
            product_line = f"{product['title'].replace(',','')},"
            product_line += f"${product['pricing']},"
            variants = flat_list([v["values"] for v in product['variants']])
            product_line += ";".join(variants) + ","
            product_line += ";".join(product['keywords']) + ","
            product_line += ";".join(product['images'])
            f.write(f"\n{product_line}")
            print(f"[OK] Produit '{product['title'][:30]}...' sauvegardé", csv_file.absolute())


def get_single_product(driver, product_url: str, output: str="single_product.csv"):
    product = get_product_infos(driver, product_url)
    if product:
        _write_products_to_csv(products=[product], csv_file_name=output)
        return product


def get_stores_from_file(file_name: str):
    file = Path(__file__).parent / file_name
    if not file.exists():
        print(f"Fichier '{file_name}' introuvable")
        sys.exit(1)
    with open(file, "r") as f:
        stores = f.read().splitlines()
        print(stores)
    return stores


