import re
from datetime import datetime

def parse_log_line(line):
    """
    Example log line: 'Failed login from 192.168.1.1 at 10:32 PM'
    Returns dict with extracted fields or None if not matched.
    """
    # Example regex for failed login
    match = re.match(r"Failed login from ([\d.]+) at ([\d: ]+[APM]{2})", line)
    if match:
        ip = match.group(1)
        time_str = match.group(2)
        # Try to parse time (assume today for demo)
        try:
            timestamp = datetime.strptime(time_str, "%I:%M %p")
            timestamp = timestamp.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        except Exception:
            timestamp = datetime.now()
        return {
            'ip': ip,
            'event': 'failed_login',
            'timestamp': timestamp
        }
    # Add more patterns as needed
    return None

def parse_log_content(content):
    """
    Parse multiline log content into structured events.
    """
    events = []
    for line in content.splitlines():
        parsed = parse_log_line(line)
        if parsed:
            events.append(parsed)
    return events
