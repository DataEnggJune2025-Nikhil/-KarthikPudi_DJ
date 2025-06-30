import re
from datetime import datetime

class LogParser:
    LOG_PATTERN = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s-\s-\s\[(?P<timestamp>[^\]]+)\]\s"(?P<request>[^"]+)"\s(?P<status>\d{3})\s(?P<bytes>\d+|-)'
        r'\s"(?P<referrer>[^"]*)"\s"(?P<user_agent>[^"]+)"'
    )

    def parse_line(self, line):
        match = self.LOG_PATTERN.match(line)
        if not match:
            return None

        data = match.groupdict()

        request_parts = data["request"].split()
        method = request_parts[0] if len(request_parts) > 0 else None
        path = request_parts[1] if len(request_parts) > 1 else None

        timestamp = datetime.strptime(data["timestamp"], "%d/%b/%Y:%H:%M:%S %z")

        return {
            "ip_address": data["ip"],
            "timestamp": timestamp,
            "method": method,
            "path": path,
            "status_code": int(data["status"]),
            "bytes_sent": int(data["bytes"]) if data["bytes"].isdigit() else 0,
            "referrer": data["referrer"] if data["referrer"] != "-" else None,
            "user_agent": data["user_agent"]
        }
