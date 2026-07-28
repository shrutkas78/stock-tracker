from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from fetch import get_price
from db import init_db, save_price

WATCHLIST = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

def job():
    for t in WATCHLIST:
        price = get_price(t)
        save_price(t, price, datetime.now().isoformat())
        print(f"Saved {t}: {price}")

init_db()
job()  # run once immediately

sched = BlockingScheduler()
sched.add_job(job, "interval", minutes=5)
print("Scheduler started. Press Ctrl+C to stop.")
sched.start()
