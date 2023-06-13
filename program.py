import kdp

import time

devtool = kdp.Kdp()

devtool.launch_chrome()

devtool.navigate('https://google.com')

print(devtool.find_element_by_id('qbc'))