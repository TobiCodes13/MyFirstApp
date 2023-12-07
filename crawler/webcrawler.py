
from bs4 import BeautifulSoup
from requests import Session, RequestException


URL = "https://www.pro-football-reference.com"
BOX_URL = URL+"/boxscores/"
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}

def requests_url(session: Session, url: str, retries:int = 3, timeout: int=10):
   for _ in range(retries):
      try:
         response = session.get(url=url, timeout=timeout, headers=HEADERS)
         response.raise_for_status()
         
         return response.text
      except RequestException as raised_exception:
         print(f"Die Anfrage an {url} ist fehlgeschlagen.")
         continue
   print(f"Die Anfrage an {url} ist final fehlgeschlagen.")
   return

def parse_html_to_soup(html: str) -> BeautifulSoup:
   return BeautifulSoup(html, "html.parser")

def extract_current_week_info(soup: BeautifulSoup) ->list:
   h2_element = soup.select_one("h2").text
   info_list = h2_element.split()

   return "/".join(info_list)



def main():
   http_session = Session()
   html = requests_url(session=http_session, url=BOX_URL)
   soup = parse_html_to_soup(html)
   
   key = extract_current_week_info(soup=soup)
   print(key)
 

if __name__ == "__main__":
   main()