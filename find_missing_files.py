import os
import re
from datetime import datetime, timedelta

FOLDER_PATH = r"output\excels"
START_DATE = "2020-02-01"
END_DATE = "2020-04-30"

start = datetime.strptime(START_DATE, "%Y-%m-%d")
end = datetime.strptime(END_DATE, "%Y-%m-%d")
expected_dates = {
    (start + timedelta(days=i)).strftime("%Y%m%d")
    for i in range((end - start).days + 1)
}

pattern = re.compile(r"(\d{8})")
actual_dates = set()

for file in os.listdir(FOLDER_PATH):
    match = pattern.search(file)
    if match:
        date_str = match.group(1)
        try:
            datetime.strptime(date_str, "%Y%m%d")
            actual_dates.add(date_str)
        except ValueError:
            continue

missing_dates = sorted(expected_dates - actual_dates)
for date in missing_dates:
    print(f"{date[:4]}-{date[4:6]}-{date[6:]}")
