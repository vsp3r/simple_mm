from datetime import datetime

# Sample datetime string
# dt_str = "2023-10-01T00:00:02.501168"

dt_str = "2023-09-30T17:00:01.383378000"
# dt_str = "2023-10-01T16:36:19.182416897"
# # Convert the string to a datetime object

# dt_obj = datetime.strptime(dt_str[:-3], "%Y-%m-%dT%H:%M:%S.%f")

# # Convert the datetime object to a Unix timestamp in seconds
# unix_time_seconds = int(dt_obj.timestamp() * 1e6)

# # Convert to microseconds (1 second = 1e6 microseconds)
# # unix_time_microseconds = int(unix_time_seconds * 1e6)

# print(unix_time_seconds)

def conv(time):
    if len(time) > len(dt_str):
        raise Exception(f"uhhh {time}")
    elif len(time) < len(dt_str):
        time += '0' * (len(dt_str) - len(time))
    dt_obj = datetime.strptime(time[:-3], "%Y-%m-%dT%H:%M:%S.%f")
    unix_time_seconds = int(dt_obj.timestamp() * 1e6)
    return unix_time_seconds

