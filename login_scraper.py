import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time


login_url = "https://quotes.toscrape.com/login"
scraping_url = "https://quotes.toscrape.com/page/{}/"

HEADERS = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


session = requests.session( )

session_response = session.get(login_url , headers=HEADERS)

soup = BeautifulSoup(session_response.text , "html.parser")

csrf_token = soup.find("input" , attrs= {"name" : "csrf_token"})["value"]


details = {

    "username" : "anyova",
    "password" : "87654321",
    "csrf_token" : csrf_token

}

login_response = session.post(login_url , data=details , headers=HEADERS)

if "logout" in login_response.text :
    print("login! succesful")

    Rows = []
    for page in range(1 , 11) :
        scraping_url = scraping_url.format(page)
        response = session.get(scraping_url , headers=HEADERS)


        soup = BeautifulSoup(response.text , "html.parser")

        content = soup.find_all("div" , attrs= {"class" : "quote"})

        for item in content :
            quotes = item.span.text
            author = item.small.text

            tags = item.find_all("a" , attrs= {"class" : "tag"})

            Tags = []
            for tag in tags :
                T = tag.text
                Tags.append(T)

            rows = {
                "Quote" : quotes,
                "Author" : author,
                "Tags" : Tags
            }

            Rows.append(rows)

        time.sleep( 5 )

    df = pd.DataFrame(Rows)

    print(df)

else :
    print("login failed")


    


