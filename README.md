# web-accessibility-MDST

Web Accessibility team project for MDST (Winter 2021).

Link to [writeup](https://www.mdst.club/projects/web-accessibility)

Purpose: to score and rank a dataset of U-M LSA websites based on their conformance to web accessibility standards using a custom-made scoring metric and online evaluation tools.

- Web scrapers (img.py and main.py) were developed with Python and Selenium.
  - main.py: web scraper to scrape site results from accessi.org.
  - img.py: web scraper to scrape image alternate tag results from https://www.digitalsales.com/alt-tag-checker.
- LSA.csv is the input dataset of U-M LSA websites*; the sorted CSV files are the cleaned datasets used for output and visualization.
- data_collection.ipynb (Jupyter Notebook) takes in the sorted output CSV files and creates the visualizations.

Credits to the wonderful team behind it all: Iris Derry, Renee Li, Myla Semanison, Nitish Vijai, Zach Breger, Vedant Iyer, Peter Zhang, Nishka Muzumdar, Kim Di Camillo, Skye Du, and Joseph Wentzel!

(*) Note: There are some minor discrepancies between this dataset and the one used in the final version.
