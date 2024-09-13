import datetime
import logging
import multiprocessing
import time

import pytz

logger = logging.getLogger(__name__)
logger.propagate = False  # Deduplicate default logging
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s[%(levelname)s][%(filename)s:%(lineno)s] %(message)s",
    datefmt="[%a %Y-%m-%d %H:%M:%S %Z]",
)
terminal_handler = logging.StreamHandler()
terminal_handler.setFormatter(formatter)
logger.addHandler(terminal_handler)

tz = pytz.timezone("US/Pacific")


def main():
    logger.info("RUNNING TESTER")
    t = 3600  # 1 hour.
    try:
        while True:
            now = datetime.datetime.now(tz=tz).astimezone(tz=tz)
            logger.info(f"RUNNING at {now}")

            num_cores = multiprocessing.cpu_count()
            logger.info(f"Using {num_cores} cores for stress testing...")

            processes = []
            for _ in range(num_cores):
                p = multiprocessing.Process(target=do_stuff)
                processes.append(p)
                p.start()

            # End processes.
            for p in processes:
                p.terminate()
            for p in processes:
                p.join()

            logger.info(f"Waiting for {t} seconds")
            time.sleep(t)

    except KeyboardInterrupt:
        pass
    finally:
        if processes:
            # End processes.
            for p in processes:
                p.terminate()
            for p in processes:
                p.join()


def do_stuff():
    x = 0
    for i in range(1000000000):
        x += i**2


if __name__ == "__main__":
    main()
