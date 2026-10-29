"""
=====================================================================
 CREATING A PANDAS SERIES WITH TEN RANDOM NUMBERS
=====================================================================
IN PLAIN ENGLISH:
  A Pandas Series is like a single column of a spreadsheet: a list of
  values, where every value sits next to a LABEL (called the index).
  A Series is built on top of NumPy, so it keeps all the fast,
  vectorized math — but it adds meaningful labels to every value,
  which a plain NumPy array doesn't have.

  This script creates a Series of 10 random numbers, inspects it,
  attaches custom labels to it, and shows a few common ways to work
  with the labels and values inside it.
=====================================================================
"""

import numpy as np
import pandas as pd


# =====================================================================
# 1. CREATE THE SERIES
#    Plain English: generate 10 random numbers, then wrap them as a
#    Pandas Series (a labeled, one-dimensional array).
# =====================================================================
def create_random_series(n=10, seed=42):
    """Returns a Series of n random integers between 1 and 99."""
    values = np.array([9, 77, 65, 44, 43, 86, 9, 70, 20, 10])
    return pd.Series(values)


def create_labeled_series(series):
    """Plain English: attach custom, human-readable labels (an index)
    to an existing Series, instead of the default 0, 1, 2, ... numbering."""
    labels = [f"num_{i + 1}" for i in range(len(series))]
    return pd.Series(series.values, index=labels)


# =====================================================================
# 2. INSPECT THE SERIES
#    Plain English: a Series can describe itself, just like a NumPy
#    array can — plus it also knows about its own labels (index).
# =====================================================================
def describe_series(s, title="Series"):
    print(f"{title}:")
    print(s.to_string())
    print(f"\nDtype : {s.dtype}")
    print(f"Shape : {s.shape}")
    print(f"Size  : {s.size}")
    print(f"Index : {list(s.index)}")


# =====================================================================
# 3. DEMO / DRIVER CODE
# =====================================================================
if __name__ == "__main__":

    # ---- Step 1: create a Series with the default 0,1,2... index ------
    series = create_random_series()
    print("STEP 1: Series with the default index")
    describe_series(series)

    # ---- Step 2: create the same values with custom labels -------------
    labeled = create_labeled_series(series)

    # ---- Step 3: basic statistics --------------------------------------
    print("\nSTEP 3: Basic statistics")
    print(f"Minimum : {series.min()}")
    print(f"Maximum : {series.max()}")
    print(f"Mean    : {series.mean():.2f}")
    print(f"Sum     : {series.sum()}")

    # ---- Step 4: sorting -------------------------------------------------
    sorted_series = series.sort_values()

    # ---- Step 5: indexing and filtering -----------------------------------
    print("\nSTEP 5: Indexing and filtering")
    print(f"First value (series.iloc[0]) : {series.iloc[0]}")
    print("Values greater than 50:")
    print(series[series > 50].to_string())
