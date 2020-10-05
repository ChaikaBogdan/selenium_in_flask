#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def selenium_task(search):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    try:
        driver.get("http://www.python.org")
        assert "Python" in driver.title
        elem = driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys(search)
        elem.send_keys(Keys.RETURN)
        results = driver.find_elements_by_xpath('//*[@id="content"]/div/section/form/ul/li')
        topics = []
        for result in results:
            topics.append(result.text)
        if not topics:
            topics = ["No results"]
        return topics
    except Exception as e:
        driver.close()
        return e
    finally:
        driver.close()
