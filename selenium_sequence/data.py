from colorama import Fore, Style


def get_element_data(driver=None, selector=None, prop=None) -> str:
    if driver is None or selector is None:
        return ''
    # print(Fore.WHITE + '-- get_element_data')
    value = ''
    try:
        value = str(
            driver.
            find_element(selector).
            get_property(prop if prop is not None else 'innerText')).strip().split("\n")[0]
        
        print(Fore.GREEN + value)
        # if prop is not None:
        #     return str(driver.find_element(selector).get_property(prop)).strip().split("\n")[0]
        # else:
        #     return str(driver.find_element(selector).get_property('innerText')).strip().split("\n")[0]
    except:
        print(Fore.RED + 'cannot get element')
   
    return value


def get_elements_data(driver=None, selector=None, prop=None) -> list:
    if driver is None or selector is None:
        return []
    # print(Fore.WHITE + '-- get_elements_data')
    data = []
    # time.sleep(2)
    elements = driver.find_elements(selector)
    for el in elements:
        if prop is not None:
            value = el.get_property(prop)
            data.append(value)
        else:
            value = el.get_property('innerText')
            data.append(value)
    return data
