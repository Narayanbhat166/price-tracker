import requests
from bs4 import BeautifulSoup


def flipkart(product_id):
    url = 'https://www.flipkart.com/product/p/itme?pid={0}'.format(product_id)

    Response = requests.get(url)

    if Response.status_code == 200:
        page = BeautifulSoup(Response.text, 'html.parser')
    else:
        print("Error")
        return

    title = ''
    price = 0
    display_price = '0'
    numberof_ratings = 0
    numberof_reviews = 0
    stars = 0

    # title
    try:
        title = page.find(class_="_35KyD6").text.strip()
    except Exception as e:
        print(
            f"Exception {sr(e)} occured while getting product title for product "+product_id)
    else:
        print("Title: ", title)

    # Price
    try:
        price = page.find(class_="_1vC4OE _3qQ9m1").text.strip()
        display_price = price
        price = int(price[1:].replace(',', '').replace('.', ''))
    except Exception as e:
        print(
            f"Exception {sr(e)} occured while getting product price for product "+product_id)
    else:
        print("Price: ", price)

    #Ratings and reviews
    try:
        ratings_span = page.find(class_="_38sUEc").find_all('span')
        numberof_ratings = int(ratings_span[1].text[:-8].replace(',', ''))
        numberof_reviews = int(ratings_span[3].text[:-8].replace(',', ''))
    except Exception as e:
        print(
            f"Exception {str(e)} occured while getting product reviews and ratings for product {product_id}")
    else:
        print("Ratings: ", numberof_ratings)
        print("Reviews: ", numberof_reviews)

    # Stars
    try:
        stars = page.find(class_='hGSR34')
    except Exception as e:
        print(
            f"Exception {str(e)} while getting product stars for product {product_id}")
    else:
        if stars is not None:
            stars = float(stars.text)
            print("Stars: ", stars)
        else:
            stars = 0

    result = {"title": title, "price": price, "ratings": numberof_ratings,
              "reviews": numberof_reviews, "stars": stars, "display_price": display_price}

    return result
