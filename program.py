import kdp

import time

devtool = kdp.Kdp()

#supply arguments ================================
devtool.launch_chrome('--disable-infobars')
#===================================================


#navigate to google get a href

print('navigate to google.com')

devtool.navigate('https://google.com')

a_element = devtool.find_element_by_selector('a')
href_attribute = devtool.get_attribute(a_element, 'href') 
print(href_attribute)

#======= navigate to example.com first a href

devtool.navigate('https://example.com/')

current_handle = devtool.get_current_window()

a_element = devtool.find_element_by_selector('a')

href_attribute = devtool.get_attribute(a_element, 'href') 
print(href_attribute)

#=======================

devtool.open_new_tab()
5
window_handles = devtool.get_window_handles() 

devtool.switch_to_window(window_handles[0])

devtool.navigate('https://mdbootstrap.com/docs/standard/forms/checkbox/')


boat_checkbox = devtool.find_element_by_id('flexCheckChecked')
devtool.click_by_css_selector('#flexCheckDefault')

#default checked, click again to uncheck then check again!
devtool.click_by_css_selector('#flexCheckChecked')
devtool.click_by_css_selector('#flexCheckChecked')

#=======================================================

devtool.execute_script('alert("click here to continue");')

#=========================================================
print(devtool.current_url())

#=======================================================


print(devtool.get_cookies())

print(devtool.delete_all_cookies())

#=======================================================

devtool.maximize_window()

#=======================================================

devtool.close()

