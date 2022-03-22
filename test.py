from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

options = ChromeOptions()
driver = webdriver.Chrome(options=options)

driver.quit()