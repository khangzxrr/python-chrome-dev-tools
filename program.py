import kdp

import time

devtool = kdp.Kdp()

devtool.launch_chrome()

devtool.navigate('https://example.com/')

time.sleep(1)
print(devtool.find_element_by_selector('h1'))