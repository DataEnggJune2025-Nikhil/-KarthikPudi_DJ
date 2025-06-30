import psycopg2
import logging

class PostgresHandler:
    def __init__(self, host, user, password, database):
        self.conn = psycopg2.connect(
            host=host, user=user, password=password, dbname=database
        )
        self.cursor = self.conn.cursor()

    def get_or_create_user_agent(self, user_agent_string):
        self.cursor.execute(
            "SELECT id FROM user_agents WHERE user_agent_string = %s",
            (user_agent_string,)
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]

        # Simple agent parsing
        os = "Unknown OS"
        browser = "Unknown Browser"
        device_type = "Desktop"

        if "Windows" in user_agent_string:
            os = "Windows"
        elif "Macintosh" in user_agent_string:
            os = "macOS"
        elif "Linux" in user_agent_string:
            os = "Linux"

        if "Chrome" in user_agent_string:
            browser = "Chrome"
        elif "Firefox" in user_agent_string:
            browser = "Firefox"
        elif "Safari" in user_agent_string:
            browser = "Safari"

        if "Mobile" in user_agent_string:
            device_type = "Mobile"
        elif "Tablet" in user_agent_string:
            device_type = "Tablet"

        self.cursor.execute("""
            INSERT INTO user_agents (user_agent_string, os, browser, device_type)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (user_agent_string, os, browser, device_type))

        self.conn.commit()
        return self.cursor.fetchone()[0]

    def insert_log_entry(self, log_data):
        user_agent_id = self.get_or_create_user_agent(log_data['user_agent'])

        self.cursor.execute("""
            INSERT INTO log_entries (ip_address, timestamp, method, path, status_code, bytes_sent, referrer, user_agent_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            log_data['ip_address'], log_data['timestamp'], log_data['method'], log_data['path'],
            log_data['status_code'], log_data['bytes_sent'], log_data['referrer'], user_agent_id
        ))

        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_top_n_ips(self, n):
        self.cursor.execute("""
        SELECT ip_address, COUNT(*) AS request_count
        FROM log_entries
        GROUP BY ip_address
        ORDER BY request_count DESC
        LIMIT %s
    """, (n,))
        return self.cursor.fetchall()
    
    def get_status_code_distribution(self):
        self.cursor.execute("""
        SELECT 
            status_code, 
            COUNT(*) AS count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM log_entries), 2) AS percentage
        FROM log_entries
        GROUP BY status_code
        ORDER BY count DESC
    """)
        return self.cursor.fetchall()
    
    def get_hourly_traffic(self):
        self.cursor.execute("""
        SELECT 
            TO_CHAR(timestamp, 'HH24:00') AS hour,
            COUNT(*) AS request_count
        FROM log_entries
        GROUP BY hour
        ORDER BY hour;
    """)
        return self.cursor.fetchall()
    
    def get_top_n_pages(self, n):
        self.cursor.execute("""
        SELECT path, COUNT(*) AS request_count
        FROM log_entries
        GROUP BY path
        ORDER BY request_count DESC
        LIMIT %s
    """, (n,))
        return self.cursor.fetchall()
    
    def get_traffic_by_os(self):
        self.cursor.execute("""
        SELECT ua.os, COUNT(le.id) AS request_count
        FROM log_entries le
        JOIN user_agents ua ON le.user_agent_id = ua.id
        GROUP BY ua.os
        ORDER BY request_count DESC;
    """)
        return self.cursor.fetchall()
    def get_error_logs_by_date(self, date_str):
        self.cursor.execute("""
        SELECT le.ip_address, le.timestamp, le.path, le.status_code, ua.user_agent_string
        FROM log_entries le
        JOIN user_agents ua ON le.user_agent_id = ua.id
        WHERE DATE(le.timestamp) = %s AND le.status_code >= 400
        ORDER BY le.timestamp;
    """, (date_str,))
        return self.cursor.fetchall()





