# AliExpress Scraper

Un scraper pour récupérer les informations produits d'AliExpress.


## Utilisation en ligne de commande (Windows)

1. Exécutez avec python3

```bash
python src/main.py -s XXXXXXXXXX # XXXXXXXXXX URL boutique AliExpress
python src/main.py -p XXXXXXXXXX # XXXXXXXXXX URL produit AliExpress
python src/main.py -f store_list.txt # Fichier texte contenant des URLs de boutiques AliExpress
```

NB : Enrégistrez le fichier store_list.txt dans 'src/'


2. Fichier exécutable '.exe' (dossier : dist/)  
!! Packagé et testé sur Windows 10 

```bash	
dist/alixscraper/alixscraper.exe -s https://aliexpress.com/store/XXXXXXXXXX/ 
dist/alixscraper/alixscraper.exe -p https://aliexpress.com/item/XXXXXXXXXX/ 
dist/alixscraper/alixscraper.exe -f store_list.txt
```

NB : Enrégistrez le fichier store_list.txt dans 'dist/alixscraper/_internal/'


## Options

- `-s` : URL de la boutique AliExpress
- `-p` : URL du produit AliExpress
- `-l` : Limite de produits à récupérer (sur une page AliExpress)
- `-o` : Fichier de sortie (CSV)

## Exemples

```bash
python src/main.py -s https://aliexpress.com/store/2231154/
python src/main.py -p https://aliexpress.com/item/32953944390.html
python src/main.py -f store_list.txt
python src/main.py -s https://aliexpress.com/store/1102134753 -l 10 -o products.csv
```


