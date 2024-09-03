import argparse
import sys


def _args_parser():
    parser = argparse.ArgumentParser(description="A-Express-Auto")
    parser.add_argument("-s", "--store_url", help="URL Fournisseur")  
    parser.add_argument("-p", "--product_url", help="URL produit")
    parser.add_argument("-l", "--limit", type=int, help="Limit de produits à récupérer (sur une page Fournisseur)")
    parser.add_argument("-o", "--output", help="Ficher de sortie", default="products.csv")
    parser.add_argument("-f", "--file", help="Fichier contenant des URLs de Fournisseurs") 
    return parser.parse_args()


def args_parser():
    parser = _args_parser()
    if not parser.store_url and not parser.product_url and not parser.file:
        print("Entrez un URL de Fournisseur: ")
        parser.store_url = input("URL Fournisseur: ")
    
    if parser.store_url and parser.product_url:
        print("Veuillz entrer un URL Fournisseur ou un URL de produit pas les deux.")
        sys.exit(1)

    if parser.limit and int(parser.limit) < 1:
        print("Pour la limit veuillez entrer un nombre supérieur à 0")
        sys.exit(1)
    
    if parser.store_url and "/store/" not in parser.store_url:
        print("Entrez un URL Fournisseur valide (https://aliexpress.com/store/XXXXXXXXXX/)")
        sys.exit(1)
    
    if parser.product_url and "/item/" not in parser.product_url:
        print("Entrez un URL de produit valide (https://aliexpress.com/item/XXXXXXXXXX/)")
        sys.exit(1)

    if parser.output and not parser.output.endswith(".csv"):
        print("Veuillez entrer un nom de fichier CSV valide")
        sys.exit(1)
    
    if parser.file and not parser.file.endswith(".txt"):
        print("Veuillez entrer un nom de fichier texte valide ('.txt')")
        sys.exit(1)
    
    return parser
