from datetime import timedelta


def td_str(td: timedelta):
    sec = td.seconds + td.days * 86400
    hours, remainder = divmod(sec, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)
