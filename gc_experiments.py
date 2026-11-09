"""
=====================================================================
 PYTHON GARBAGE COLLECTION: AUTOMATIC MECHANISM AND MANUAL CONTROL
 Experiments with the gc module
=====================================================================
IN PLAIN ENGLISH:
  Python cleans up memory in TWO ways.
  1) Reference counting: every object counts how many names point to
     it. The moment the count hits zero, it is thrown away at once.
  2) The cyclic garbage collector (the gc module): finds groups of
     objects that only point to EACH OTHER (a cycle). Their counts
     never reach zero, so reference counting alone would leak them.
     gc runs now and then, finds such islands and removes them.
  The gc module lets us watch, tune, pause and trigger step 2 by hand.
=====================================================================
"""

import gc
import sys
import time
import weakref
import tracemalloc


def section(title):
    print(f"\n{'=' * 8} {title} {'=' * 8}")


class Node:
    """A tiny object that announces when it is destroyed."""
    def __init__(self, name):
        self.name = name
        self.other = None

    def __del__(self):
        print(f"   [__del__] {self.name} destroyed")


# ---------------------------------------------------------------------
# EXPERIMENT 1: reference counting frees objects instantly
# ---------------------------------------------------------------------
def exp1_reference_counting():
    section("1. Reference counting: instant cleanup")
    a = Node("A")
    print("refcount of A (name + argument of getrefcount):", sys.getrefcount(a))
    b = a                                   # a second name for the same object
    print("after b = a, refcount:", sys.getrefcount(a))
    del a
    print("after del a, refcount:", sys.getrefcount(b), "(object still alive)")
    print("deleting the last name...")
    del b                                   # count hits zero -> __del__ runs NOW
    print("(destroyed immediately, no gc needed)")


# ---------------------------------------------------------------------
# EXPERIMENT 2: a reference CYCLE defeats reference counting
# ---------------------------------------------------------------------
def exp2_cycle_and_manual_collect():
    section("2. Reference cycle leaks until gc.collect()")
    gc.collect()                            # start from a clean slate
    gc.disable()                            # pause automatic collection
    print("gc enabled?", gc.isenabled())
    x, y = Node("X"), Node("Y")
    x.other, y.other = y, x                 # X -> Y -> X  (a cycle)
    del x, y                                # no outside names remain...
    print("deleted both names. Nothing printed => still in memory (leaked)")
    found = gc.collect()                    # manual collection
    print(f"gc.collect() returned {found} (unreachable objects found)")
    gc.enable()


# ---------------------------------------------------------------------
# EXPERIMENT 3: thresholds, counts and statistics
# ---------------------------------------------------------------------
def exp3_thresholds_counts_stats():
    section("3. Thresholds, counts and statistics")
    print("get_threshold():", gc.get_threshold(),
          " (gen0 trigger, gen1 trigger, gen2 trigger)")
    print("get_count()    :", gc.get_count(),
          " (allocations - deallocations, per generation)")
    print("get_stats()    : one dict per generation, e.g. generation 0:")
    s = gc.get_stats()[0]
    print("   collections =", s["collections"], " collected =", s["collected"],
          " uncollectable =", s["uncollectable"])


# ---------------------------------------------------------------------
# EXPERIMENT 4: watch AUTOMATIC collections with a callback
# ---------------------------------------------------------------------
def exp4_automatic_trigger():
    section("4. Automatic collection triggered by the threshold")
    events = []

    def watcher(phase, info):               # gc calls this before/after a run
        if phase == "stop":
            events.append((info["generation"], info["collected"]))

    gc.callbacks.append(watcher)
    old = gc.get_threshold()
    gc.collect()
    gc.set_threshold(50, 5, 5)              # tiny gen0 threshold => frequent runs
    events.clear()

    for _ in range(300):                    # create many small cycles
        a, b = [], []
        a.append(b)
        b.append(a)

    gc.set_threshold(*old)
    gc.callbacks.remove(watcher)
    print(f"With threshold0=50, gc ran {len(events)} times by itself.")
    print("First few runs (generation, objects collected):", events[:5])


# ---------------------------------------------------------------------
# EXPERIMENT 5: generations - survivors get promoted
# ---------------------------------------------------------------------
def exp5_generations():
    section("5. Generations: young objects that survive grow old")
    gc.collect()
    keeper = [Node("K")]                    # a long-lived object
    keeper[0].other = keeper                # make it a cycle holder, still referenced
    print("objects per generation BEFORE collect(0):",
          [len(gc.get_objects(g)) for g in range(3)])
    gc.collect(0)                           # collect only the youngest
    print("objects per generation AFTER  collect(0):",
          [len(gc.get_objects(g)) for g in range(3)])
    gc.collect(1)
    print("objects per generation AFTER  collect(1):",
          [len(gc.get_objects(g)) for g in range(3)])
    print("(young objects that survive are promoted to older generations)")
    keeper[0].other = None
    del keeper


# ---------------------------------------------------------------------
# EXPERIMENT 6: memory before / after manual collection
# ---------------------------------------------------------------------
def exp6_memory_effect():
    section("6. Memory effect of cycles with gc paused")
    gc.collect()
    gc.disable()
    tracemalloc.start()
    base = tracemalloc.get_traced_memory()[0]
    for _ in range(20000):
        a, b = {}, {}
        a["b"], b["a"] = b, a               # 20,000 dictionary cycles
    del a, b
    leaked = tracemalloc.get_traced_memory()[0] - base
    n = gc.collect()
    after = tracemalloc.get_traced_memory()[0] - base
    tracemalloc.stop()
    gc.enable()
    print(f"memory held by unreachable cycles : {leaked / 1024:8.1f} KiB")
    print(f"gc.collect() freed {n} objects")
    print(f"memory after collect              : {after / 1024:8.1f} KiB")


# ---------------------------------------------------------------------
# EXPERIMENT 7: DEBUG_SAVEALL - inspect what gc would delete
# ---------------------------------------------------------------------
def exp7_debug_saveall():
    section("7. DEBUG_SAVEALL: peek at the garbage")
    gc.collect()
    gc.set_debug(gc.DEBUG_SAVEALL)          # keep garbage in gc.garbage
    p, q = [1], [2]
    p.append(q)
    q.append(p)
    del p, q
    gc.collect()
    print("gc.garbage now holds:", gc.garbage)
    gc.set_debug(0)                         # turn debugging off
    gc.garbage.clear()                      # drop our references (now truly freed)
    gc.collect()


# ---------------------------------------------------------------------
# EXPERIMENT 8: which objects does gc track? weak references
# ---------------------------------------------------------------------
def exp8_tracking_and_weakref():
    section("8. is_tracked() and weak references")
    samples = [("int 5", 5), ("string", "hi"), ("list", [1]),
               ("empty dict", {}), ("dict with list", {"k": [1]}),
               ("tuple of ints", (1, 2)), ("Node object", Node("T"))]
    for label, obj in samples:
        print(f"   {label:<16} tracked by gc? {gc.is_tracked(obj)}")
    n = Node("W")
    ref = weakref.ref(n)                    # does NOT keep n alive
    print("weakref alive?", ref() is not None)
    del n
    print("after del, weakref alive?", ref() is not None)


# ---------------------------------------------------------------------
# EXPERIMENT 9: freeze() - exclude long-lived objects from scans
# ---------------------------------------------------------------------
def exp9_freeze():
    section("9. gc.freeze(): park long-lived objects")
    gc.collect()
    print("frozen before :", gc.get_freeze_count())
    gc.freeze()
    print("frozen after  :", gc.get_freeze_count(), "(skipped by later scans)")
    gc.unfreeze()
    print("after unfreeze:", gc.get_freeze_count())


# ---------------------------------------------------------------------
# EXPERIMENT 10: speed - gc on vs off for allocation-heavy code
# ---------------------------------------------------------------------
def exp10_timing():
    section("10. Cost of automatic gc (allocation-heavy loop)")

    def work():
        data = []
        for i in range(400_000):
            data.append([i])                # many tracked containers survive
        return len(data)

    results = {}
    for label, enabled in (("gc enabled ", True), ("gc disabled", False)):
        gc.collect()
        (gc.enable if enabled else gc.disable)()
        t = time.perf_counter()
        work()
        results[label] = time.perf_counter() - t
        gc.enable()
        print(f"   {label}: {results[label] * 1000:7.1f} ms")
    print("(timings vary by machine and Python version; the lesson is that")
    print(" gc has a cost, so only pause it when you have measured a gain)")


if __name__ == "__main__":
    print("Python", sys.version.split()[0])
    exp1_reference_counting()
    exp2_cycle_and_manual_collect()
    exp3_thresholds_counts_stats()
    exp4_automatic_trigger()
    exp5_generations()
    exp6_memory_effect()
    exp7_debug_saveall()
    exp8_tracking_and_weakref()
    exp9_freeze()
    exp10_timing()