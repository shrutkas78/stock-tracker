from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from fetch import get_price
from db import init_db, save_price
from config import WATCHLIST, FETCH_INTERVAL_MINUTES

def job():
    for t in WATCHLIST:
        try:
            price = get_price(t)
            save_price(t, price, datetime.now().isoformat())
            print(f"Saved {t}: {price}")
        except Exception as e:
            print(f"Failed {t}: {e}")

init_db()
job()  # run once immediately

sched = BlockingScheduler()
sched.add_job(job, "interval", minutes=FETCH_INTERVAL_MINUTES)
print("Scheduler started. Press Ctrl+C to stop.")
sched.start()
