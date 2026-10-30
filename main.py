try:
    with open("input.txt", "r") as f:
        lines = f.readlines()

    print("Total number of lines:", len(lines))

    with open("output.txt", "w") as f:
        f.writelines(lines[:2])

    print("First two lines saved to output.txt")

except FileNotFoundError:
    print("Input file not found!")