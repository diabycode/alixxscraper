import sys

from selenium import webdriver

from utils import get_store_products, get_single_product, get_stores_from_file
import cli


def main(store_url: str|None = None, file_name: str|None = None, product_url: str|None = None, limit: int|None = None, output: str = "products.csv"):
    # chrome options
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=chrome_options)

    total_products = 0
    if file_name:
        stores = get_stores_from_file(file_name)
        for store in stores:
            products = get_store_products(driver=driver, store_url=store, limit=limit, saved=True, output=output)
            total_products += len(products)
        sys.exit(0)

    if store_url:
        products = get_store_products(driver=driver, store_url=store_url, limit=limit, saved=True, output=output)
        total_products += len(products)

    if product_url:
        product = get_single_product(driver=driver, product_url=product_url, output=output)
        if product:
            total_products += 1
            
    print(f"\n{total_products} produit(s) téléchargé(s) dans {output}.")


if __name__ == "__main__":
    args = cli.args_parser()
    main(
        store_url=args.store_url,
        product_url=args.product_url,
        file_name=args.file,
        limit=args.limit,
        output=args.output
    )
    input("\nFaites ENTRER pour quitter...")

