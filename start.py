from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from database import Database


class SeleniumScraper:
    DRIVER = webdriver.Chrome()
    URL = "https://auto.ria.com/car/used/"
    DRIVER.get(URL)
    CARS_DETAIL_LINK = 'address'
    ALL_CARS_LINK = []
    TITLE = '/html/body/div[6]/div[11]/div[1]/div/h1'
    USD_PRICE = "/html/body/div[6]/div[11]/div[4]/aside/section[1]/div[1]/strong"
    MILE_AGE = "/html/body/div[6]/div[11]/div[4]/aside/section[1]/div[3]"
    USERNAME = '//*[@id="userInfoBlock"]/div[1]/div/h4'
    PHONE = '/html/body/div[12]/div/div[2]/div[2]/div[2]'
    IMAGE_URL = '//*[@id="photosBlock"]/div[2]/div[1]/a[2]/picture/img'
    TOTAL_IMAGE_COUNT = '/html/body/div[6]/div[11]/div[4]/main/div[1]/div[1]/div[2]/span/span[2]'
    CAR_NUMBER = '/html/body/div[6]/div[11]/div[4]/main/div[2]/div[2]/div[1]/div[2]/span[1]'
    VIN_CODE = 'vin-code'
    ALT_VIN_CODE = "label-vin"
    NEXT_PAGE = '/html/body/div[11]/section[2]/div[1]/div[4]/nav/span[10]/a'
    LINKED = '/html/body/div[11]/section[2]/div[1]/div[4]/nav/span[10]/a [href]'
    CLICKER = "/html/body/div[6]/div[11]/div[4]/aside/section[2]/div[2]/div/span/a"
    CURRENT_PAGE = "/html/head/link[73]"
    ALL_ITEM = []

    def __init__(self) -> None:
        self.database = Database()

    def get_all_cars_link(self):
        cars = self.DRIVER.find_elements(By.CLASS_NAME, self.CARS_DETAIL_LINK)
        for value in cars:
            self.ALL_CARS_LINK.append(value.get_attribute('href'))

    def get_detail_info(self):
        for car in self.ALL_CARS_LINK:
            self.DRIVER.get(car)
            link = car
            title = self.DRIVER.find_element(By.XPATH, self.TITLE).text
            usd_price = self.DRIVER.find_element(By.XPATH, self.USD_PRICE).text
            mile_age = self.DRIVER.find_element(By.XPATH, self.MILE_AGE).text
            username = self.DRIVER.find_element(By.XPATH, self.USERNAME).text
            image = self.DRIVER.find_element(By.XPATH, self.IMAGE_URL).get_attribute('src')
            total_image_count = self.DRIVER.find_element(By.XPATH, self.TOTAL_IMAGE_COUNT).text
            try:
                car_number = self.DRIVER.find_element(By.XPATH, self.CAR_NUMBER).text
            except NoSuchElementException:
                car_number = None
            try:
                vin_code = self.DRIVER.find_element(By.CLASS_NAME, self.VIN_CODE).text
            except NoSuchElementException:
                vin_code = self.DRIVER.find_element(By.CLASS_NAME, self.ALT_VIN_CODE).text
            clicker = self.DRIVER.find_element(By.XPATH, self.CLICKER)
            clicker.click()
            phone = self.DRIVER.find_element(By.XPATH, self.PHONE).text
            data = (
                link,
                title,
                usd_price,
                mile_age,
                username,
                phone,
                image,
                total_image_count,
                car_number,
                vin_code,
            )
            self.ALL_ITEM.append(data)
        self.database.insert_data(self.ALL_ITEM)

    def get_next_page(self):
        self.DRIVER.get(self.URL)
        while TimeoutException:
            try:
                next_page = self.DRIVER.execute_script("arguments[0].click();", WebDriverWait(self.DRIVER, 2).until(
                    EC.element_to_be_clickable((By.XPATH, self.NEXT_PAGE))))
                current_page = self.DRIVER.find_element(By.XPATH, self.CURRENT_PAGE).get_attribute('href')
                self.URL = current_page
            except TimeoutException:
                print('No more pages')
                break

    def main(self):
        self.get_all_cars_link()
        self.get_next_page()
        self.get_detail_info()
        self.DRIVER.quit()


if __name__ == "__main__":
    selen = SeleniumScraper()
    selen.main()
