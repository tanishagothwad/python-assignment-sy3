"""
=====================================================================
 LONGEST COMMON SUBSEQUENCE (LCS)
 Approach : Dynamic Programming (Tabulation), with Brute-Force and
            Memoized versions included for comparison.
=====================================================================
IN PLAIN ENGLISH:
  Imagine two playlists. You want the longest list of songs that
  appear in BOTH playlists, in the same relative order, even if other
  songs are mixed in between them. That shared, in-order list is a
  "common subsequence". The LONGEST one possible is the LCS.

  Example:
      Playlist 1: A B C B D A B
      Playlist 2: B D C A B A
      Longest common subsequence: B C B A   (length 4)
=====================================================================
"""


# =====================================================================
# 1. BRUTE FORCE  (for comparison only \u2014 exponential time)
#    Plain English: try EVERY possible way of matching characters.
#    Fine for tiny inputs, hopeless for anything real-sized.
# =====================================================================
def brute_force_lcs(seq1, seq2):
    """Naive recursive LCS length. Explores every combination of
    'skip from seq1' / 'skip from seq2' / 'match both'.
    Time complexity: O(2^(m+n)) \u2014 exponential."""

    def helper(i, j):
        if i == 0 or j == 0:
            return 0
        if seq1[i - 1] == seq2[j - 1]:
            return 1 + helper(i - 1, j - 1)
        return max(helper(i - 1, j), helper(i, j - 1))

    return helper(len(seq1), len(seq2))


# =====================================================================
# 2. TOP-DOWN DP  (memoized recursion)
#    Plain English: same idea as brute force, but REMEMBERS answers
#    it has already worked out, so nothing is recomputed twice.
# =====================================================================
def memoized_lcs(seq1, seq2):
    """Recursive LCS length with a cache. Time complexity: O(m*n)."""
    memo = {}

    def helper(i, j):
        if i == 0 or j == 0:
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
        if seq1[i - 1] == seq2[j - 1]:
            result = 1 + helper(i - 1, j - 1)
        else:
            result = max(helper(i - 1, j), helper(i, j - 1))
        memo[(i, j)] = result
        return result

    return helper(len(seq1), len(seq2))


# =====================================================================
# 3. BOTTOM-UP DP (tabulation) \u2014 the main, recommended solution
#    Plain English: build a grid, fill it in one cell at a time using
#    only cells already filled (no recursion needed at all).
# =====================================================================
def build_lcs_table(seq1, seq2):
    """Fills an (m+1) x (n+1) grid where dp[i][j] = length of the LCS
    of the first i characters of seq1 and the first j characters of
    seq2. dp[m][n] (bottom-right corner) is the final answer's length.

    Recurrence:
        dp[i][j] = dp[i-1][j-1] + 1               if seq1[i-1] == seq2[j-1]
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])    otherwise
    """
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def reconstruct_lcs(dp, seq1, seq2):
    """Walks BACKWARDS through the filled table (from the bottom-right
    corner to the top-left) to recover the actual subsequence, not
    just its length."""
    i, j = len(seq1), len(seq2)
    result = []
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            result.append(seq1[i - 1])   # part of the LCS -> move diagonally
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1                       # move up
        else:
            j -= 1                       # move left
    result.reverse()
    return "".join(result) if isinstance(seq1, str) else result


def lcs(seq1, seq2):
    """Main entry point.
    Returns: (length, subsequence, dp_table)"""
    dp = build_lcs_table(seq1, seq2)
    length = dp[len(seq1)][len(seq2)]
    subsequence = reconstruct_lcs(dp, seq1, seq2)
    return length, subsequence, dp


# =====================================================================
# 4. HELPER: pretty-print the DP table (great for understanding it)
# =====================================================================
def print_dp_table(dp, seq1, seq2):
    header = "        " + "  ".join(f"{c:>2}" for c in seq2)
    print(header)
    for i, row in enumerate(dp):
        label = seq1[i - 1] if i > 0 else " "
        print(f"  {label:>2} | " + "  ".join(f"{v:>2}" for v in row))


# =====================================================================
# 5. DEMO / DRIVER CODE
# =====================================================================
if __name__ == "__main__":

    # ---- Example 1: classic textbook strings -------------------------
    seq1 = "ABCBDAB"
    seq2 = "BDCABA"

    print(f"Sequence 1: {seq1}")
    print(f"Sequence 2: {seq2}\n")

    length, subsequence, dp = lcs(seq1, seq2)

    print("DP Table  (dp[i][j] = LCS length of seq1[:i] and seq2[:j]):")
    print_dp_table(dp, seq1, seq2)

    print(f"\nLCS length      : {length}")
    print(f"LCS subsequence  : {subsequence}")

    # ---- cross-check the three approaches agree -----------------------
    print(f"\n[check] memoized_lcs length   : {memoized_lcs(seq1, seq2)}")
    print(f"[check] brute_force_lcs length (small input 'ABC' vs 'AC') : "
          f"{brute_force_lcs('ABC', 'AC')}")

    # ---- Example 2: LCS also works on lists, not just strings ---------
    list1 = ["walk", "to", "the", "store", "and", "buy", "milk"]
    list2 = ["drive", "to", "store", "buy", "some", "milk"]
    length2, subsequence2, _ = lcs(list1, list2)

    print("\nWord-list example:")
    print(f"List 1     : {list1}")
    print(f"List 2     : {list2}")
    print(f"LCS length : {length2}")
    print(f"LCS words  : {subsequence2}")
