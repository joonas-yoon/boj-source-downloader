from util import Chrome, get_text

driver = Chrome().get_driver()
driver.implicitly_wait(3)

driver.quit()
