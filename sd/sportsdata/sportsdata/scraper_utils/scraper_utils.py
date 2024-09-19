import time

from selenium.webdriver.common.action_chains import ActionChains


def scroll_to_and_click_button(driver, element, sleep_time=1) -> None:
    if element.is_displayed() and element.is_enabled():
        try:
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                element,
            )
            time.sleep(sleep_time)
            driver.execute_script("arguments[0].click();", element)
            time.sleep(sleep_time)
        except Exception as e:
            print(f"failed to click button: {str(e)}")


def scroll_to_and_click_buttons(driver, elements, sleep_time=1) -> None:
    for element in elements:
        scroll_to_and_click_button(driver, element, sleep_time)
