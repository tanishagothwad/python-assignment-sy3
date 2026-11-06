"""
=====================================================================
 MULTIPLE THREADS PERFORMING DIFFERENT TASKS CONCURRENTLY
 Tools used : threading.Thread, threading.Lock, join(), time.sleep()
=====================================================================
IN PLAIN ENGLISH:
  Think of a kitchen with three cooks. One chops vegetables, one boils
  rice, one makes tea. They all work AT THE SAME TIME, so dinner is
  ready in the time of the SLOWEST job, not the sum of all three.

  A thread is one "cook". Our program starts several threads, each
  doing a DIFFERENT task, waits for all of them to finish (join), and
  uses a Lock so that two threads never scribble in the shared
  notebook (the results list) at the same moment.
=====================================================================
"""

import threading
import time
import tempfile
import os

# ---------------------------------------------------------------------
# SHARED STATE (every thread can see these)
# Plain English: a common notebook + a "talking stick" (Lock). Only the
# thread holding the stick may write in the notebook.
# ---------------------------------------------------------------------
results = []
results_lock = threading.Lock()
START = time.perf_counter()


def record(task_name, message):
    """Safely add one line to the shared results list."""
    elapsed = time.perf_counter() - START
    with results_lock:                      # only one thread at a time
        results.append(f"[{elapsed:5.2f}s] {task_name:<10} {message}")
        print(results[-1])


# ---------------------------------------------------------------------
# THREE DIFFERENT TASKS
# ---------------------------------------------------------------------
def compute_squares(n=5):
    """Task 1 - a CPU style job: compute squares step by step."""
    record("Compute", "started")
    total = 0
    for i in range(1, n + 1):
        time.sleep(0.3)                     # pretend heavy work
        total += i * i
    record("Compute", f"finished, sum of squares 1..{n} = {total}")


def write_file(path, lines=5):
    """Task 2 - a file I/O job: write lines into a text file."""
    record("FileWrite", "started")
    with open(path, "w") as f:
        for i in range(1, lines + 1):
            f.write(f"line {i}\n")
            time.sleep(0.2)
    record("FileWrite", f"finished, wrote {lines} lines")


def fake_download(name="report.pdf", seconds=1.0):
    """Task 3 - a network style job: simulate waiting for a download."""
    record("Download", f"started {name}")
    time.sleep(seconds)
    record("Download", f"finished {name}")


# ---------------------------------------------------------------------
# RUNNERS: one-after-another vs all-together
# ---------------------------------------------------------------------
def run_sequential(path):
    t0 = time.perf_counter()
    compute_squares()
    write_file(path)
    fake_download()
    return time.perf_counter() - t0


def run_threaded(path):
    t0 = time.perf_counter()
    threads = [
        threading.Thread(target=compute_squares, name="T-Compute"),
        threading.Thread(target=write_file, args=(path,), name="T-File"),
        threading.Thread(target=fake_download, kwargs={"name": "data.zip"},
                         name="T-Download"),
    ]
    for t in threads:
        t.start()                           # all begin together
    for t in threads:
        t.join()                            # wait until every one is done
    return time.perf_counter() - t0


if __name__ == "__main__":
    out = os.path.join(tempfile.gettempdir(), "thread_demo.txt")

    print("=== A) SEQUENTIAL (one task after another) ===")
    t_seq = run_sequential(out)

    results.clear()
    START = time.perf_counter()
    print("\n=== B) THREADED (all tasks together) ===")
    t_thr = run_threaded(out)

    print(f"\nSequential time : {t_seq:.2f} s")
    print(f"Threaded time   : {t_thr:.2f} s")
    print(f"Speed-up        : {t_seq / t_thr:.1f}x faster")
    print(f"Active threads at end: {threading.active_count()} (main only)")