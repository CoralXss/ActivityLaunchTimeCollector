import datetime


# 获取当前时间
def get_current_time():
    return datetime.datetime.now()


# 参数均由 datetime.datetime.now() 提供才能获取 seconds
def get_time_span(start_time, end_time):
    return (end_time - start_time).seconds


def get_time_span_string(start_time, end_time):
    s = '%d s' % (end_time - start_time).seconds
    return s.strip()

# s_time = get_current_time()
# for i in range(10):
#     print('------')
# e_time = get_current_time()
#
# print('time = %d' % get_time_span(e_time, s_time))

