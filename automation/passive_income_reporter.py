import os
import datetime

def generate_report():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_path = os.path.expanduser('~/streamline-ai-project/reports/latest_income_report.txt')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        f.write(f"--- PASSIVE INCOME REPORT ---\nTIMESTAMP: {timestamp}\nPAYMENT LINK: https://paypal.me/mitchdav0518n")
    print("Report generated.")

if __name__ == "__main__":
    generate_report()
