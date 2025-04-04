from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def get_html(url):
    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        html = driver.page_source
        with open("output.html", "w", encoding="utf-8") as file:
            file.write(html)
        print("HTML content saved as output.html")
        driver.quit()
    except Exception as e:
        print(f"Error fetching {url}: {e}")


url = "https://x.com/Teradeportes/status/1907586515573592564"
get_html(url)
