import datetime
import math

def next_week_days(d):
    # printing original date
    # print("The original date is : " + d.strftime('%Y-%m-%d'))
    # initializing weekday index
    weekday_idx = 0
    # computing delta days
    days_delta = weekday_idx - d.weekday()
    if days_delta <= 0:
        days_delta += 7
    # adding days to required result
    res = d + datetime.timedelta(days_delta)
    # printing result
    ret = []
    ret.append(res.strftime('%Y-%m-%d'))
    ret.append((res+datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
    ret.append((res+datetime.timedelta(days=2)).strftime('%Y-%m-%d'))
    ret.append((res+datetime.timedelta(days=3)).strftime('%Y-%m-%d'))
    ret.append((res+datetime.timedelta(days=4)).strftime('%Y-%m-%d'))
    return ret

def is_number(v):
    r = True
    try:
        v = float(v)
        r = False if math.isnan(v) else True
    except:
        r = False
    return r