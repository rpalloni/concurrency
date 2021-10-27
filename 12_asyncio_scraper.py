import asyncio
import httpx
import bs4
from colorama import Fore


def get_data(html: str, num_prod: int) -> str:
    print(Fore.CYAN + f'Product number: {num_prod}', flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    descr = soup.find('p', class_='description')
    price = soup.find('h4', class_='pull-right price')
    
    if not price:
        return 'MISSING'

    return descr.text.strip() + ' - ' + price.text.strip()


async def get_html(num_prod: int) -> str:
    print(Fore.YELLOW + f'Getting HTML for product {num_prod}', flush=True)

    url = f'https://www.webscraper.io/test-sites/e-commerce/allinone/product/{num_prod}'

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status() # check status

        return resp.text


async def get_range_products():

    tasks = []

    for n in range(500, 550):
        tasks.append((n, asyncio.create_task(get_html(n))))

    for n, t in tasks:
        html = await t
        product = get_data(html, n)
        print(Fore.WHITE + f'Product: {product}', flush=True)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_range_products())