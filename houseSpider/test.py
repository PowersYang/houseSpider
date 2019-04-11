# -*- coding: utf-8 -*-

import time, datetime

kHr = 0  # index for hour
kMin = 1  # index for minute
kSec = 2  # index for second
kPeriod1 = 0  # 时间段，这里定义了两个代码执行的时间段
kPeriod2 = 1
starttime = [[9, 30, 0], [13, 0, 0]]  # 两个时间段的起始时间，hour, minute 和 second
endtime = [[11, 30, 0], [15, 0, 0]]  # 两个时间段的终止时间
sleeptime = 5  # 扫描间隔时间，s


def DoYourWork():  # 你的工作函数
    print('Now it\'s the time to work!')


def RestYourSelf():  # 你的休息函数
    print('Now it\'s the time to take a rest!')


def T1LaterThanT2(time1, time2):  # 根据给定时分秒的两个时间，比较其先后关系
    # t1 < t2, false, t1 >= t2, true
    if len(time1) != 3 or len(time2) != 3:
        raise Exception('# Error: time format error!')
    T1 = time1[kHr] * 3600 + time1[kMin] * 60 + time1[kSec]  # s
    T2 = time2[kHr] * 3600 + time2[kMin] * 60 + time2[kSec]  # s
    if T1 < T2:
        return False
    else:
        return True


def RunNow():  # 判断现在是否工作
    mytime = datetime.datetime.now()
    currtime = [mytime.hour, mytime.minute, mytime.second]
    if (T1LaterThanT2(currtime, starttime[kPeriod1]) and (not T1LaterThanT2(currtime, endtime[kPeriod1]))) or (
            T1LaterThanT2(currtime, starttime[kPeriod2]) and (not T1LaterThanT2(currtime, endtime[kPeriod2]))):
        return True
    else:
        return False


if __name__ == "__main__":
    if len(starttime) != len(endtime):
        raise Exception('# Error: the run time format is not correct!')
    else:
        while True:
            if RunNow():
                DoYourWork()
            else:
                RestYourSelf()

            time.sleep(sleeptime)  # sleep for 5 s
