
"""
=====================================================================
 CREATING A ONE-DIMENSIONAL NUMPY ARRAY (THE NUMBERS 1 TO 10)
=====================================================================
IN PLAIN ENGLISH:
  A NumPy array is like a Python list, but built specifically for
  fast, whole-array math. A "one-dimensional" array is simply a
  single row of numbers \u2014 no rows-and-columns grid, just one
  straight line of values, like beads on a single string.

  This script creates that array two different ways, inspects its
  basic properties, and shows a few quick examples of why NumPy
  arrays are so useful compared to plain Python lists.
=====================================================================
"""

import numpy as np


# =====================================================================
# 1. CREATE THE ARRAY \u2014 TWO COMMON WAYS
# =====================================================================
def create_array_from_list():
    """Plain English: hand NumPy a Python list, and it wraps it up as
    an array. Simple and explicit, but tedious for long sequences."""
    return np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


def create_array_with_arange():
    """Plain English: np.arange(start, stop) generates a sequence of
    numbers directly, without typing them all out. Note that `stop`
    (11) is EXCLUDED, which is why we write 11, not 10, to include 10."""
    return np.arange(1, 11)


# =====================================================================
# 2. INSPECT THE ARRAY'S BASIC PROPERTIES
#    Plain English: every NumPy array carries a few useful facts
#    about itself, which we can simply ask for.
# =====================================================================
def describe_array(arr):
    """Prints the array itself and its key attributes."""
    print(f"Array            : {arr}")
    print(f"Data type (dtype): {arr.dtype}")
    print(f"Shape            : {arr.shape}")
    print(f"Number of dims   : {arr.ndim}")
    print(f"Size (elements)  : {arr.size}")


# =====================================================================
# 3. DEMO / DRIVER CODE
# =====================================================================
if __name__ == "__main__":

    # ---- Method 1: build the array from an explicit list --------------
    arr1 = create_array_from_list()
    print("Array created with np.array([1, 2, ..., 10]):")
    describe_array(arr1)

    # ---- Method 2: build the same array with arange --------------------
    print()
    arr2 = create_array_with_arange()
    print("Array created with np.arange(1, 11):")
    describe_array(arr2)

    # ---- confirm both methods give the exact same result ---------------
    print()
    print("Are both arrays equal?", np.array_equal(arr1, arr2))

    # ---- BONUS: vectorized operations (no loop needed) -------------------
    print()
    print("Bonus: vectorized operations (applied to every element at once)")
    print(f"arr1 * 2       : {arr1 * 2}")
    print(f"arr1 + 100     : {arr1 + 100}")
    print(f"sum(arr1)      : {arr1.sum()}")
    print(f"mean(arr1)     : {arr1.mean()}")

    # ---- BONUS: indexing and slicing ---------------------------------------
    print()
    print("Bonus: indexing and slicing")
    print(f"First element  : {arr1[0]}")
    print(f"Last element   : {arr1[-1]}")
    print(f"First 5 values : {arr1[:5]}")
    print(f"Every other    : {arr1[::2]}")