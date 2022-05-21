import time
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import os

website = 'https://www.emag.ro/'
class Emag_bot(webdriver.Chrome):

    def __init__(self, drive_path=service.Service("C:\SeleniumDrivers\chromedriver.exe"), teardown=False):
        self.driver_path = drive_path
        self.teardown = teardown
        options = Options()
        s = service.Service('C:\SeleniumDrivers\chromedriver.exe')
        super(Emag_bot, self).__init__(service=s, options=options)
        self.implicitly_wait(1)
        self.maximize_window()
        self.get(website)
        self.implicitly_wait(2)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def GDPR(self):
        time.sleep(3)
        try:
            gdpr = self.find_element(By.XPATH, '//button[text()="Accept"]')
            gdpr.click()
            time.sleep(2)
            xclose = self.find_element(By.CSS_SELECTOR,
                                       'body > div.gdpr-cookie-banner.js-gdpr-cookie-banner.pad-sep-xs.pad-hrz-none.login-view.login-view-ro.show > div > button > i')
            xclose.click()
        except:
            pass
        # x2close = self.find_element(By.CSS_SELECTOR, 'body > div.ns-wrap-bottom-right > div > div > button > i')
        # x2close.click()
        # time.sleep(2)

    def Searchbox(self,product=str()):

        searchbox = self.find_element(By.ID, 'searchboxTrigger')
        searchbox.send_keys(product)
        search = self.find_element(By.XPATH, '//*[@id="masthead"]/div/div/div[2]/div/form/div[1]/div[2]/button[2]')
        search.click()
        time.sleep(2)
        afisare = self.find_element(By.XPATH, '//div[@class="sort-control-btn-dropdown"]')
        afisare.click()
        time.sleep(2)
        afisare100 = self.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/section[1]/div/div[3]/div[2]/div[1]/div[5]/div/div[3]/div/div/ul/li[3]/a')
        afisare100.click()
        for_men = self.find_element(By.PARTIAL_LINK_TEXT,'Barbati')
        for_men.click()
        time.sleep(2)
        """
        We can select to display only the items that are in stock
        """
        # stoc = self.find_element(By.PARTIAL_LINK_TEXT, 'In Stoc')
        # stoc.click()
        """
        We can select a price range for items
        """
        # price_min = self.find_element(By.XPATH,
        #                               '// *[ @ id = "js-filter-6411-collapse"] / div[2] / div[2] / div[2] / input[1]')
        # price_min.clear()
        # price_min.send_keys(3900)
        # time.sleep(2)
        # price_max = self.find_element(By.XPATH,
        #                               '// *[ @ id = "js-filter-6411-collapse"] / div[2] / div[2] / div[2] / input[2]')
        # price_max.clear()
        # price_max.send_keys(2000)
        # button_price = self.find_element(By.XPATH,
        #                                  '//*[@id="js-filter-6411-collapse"]/div[2]/div[2]/div[2]/span/button/i')
        # button_price.click()
        # self.execute_script('window.scrollBy(0,10)')

    def database(self):

        time.sleep(3)
        watches = self.find_elements(By.CSS_SELECTOR, '#card_grid > div')
        watch_nr = 99
        page_nr = 2
        for watch in watches:
            time.sleep(1)
            """
            There are 100 articles on the page, then we have to move on to the next page
            """
            if watch_nr ==99:
                self.get('https://www.emag.ro/search/stoc/filter/pentru-f9777,barbati-v32/g-shock/p'+str(page_nr))
                watch_nr = 1
                self.execute_script('window.scrollBy(0,0)')
                watch_nr = 1
                self.execute_script('window.scrollBy(0,0)')
                watch2 = self.find_element(By.XPATH, "//div[contains(@data-position,'" + str(watch_nr) + "')]")
                watch2.click()
                try:
                    """
                    Not all articles have the same page structure. Some did not provide details.
                     In order not to block the script, 
                     we go further where we do not find details in the appropriate format.
                    """
                    detalii1 = self.find_element(By.XPATH,
                                                "//tr//td[@class='col-xs-8']/following::td[contains(text(),'Cod produs')]").\
                        get_attribute("innerHTML")
                    caracteristici = detalii1.split('; ')
                    columns = []
                    elements = []
                    price_all = self.find_element(By.CLASS_NAME, 'product-new-price').get_attribute('innerHTML')
                    pret = price_all.split('<')
                    columns.append('Pret')
                    elements.append(str(pret[0].replace('.', '')))
                    for i in caracteristici:
                        caract = i.split(': ')
                        columns.append(caract[0])
                        elements.append(caract[1])

                    if os.path.exists('database_g_shock.csv'):
                        with open('database_g_shock.csv', 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(elements)
                    else:
                        with open('database_g_shock.csv', 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(columns)
                            writer.writerow(elements)
                    print(elements)
                    page_nr +=1
                except:
                    pass
                watch_nr += 1
                self.back()

            else:
                pass

            watch1 = self.find_element(By.XPATH, "//div[contains(@data-position,'" + str(watch_nr) + "')]")
            watch1.click()
            price_all = self.find_element(By.CLASS_NAME, 'product-new-price').get_attribute('innerHTML')
            pret = price_all.split('<')
            try:
                """
                   Not all articles have the same page structure. Some did not provide details.
                    In order not to block the script, 
                    we go further where we do not find details in the appropriate format.
               """
                detalii = self.find_element(By.XPATH,
                                              "//tr//td[@class='col-xs-8']/following::td[contains(text(),'Cod produs')]").get_attribute(
                    "innerHTML")
                caracteristici = detalii.split('; ')
                columns = []
                elements = []
                time.sleep(3)
                price_all = self.find_element(By.CLASS_NAME, 'product-new-price').get_attribute('innerHTML')
                pret = price_all.split('<')
                columns.append('Pret')
                elements.append(str(pret[0].replace('.', '')))
                for i in caracteristici:
                    caract = i.split(': ')
                    columns.append(caract[0])
                    elements.append(caract[1])

                if os.path.exists('database_g_shock.csv'):
                    with open('database_g_shock.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(elements)
                else:
                    with open('database_g_shock.csv', 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(columns)
                        writer.writerow(elements)
                print(elements)
            except:
                pass
            watch_nr += 1
            self.back()




