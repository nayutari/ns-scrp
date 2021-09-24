import nslib.scrp as scrp

driver = scrp.Driver()
driver.setup("bin/chromedriver-94-win.exe")

v = driver.scraping_total_number(["tokyo", "lunch"])
print(v)
