import datetime
import re
def genLogName():
    now_time = datetime.datetime.now()
    # strTime = datetime.datetime.strftime(now_time, )
    t = re.sub(' ', '--',str(now_time) )
    name = re.sub(r'(\:|\.)','+',t)
    name = name+'-log.log'
    return name
