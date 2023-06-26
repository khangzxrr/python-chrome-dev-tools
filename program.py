import kdp

import time

devtool = kdp.Kdp()

devtool.launch_chrome()


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

print(boat_checkbox)
# h1_element = devtool.find_all_element_by_xpath('/html/body/div/h1')

# print(h1_element[0])




