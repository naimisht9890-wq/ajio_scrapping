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

    # number of products already processed
    processed=0
    # Time When new products were last found
    last_new_products = time.time()
    # Count rows written since last flush
    save_counter=0
    total_scraped =0

    while True:

        products = driver.find_elements(By.CSS_SELECTOR, "div.item")

        # Process only newly loaded products
        new_products = products[processed:]

        for product in new_products:

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

            save_counter+=1

            # Flush every 50 products
            if save_counter %  100==0:
                file.flush()

            total_scraped += 1

            print(
                f"Loaded : {len(products)} | Scraped : {total_scraped}",
                end="\r",
                flush=True
            )
        processed = len(products)

        if products:
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior:'smooth',block:'center'});",
                products[-1]
            )

        time.sleep(2)

        current_count = len(products)

        print(
            f"\nProducts Loaded : {current_count}"
        )

        if current_count > previous_count:

            previous_count = current_count
            last_new_products = time.time()



        else:
            print("No new products...moving up")

            driver.execute_script(
                "window.scrollBy(0,-800)"
            )

            time.sleep(0.8)

            driver.execute_script(
                "window.scrollBy(0,1600)"
            )

            time.sleep(2)

        # Stop only if no new products appear for 2 minutes
        if time.time()-last_new_products>120:

            print("\nNo new products for 2 minutes.")
            print("Stopping Scraper...")

            break


except KeyboardInterrupt:

    print("\n\nCTRL + C detected.")
    print("Stopping scraper...")

finally:

    try:
        file.flush()
        file.close()
    except:
        pass

    if driver:
        driver.quit()

    print("\nCSV saved successfully.")
    print(f"Total Products Scraped : {len(scraped_links)}")
    print("Chrome Closed.")