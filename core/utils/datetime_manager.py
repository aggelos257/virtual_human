import datetime

def now_iso():
    return datetime.datetime.now().isoformat()

def format_time(ts=None):
    dt = datetime.datetime.fromtimestamp(ts) if ts else datetime.datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")
