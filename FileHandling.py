"""
=====================================================================
 FILE READER: COUNT LINES, EXTRACT FIRST TWO LINES, WRITE TO NEW FILE
=====================================================================
IN PLAIN ENGLISH:
  Think of a text file like a stack of index cards, one line per
  card. This script (1) counts how many cards are in the stack,
  (2) pulls out just the top two cards, and (3) writes copies of
  those two cards into a brand-new stack (a new file) \u2014 without
  ever touching or changing the original stack.
=====================================================================
"""


# =====================================================================
# 1. COUNT LINES IN A FILE
#    Plain English: open the file, and count how many lines it has.
# =====================================================================
def count_lines(input_path):
    """Returns the total number of lines in the file at input_path."""
    with open(input_path, "r") as f:
        return sum(1 for _ in f)


# =====================================================================
# 2. EXTRACT THE FIRST N LINES
#    Plain English: read lines one at a time, stopping as soon as we
#    have enough \u2014 no need to read the WHOLE file if it's huge.
# =====================================================================
def extract_first_lines(input_path, n=2):
    """Returns a list containing the first n lines of the file
    (each line still includes its trailing newline character, if any)."""
    first_lines = []
    with open(input_path, "r") as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            first_lines.append(line)
    return first_lines


# =====================================================================
# 3. WRITE THE EXTRACTED LINES TO A NEW FILE
#    Plain English: open a brand-new file for writing, and save the
#    lines we extracted into it.
# =====================================================================
def write_lines(output_path, lines):
    """Writes `lines` to a new file at output_path (overwriting it if
    it already exists)."""
    with open(output_path, "w") as f:
        f.writelines(lines)


# =====================================================================
# 4. DEMO / DRIVER CODE
# =====================================================================
if __name__ == "__main__":

    input_path = "input.txt"
    output_path = "output_first_two_lines.txt"

    # ---- create a sample input file, just for this demo --------------
    sample_content = (
        "Monday: Team stand-up at 9:00 AM\n"
        "Tuesday: Client review meeting\n"
        "Wednesday: Code review session\n"
        "Thursday: Sprint planning\n"
        "Friday: Deployment and retrospective\n"
    )
    with open(input_path, "w") as f:
        f.write(sample_content)
    print(f"Created sample input file: {input_path}\n")

    # ---- Step 1: count lines --------------------------------------------
    total_lines = count_lines(input_path)
    print(f"Total number of lines in '{input_path}': {total_lines}")

    # ---- Step 2: extract the first two lines -----------------------------
    first_two = extract_first_lines(input_path, n=2)
    print("\nFirst two lines extracted:")
    for line in first_two:
        print(f"  {line.rstrip()}")

    # ---- Step 3: write the extracted lines to a new file -------------------
    write_lines(output_path, first_two)
    print(f"\nExtracted lines written to: {output_path}")

    # ---- verify: read back the new file and print its contents --------------
    print(f"\nContents of '{output_path}':")
    with open(output_path, "r") as f:
        print(f.read())