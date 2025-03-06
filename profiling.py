"""
profiling.py

Profile speed and memory allocation
"""

import tracemalloc
import time
import pixdiff

def profiling(version=None):
    """
    testing, profiling, and benchmarking pixdiff.compare
    Args: version (optional)
    Returns: result of pixdiff.compare()
    """

    # time
    start_time = time.perf_counter()

    # malloc
    tracemalloc.start()

    # ======================

    result = pixdiff.compare(
        "readme_images/example1.png", 
        "readme_images/example2.png", 
        rgba=(255, 0, 0, 128)
    )

    # ======================

    # time
    end_time = time.perf_counter()
    elapsed_time_ms = (end_time - start_time) * 1000
    print(f"Elapsed time (v{version}): {elapsed_time_ms:.2f} ms")

    # malloc
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    print(f"[ Top 10 (v{version}) ]")
    for stat in top_stats[:10]:
        print(stat)

    return result

def both():
    """
    profile 2 different modes
    """
    result_default = profiling(pixdiff.VERSION)
    print("=" * 50)
    result_fast = profiling(pixdiff.VERSION)
    print("=" * 50)

    if result_default == result_fast:
        print("results are the same")
    else:
        print("results are NOT the same")

def one():
    """
    profile 1 mode
    """
    print("=" * 50)
    _ = profiling(pixdiff.VERSION)
    print("=" * 50)

if __name__ == "__main__":
    one()
