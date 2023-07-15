from colorama import Fore, Style


def get_element_data(driver=None, selector=None, prop=None):
    if driver is None or selector is None:
        return ''
    print(Fore.WHITE + '-- get_element_data')
    try:
        if prop is not None:
            return driver.find_element(selector).get_property(prop).strip().split("\n")[0]
        else:
            return driver.find_element(selector).get_property('innerText').strip().split("\n")[0]
    except:
        pass
    print(Fore.RED + 'cannot get element')
    print(Style.RESET_ALL)
    return ''


def get_elements_data(driver=None, selector=None, prop=None):
    if driver is None or selector is None:
        return
    print(Fore.WHITE + '-- get_elements_data')
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
