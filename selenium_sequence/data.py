from traceback import print_tb
from colorama import Fore, Style
from selenium_driver import SeleniumDriver


def get_element_data(driver=None, selector=None, prop=None) -> str:
    if driver is None or selector is None:
        return ''
    
    value = ''
    try:
        value = str(
            driver.
            find_element(selector).
            get_property(prop if prop is not None else 'innerText')).strip().split("\n")[0]
    except:
        print(Fore.RED + 'cannot get element')
   
    return value


def get_elements_data(driver=None, selector=None, prop=None) -> list:
    # print('get_elements_data')
    if driver is None:
        print(Fore.RED + "Missing driver")
        return []
    if selector is None:
        print(Fore.RED + "Missing selector")
        return []

    data = []

    # print(f'selector: {selector}')
    elements = driver.find_elements(selector)
    if type(elements) != list:
        print(Fore.RED + "No such elements")
        return []

    for el in elements:
        if prop is not None:
            value = el.get_property(prop)
            data.append(value)
        else:
            value = el.get_property('innerText')
            data.append(value)
    # print(elements)

    return data
