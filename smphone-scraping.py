# importing the required libraries
import requests
from bs4 import BeautifulSoup
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

jumia_smphone_link = 'https://www.jumia.co.ke/smartphones/' # many other pages https://www.jumia.co.ke/smartphones/?page=2wq11Q#catalog-listing

# function to save the data obtained
def save_product_data(product_details):
    print(product_details)
    # for i in product_details:
    #     pass
    # print(type(i))
    
    
def get_product_details(detail):
    phone_name = detail.find('h3', {'class':'name'})
    phone_name = phone_name.text # phone name
    phone_name = re.split(r',|\-|;|//|–', phone_name)
    phone_name = phone_name[0]
    
    # phone selling price
    price = detail.find('div', {'class':'prc'})
    selling_price = price.text
    
    # phone previous price
    original_price = detail.find('div', {'class':'old'})
    if not original_price:
        original_price = ''
    else:
        original_price = original_price.text
    
    # discount on phone
    discount = detail.find('div', {'class':'tag _dsct _sm'})
    if not original_price:
        discount = ''
    else:
        discount = discount.text
    
    
    # find the link to each of the phone
    phone_url = detail.find('a', {'class':'core'}, href=True)
    phone_url = phone_url['href']
    full_phone_url = base_url + phone_url
    
    # print(phone_name, selling_price, original_price, discount)
    # print('\n')
    
    # now that we have the url link to each product, we will scrape each of the pages for more info
    more_response = requests.get(full_phone_url, headers = headers)
    more_soup = BeautifulSoup(more_response.text, 'html.parser')
    brand = more_soup.find_all('a', {'class':'_more'})
    brand = brand[1].text
    
    #getting the product's specifications / features
    specs = more_soup.find('div', {'class':'markup -pam'})
    features = specs.find_all('li')
    all_specs = ''
    for spec in features:
        spec = spec.text
        if '\xa0' in spec:
            spec = spec.replace('\xa0', '')
        if not all_specs:
            all_specs += spec
        else:
            all_specs += ', ' + spec
    
    # getting the product rating
    product_ratings = more_soup.find('div', {'class':'-fs29 -yl5 -pvxs'})
    if not product_ratings:
        product_rating = ''
    else:
        product_rating = product_ratings.text
    
    people_rated = more_soup.find('p', {'class':'-fs16 -pts'})
    if not people_rated:
        number_of_verified_ratings = ''
    else:
        number_of_ratings = people_rated.text.split(' ')
        number_of_verified_ratings = number_of_ratings[0]
    
    # getting the seller information details
    card_info = more_soup.find_all('section', {'class': 'card'})
    seller_info = card_info[1]
    seller_info_details = seller_info.find('div', {'class':'-hr -pas'})
    #name of the seller
    seller_name = seller_info_details.find('p', {'class':'-m -pbs'})
    seller_name = seller_name.text
    # seller score
    score = seller_info_details.find('bdo', {'class':'-m -prxs'})
    seller_score = score.text
    # number of followers that the seller has
    followers = seller_info_details.find('span', {'class':'-m'})
    seller_followers = followers.text
    ### Seller permormance
    seller_performance = seller_info.find_all('div', {'class':'-df -i-ctr -pts'})
    # order fulfillment rate
    order_fulfillment_rate = seller_performance[0].text.split('\xa0')
    order_fulfillment_rate = order_fulfillment_rate[-1]
    # Quality Score
    quality_score = seller_performance[1].text.split('\xa0')
    quality_score = quality_score[-1]
    # customer rating
    customer_rating = seller_performance[-1].text.split('\xa0')
    customer_rating = customer_rating[-1]
    # warranty
    warranty = card_info[0].find_all('div', {'class':'-df -d-co -c-bet'})
    warranty = warranty[-1].text.replace('Warranty', '')
    warranty = warranty.replace('\xa0', '')
    
    return {
        'Phone Name': phone_name,
        'Brand': brand,
        'Original Price': original_price,
        'Selling Price': selling_price,
        'Discount': discount,
        'Specifications/Features': all_specs,
        'Warranty': warranty,
        'Product Ratings': product_rating,
        'Number of Verified Ratings': number_of_verified_ratings,
        'Seller Name': seller_name,
        'Seller Score': seller_score,
        'Seller Followers': seller_followers,
        "Seller's Order Fulfillment Rate": order_fulfillment_rate,
        "Seller's Quality Score": quality_score,
        "Seller's Customer Rating": customer_rating,
        "Purchase Link": full_phone_url
    }
    print(phone_name)

def get_products(soup):
    class_name = 'prd _fb col c-prd'
    # let's parse through each phone to get its name
    phone_wrap = soup.find_all('article', {'class':class_name})
    print(f'A total of {len(phone_wrap)} items were found on the first page', '\n')
    product_details = [get_product_details(detail) for detail in phone_wrap]
    
    # function to save the data as a dictionary
    save_data = save_product_data(product_details)
    return product_details

def get_response(link):
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
        
    # calling the get_products function
    products = get_products(soup)
    return products


# base website URL
base_url = 'https://www.jumia.co.ke'

    
if __name__ == "__main__":    

    response = [get_response(link=f'https://www.jumia.co.ke/smartphones/?page={link}#catalog-listing') for link in range(1,5)]
    #print(response)
    
    #print(f'Found {len(videos)} videos')
    
    # title, url, thumbnail_url, channel, views, uploaded, description
    # videos_data = [parse_video(video) for video in videos]
    
    # print(videos_data[-1])
    # print('\n')
    
    # # saving videos as CSV
    # print("Saving data to a CSV")
    # videos_df = pd.DataFrame(videos_data)
    # print(videos_df)
    # videos_df.to_csv('trending.csv')
    
