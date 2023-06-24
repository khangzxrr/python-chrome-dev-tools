import kdp

import time

devtool = kdp.Kdp()

devtool.launch_chrome()

print('yeah')

devtool.navigate('https://example.com/')

# a_element = devtool.find_element_by_selector('a')

# href_attribute = devtool.get_attribute(a_element, 'href') 
# print(href_attribute)

# devtool.open_new_tab()

# window_handles = devtool.get_window_handles() 

# devtool.switch_to_window(window_handles[0])

# current_handle = devtool.get_current_window()
# print(current_handle)

# devtool.navigate('https://google.com')

# devtool.close()

# window_handles = devtool.get_window_handles() 

# devtool.switch_to_window(window_handles[0])

# h1_element = devtool.find_all_element_by_xpath('/html/body/div/h1')

# print(h1_element[0])




