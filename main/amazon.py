import requests
from bs4 import BeautifulSoup


def amazon(product_id):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "Dnt": "1",
        "Upgrade-Insecure-Requests": "1",
    }

    url = 'https://www.amazon.in/dp/{}/'.format(product_id)

    headers["User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'

    title = None
    price = None
    display_price = '0'
    numberof_ratings = 0
    stars = 0

    result_page = requests.get(url=url, headers=headers)
    page = BeautifulSoup(result_page.text, 'html.parser')

    if page.title.text == "Robot Check":
        print("Robot check")
        return None

    # Title
    try:
        title = page.find(id='productTitle').text.strip()
    except Exception as e:
        print(
            f"Exception {str(e)} occured while getting product title for {product_id}")
    else:
        print("Title: ", title)

    # Price
    try:
        price = page.find(id='priceblock_ourprice')

        if not price:
            price = page.find(id='priceblock_dealprice')
        if not price:
            price = page.find(id='priceblock_saleprice')

        if price:
            price = price.text
            display_price = price
            price = float(price[2:].replace(',', ''))
        else:
            print(f"Price unavailable for product {product_id}")
    except Exception as e:
        print(
            f"Exception {str(e)} occured while getting product price for {product_id}")
    else:
        print("Price: ", price)

    # Stars
    try:
        stars_span = page.find(id='acrPopover')
        stars = float(stars_span.span.a.text.replace(
            '\n', '')[:3].replace(',', ''))
    except Exception as e:
        print(
            f"Exception {str(e)} occured while getting product stars for {product_id}")
    else:
        print("Stars: ", stars)

    #Ratings = Reviews
    try:
        ratings = page.find(id='acrCustomerReviewText')
        if ratings is not None:
            numberof_ratings = int(ratings.text[:-7].replace(',', ''))
        else:
            ratings = 0
    except Exception as e:
        print(
            f"Exception {str(e)} occured while getting product Ratings for {product_id}")
    else:
        print("Ratings: ", numberof_ratings)

    result = {"title": title, "price": price, "ratings": numberof_ratings,
              "reviews": numberof_ratings, "stars": stars, "display_price": display_price}

    return result
