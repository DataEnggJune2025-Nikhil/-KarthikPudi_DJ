import argparse
from log_parser import LogParser
from postgres_handler import PostgresHandler
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

db_config = {
    'host': config.get('postgres', 'host'),
    'user': config.get('postgres', 'user'),
    'password': config.get('postgres', 'password'),
    'database': config.get('postgres', 'database')
}


def process_logs(file_path):
    parser = LogParser()
    db = PostgresHandler(**db_config)

    with open(file_path, "r") as file:
        for line in file:
            parsed = parser.parse_line(line)
            if parsed:
                db.insert_log_entry(parsed)

    db.close()
    print("✅ Finished processing log file.")

def generate_report(report_type, n=None):
    db = PostgresHandler(**db_config)

    if report_type == "top_n_ips":
        results = db.get_top_n_ips(n)
        print(f"\nTop {n} IP Addresses:")
        for row in results:
            print(f"{row[0]} → {row[1]} requests")

    elif report_type == "status_code_distribution":
        results = db.get_status_code_distribution()
        print("\nStatus Code Distribution:")
        for row in results:
            print(f"HTTP {row[0]} → {row[1]} times ({row[2]}%)")

    elif report_type == "hourly_traffic":
        results = db.get_hourly_traffic()
        print("\nHourly Traffic:")
        for row in results:
            print(f"{row[0]} → {row[1]} requests")

    elif report_type == "top_n_pages":
        results = db.get_top_n_pages(n)
        print(f"\nTop {n} Requested Pages:")
        for row in results:
            print(f"{row[0]} → {row[1]} requests")

    elif report_type == "traffic_by_os":
        results = db.get_traffic_by_os()
        print("\nTraffic by Operating System:")
        for row in results:
            os_label = row[0] or "Unknown"
            print(f"{os_label} → {row[1]} requests")

    elif report_type == "error_logs_by_date":
        date_str = input("Enter date (YYYY-MM-DD): ")
        results = db.get_error_logs_by_date(date_str)
        print(f"\nError Logs on {date_str}:")
        for row in results:
            print(f"{row[0]} at {row[1]} → {row[3]} on {row[2]}")
            print(f"User Agent: {row[4]}\n")

    db.close()

def main():
    parser = argparse.ArgumentParser(description="Log Analyzer CLI")
    subparsers = parser.add_subparsers(dest="command")

    process_parser = subparsers.add_parser("process_logs", help="Parse and load logs from a file")
    process_parser.add_argument("file_path", type=str, help="Path to the log file")

    report_parser = subparsers.add_parser("generate_report", help="Generate reports")
    report_parser.add_argument("report_type", choices=["top_n_ips","status_code_distribution","hourly_traffic","top_n_pages", "traffic_by_os", "error_logs_by_date"])
    report_parser.add_argument("-n", type=int, help="Number of top IPs (for top_n_ips)")

    args = parser.parse_args()

    if args.command == "process_logs":
        process_logs(args.file_path)
    elif args.command == "generate_report":
        generate_report(args.report_type, args.n)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
