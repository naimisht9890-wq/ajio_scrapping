import time
import csv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = None
scraped_links = set()

try:
    # Start Chrome
    driver = uc.Chrome(version_main=149)
    driver.maximize_window()

    driver.get("https://www.ajio.com/men-backpacks/c/830201001")

    wait = WebDriverWait(driver, 20)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.item"))
    )

    # Create CSV
    file = open(
        "Ajio_Backpacks.csv",
        "w",
        newline="",
        encoding="utf-8"
    )

    writer = csv.writer(file)

    writer.writerow([
        "Brand",
        "Product Name",
        "Price",
        "Rating",
        "Reviews",
        "Image URL",
        "Product Link"
    ])

    file.flush()

    print("\nStarted Scraping...")
    print("Press CTRL + C anytime to stop.\n")

    previous_count = 0
    same_count = 0
    total_scraped = 0

    while True:

        products = driver.find_elements(By.CSS_SELECTOR, "div.item")

        # Scrape all newly loaded products
        for product in products:

            try:
                link = product.find_element(
                    By.CSS_SELECTOR,
                    "a.rilrtl-products-list__link"
                ).get_attribute("href")
            except:
                continue

            if link in scraped_links:
                continue

            scraped_links.add(link)

            try:
                brand = product.find_element(
                    By.CLASS_NAME,
                    "brand"
                ).text.strip()
            except:
                brand = ""

            try:
                name = product.find_element(
                    By.CLASS_NAME,
                    "nameCls"
                ).text.strip()
            except:
                name = ""

            try:
                price = product.find_element(
                    By.CLASS_NAME,
                    "price"
                ).text.strip()
            except:
                price = ""

            try:
                rating = product.find_element(
                    By.CSS_SELECTOR,
                    "p._3I65V"
                ).text.strip()
            except:
                rating = ""

            try:
                reviews = product.find_element(
                    By.CSS_SELECTOR,
                    "div._2mae- p:last-child"
                ).text.replace("|", "").strip()
            except:
                reviews = ""

            try:
                image = product.find_element(
                    By.TAG_NAME,
                    "img"
                ).get_attribute("src")
            except:
                image = ""

            writer.writerow([
                brand,
                name,
                price,
                rating,
                reviews,
                image,
                link
            ])

            file.flush()

            total_scraped += 1

            print(
                f"Scraped : {total_scraped}",
                end="\r"
            )

        # Scroll to last product
        products = driver.find_elements(By.CSS_SELECTOR, "div.item")

        if products:
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                products[-1]
            )

        time.sleep(3)

        current_count = len(
            driver.find_elements(By.CSS_SELECTOR, "div.item")
        )

        print(
            f"\nProducts Loaded : {current_count}"
        )

        if current_count > previous_count:

            previous_count = current_count
            same_count = 0

        else:

            same_count += 1

            print("No new products...moving up")

            driver.execute_script(
                "window.scrollBy(0,-1200)"
            )

            time.sleep(2)

            driver.execute_script(
                "window.scrollBy(0,1800)"
            )

            time.sleep(4)

        # Stop after many retries
        if same_count >= 50:
            print("\nNo more products detected.")
            break

except KeyboardInterrupt:

    print("\n\nCTRL + C detected.")
    print("Stopping scraper...")

finally:

    try:
        file.close()
    except:
        pass

    if driver:
        driver.quit()

    print("\nCSV saved successfully.")
    print(f"Total Products Scraped : {len(scraped_links)}")
    print("Chrome Closed.")