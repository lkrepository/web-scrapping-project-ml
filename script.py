from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrapping():
    url = 'https://listado.mercadolibre.com.ar/notebooks#D[A:notebooks]'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products_html = soup.find_all('div', class_='poly-card__content')
    data = []
    for prod in products_html:
        prod_name = prod.find('h3', class_='poly-component__title-wrapper').text.strip()
        prod_price = prod.find('span', class_='andes-money-amount__fraction').text.strip()
        prod_brand = prod.find('span', class_='poly-component__brand')
        prod_disc = prod.find('span', class_='andes-money-amount__discount')
        disc = prod_disc.text.strip() if prod_disc else "No discount"
        
        data.append({
            'Prod_name': prod_name,
            'Prod_brand': prod_brand,
            'Prod_price': prod_price,
            'Prod_disc': disc
        })
    df = pd.DataFrame(data)
    df['Prod_brand'] = df['Prod_brand'].apply(lambda x: x.get_text(strip=True) if x else '').str.replace(r'[\[\]]', '', regex=True)
    df['Prod_brand'] = df['Prod_brand'].str.strip()                
    df['Prod_brand'] = df['Prod_brand'].replace('', pd.NA)         
    df['Prod_brand'] = df['Prod_brand'].fillna('Other')  
    df['Prod_price'] = df['Prod_price'].str.replace('.', '', regex=False)
    df['Prod_price'] = df['Prod_price'].astype(int)
    df['price_category'] = df['Prod_price'].apply(lambda x: 'High' if x >= 2000000  else 'Medium' if  500000 < x < 2000000 else 'Low'  )
    return df
    print(df)

def export():
    df = scrapping()
    df.to_csv('output.csv', index=False)

scrapping()
export()