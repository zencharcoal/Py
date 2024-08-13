import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    s = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver

def scan_urls(urls):
    driver = load_driver()
    for url in urls:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print(f"Scanning {url}...")

        # Fetch all script elements
        scripts = driver.find_elements(By.TAG_NAME, 'script')
        for script in scripts:
            script_content = script.get_attribute('innerHTML')
            if script_content:  # Checking if the script tag has inline content
                if "ajax" in script_content or "XMLHttpRequest" in script_content or "fetch(" in script_content:
                    print(f"Potential AJAX or API call found in script at {url}:")
                    print(script_content[:200])  # Print first 200 characters to check

    driver.quit()

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <url_list.txt> OR <url1> <url2> ...")
        sys.exit(1)

    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], 'r') as file:
                urls = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print("File not found. Exiting.")
            sys.exit(1)
    else:
        urls = sys.argv[1:]

    scan_urls(urls)

if __name__ == "__main__":
    main()

