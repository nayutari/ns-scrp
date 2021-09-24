import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ENGINE_URL = "https://www.google.com/"

class Driver:
    def __init__(self):
        self.wait_sec = 2.0
        self.driver = None

    def setup(self, driver_path):
        option = Options()
        option.add_argument("--headless")

        self.log("run chrome")
        self.log(driver_path)
        self.driver = webdriver.Chrome(driver_path, options=option)
        time.sleep(self.wait_sec)

    def scraping_total_number(self, keywords):
        self.driver.get(ENGINE_URL)
        search = self.driver.find_element_by_name('q')
        keyword = " ".join(keywords)
        search.send_keys(keyword)
        time.sleep(self.wait_sec)

        search.submit()
        time.sleep(self.wait_sec)

        results = self.driver.find_elements_by_id("result-stats")

        result_num = 0

        if len(results) > 0:
            result_num = self.result_to_num(results[0].text)
        else:
            nexts = self.driver.find_elements_by_css_selector("div#rcnt tr td a.fl")
            if len(nexts) > 0:
                self.log("nothing first page, testing second page.")
                nexts[0].click()
                time.sleep(self.wait_sec)

                results = self.driver.find_elements_by_id("result-stats")
                if len(results) > 0:
                    result_num = self.result_to_num(results[0].text)
        
        return result_num

    def result_to_num(self, result):
        result_num = re.findall(r"約(.*)件", result)
        result_num = re.sub(r"[, ]", "", result_num[0])
        return int(result_num)

    def log(self, s):
        print(s)

    def __del__(self):
        self.driver.quit()
