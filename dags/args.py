from datetime import datetime, timedelta

default_args = {
    "owner": "Ngoc_Thinh",
    "retries": 2,
    "retry_delay": timedelta(seconds=5),
    "start_date": datetime(2022, 1, 1),
}
