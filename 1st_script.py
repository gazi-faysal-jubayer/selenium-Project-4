from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://mobilityex.com/#/search?svc=Moving%20Services%20Company%20&sort=companylegalname,asc&range=50&mocs=104&assocs=800&query=q%3D%204&spc=10")
driver.implicitly_wait(10)

links_list = []
def sub():
    # Find all 'a' tags matching the specific format
    filtered_links = driver.find_elements(By.XPATH, "//a[@ui-sref='searchdetails({id:sp.id})' and @ng-click=\"vm.generateEventGa4('IAMX Profile', {'sp_results_profile': sp.companylegalname, 'sp_legal_name': sp.companylegalname})\" and @analytics-on='click' and @analytics-event='Navigate to Profile Page' and @analytics-label]")

    # Extract the href attribute from each filtered link
    for link in filtered_links:
        href = link.get_attribute('href')
        links_list.append(href)

pages = []

for j in range(66):
# while True:
    try:
        # Find the active page number
        active_page_number = driver.find_element(By.CSS_SELECTOR, "#left > ul > li.pagination-page.active > a").text
        if active_page_number in pages:
            break
        
        print(active_page_number)
        sub()
        
        pages.append(active_page_number)
        
        # # Find the <ul> element with class "pagination"
        # pagination_ul = driver.find_element(By.CLASS_NAME,"pagination")

        # # Find all <li> elements within the <ul> using XPath
        # li_elements = pagination_ul.find_elements(By.XPATH,".//li")
        # if len(li_elements)==1:
        #     break

        # # Construct the XPath for the next page
        next_page_xpath = "#left > ul > li.pagination-next > a"

        # # Check if the next page element exists
        next_page_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, next_page_xpath)))

        driver.execute_script("arguments[0].click();", next_page_element)
        time.sleep(3)
        # Wait until the spinner disappears
        # WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'sb_loading')))

    except (TimeoutException, StaleElementReferenceException) as e:
        # print(f"Exception: {e}")
        # print(f"Element for page {int(active_page_number) + 1} not found. Exiting the loop.")
        break

    time.sleep(10)

# Close the WebDriver
driver.quit()

# Create a DataFrame from the list of links
df = pd.DataFrame(links_list, columns=['Links'])

# Save the DataFrame to a CSV file
df.to_csv('filtered_links.csv', index=False)