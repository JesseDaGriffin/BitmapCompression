data = './data/animals.txt'
sorted_data = './animals_sorted.txt'
bitmap = './animals_bitmap.txt'
sorted_bitmap = './animals_bitmap_sorted.txt'
unsorted_WAH32 = './animals_compressed_32.txt'
sorted_WAH32 = './animals_compressed_sorted_32.txt'
unsorted_WAH64 = './animals_compressed_64.txt'
sorted_WAH64 = './animals_compressed_sorted_64.txt'


def main():
    """Create unsorted bitmap"""
    dataF = open(data, 'r')
    bitmapF = open(bitmap, 'w')

    tup = dataF.readline()

    while tup:
        parse(tup, bitmapF)
        tup = dataF.readline()

    """Create sorted bitmap"""
    dataF.seek(0)
    num_lines = sort_it(dataF)

    sorted_dataF = open(sorted_data, 'r')
    sorted_bitmapF = open(sorted_bitmap, 'w')

    tup = sorted_dataF.readline()

    while tup:
        parse(tup, sorted_bitmapF)
        tup = sorted_dataF.readline()

    sorted_dataF.close()
    sorted_bitmapF.close()

    """Unsorted WAH 32 Compression"""
    bitmapF = open(bitmap, 'r')
    unsorted_WAH32F = open(unsorted_WAH32, 'w')
    # Print for writeup
    print('Unsorted WAH 32 Compression')
    wah_comp(num_lines, bitmapF, unsorted_WAH32F, 32)

    bitmapF.close()
    unsorted_WAH32F.close()

    """Sorted WAH 32 Compression"""
    sorted_bitmapF = open(sorted_bitmap, 'r')
    sorted_WAH32F = open(sorted_WAH32, 'w')

    print('Sorted WAH 32 Compression')
    wah_comp(num_lines, sorted_bitmapF, sorted_WAH32F, 32)

    sorted_bitmapF.close()
    sorted_WAH32F.close()

    """Unsorted WAH 64 Compression"""
    bitmapF = open(bitmap, 'r')
    unsorted_WAH64F = open(unsorted_WAH64, 'w')

    print('Unsorted WAH 64 Compression')
    wah_comp(num_lines, bitmapF, unsorted_WAH64F, 64)

    bitmapF.close()
    unsorted_WAH64F.close()

    """Sorted WAH 64 Compression"""
    sorted_bitmapF = open(sorted_bitmap, 'r')
    sorted_WAH64F = open(sorted_WAH64, 'w')

    print('Sorted WAH 64 Compression')
    wah_comp(num_lines, sorted_bitmapF, sorted_WAH64F, 64)

    sorted_bitmapF.close()
    sorted_WAH64F.close()


def wah_comp(number_lines, bitmapF, wahF, comp_size):
    bits = []
    run_count0 = 0
    run_count1 = 0
    num_lines = 0
    flag0 = 0
    flag1 = 0
    num_lines = number_lines
    # Keep track and print for assignment writeup
    num_runs0 = 0
    num_runs1 = 0
    num_lits = 0
    # Set variables based on wordsize passed in
    if comp_size == 32:
        bin_fill = '030b'
        word_size = 31
    if comp_size == 64:
        bin_fill = '062b'
        word_size = 63

    bitmapF.seek(0)
    # Iterate through each column
    for i in range(0, 16):
        # Iterate through each row
        for j in range(0, num_lines + 1):
            # Set offset to (i, j) position
            bitmapF.seek(i + (j * 17))
            bits.append(bitmapF.read(1))
            # When we have 31 bits, check if there are a miture of bits or a run
            if len(bits) == word_size:
                for bit in bits:
                    if bit == '0':
                        flag0 = 1
                    else:
                        flag1 = 1
                # Saw a literal
                if flag0 == 1 and flag1 == 1:
                    # Write run of 0's if there was a previous run
                    if run_count0 > 0:
                        wahF.write('10' + format(run_count0, bin_fill))
                        run_count0 = 0
                    # Write run of 1's if there was a previous run
                    if run_count1 > 0:
                        wahF.write('11' + format(run_count1, bin_fill))
                        run_count1 = 0
                    # Write literal
                    wahF.write('0' + ''.join(bits))
                    flag0 = 0
                    flag1 = 0
                    num_lits += 1
                    bits = []
                # Saw a run of 0's
                if flag0 == 1 and flag1 == 0:
                    # Write run of 1's if there was a previous run
                    if run_count1 > 0:
                        wahF.write('11' + format(run_count1, bin_fill))
                        run_count1 = 0

                    flag0 = 0
                    run_count0 += 1
                    num_runs0 += 1
                    bits = []
                # Saw a run of 1's
                if flag0 == 0 and flag1 == 1:
                    # Write run of 0's if there was a previous run
                    if run_count0 > 0:
                        wahF.write('10' + format(run_count0, bin_fill))
                        run_count0 = 0

                    flag1 = 0
                    run_count1 += 1
                    num_runs1 += 1
                    bits = []
        # Write run of 0's if there was a previous run
        if run_count0 > 0:
            wahF.write('10' + format(run_count0, bin_fill))
            run_count0 = 0
        # Write run of 1's if there was a previous run
        if run_count1 > 0:
            wahF.write('11' + format(run_count1, bin_fill))
            run_count1 = 0
        # Write the remaining bits as a literal
        wahF.write('0' + ''.join(bits))
        wahF.write('\n')
        bits = []
        num_lits += 1
    print('Number of 0 fills: ' + str(num_runs0))
    print('Number of 1 fills: ' + str(num_runs1))
    print('Number of literals: ' + str(num_lits))


"""Sort data file lexicographically and write to a new file"""


def sort_it(dataF):
    num_lines = 0
    sorted_dataF = open(sorted_data, 'w')

    text = dataF.readlines()
    text.sort()
    # Sort file and count number of lines
    for line in text:
        sorted_dataF.write(line)
        num_lines += 1

    sorted_dataF.close()
    # Return number of lines for the rest of the program to use
    return num_lines


"""Takes in a tuple and coverts it into a bitmap"""


def parse(tup, bitmapF):
    string = ""
    tuple = tup.split(',')
    # Set bits for animal in tuple
    if tuple[0] == "cat":
        string = string + "1000"
    if tuple[0] == "dog":
        string = string + "0100"
    if tuple[0] == "turtle":
        string = string + "0010"
    if tuple[0] == "bird":
        string = string + "0001"
    # Set bits for age range in tuple
    if withinR(int(tuple[1]), 1, 10):
        string = string + "1000000000"
    if withinR(int(tuple[1]), 11, 20):
        string = string + "0100000000"
    if withinR(int(tuple[1]), 21, 30):
        string = string + "0010000000"
    if withinR(int(tuple[1]), 31, 40):
        string = string + "0001000000"
    if withinR(int(tuple[1]), 41, 50):
        string = string + "0000100000"
    if withinR(int(tuple[1]), 51, 60):
        string = string + "0000010000"
    if withinR(int(tuple[1]), 61, 70):
        string = string + "0000001000"
    if withinR(int(tuple[1]), 71, 80):
        string = string + "0000000100"
    if withinR(int(tuple[1]), 81, 90):
        string = string + "0000000010"
    if withinR(int(tuple[1]), 91, 100):
        string = string + "0000000001"
    # Set bits for true or false in tuple
    if tuple[2] == "True\n":
        string = string + "10"
    if tuple[2] == "False\n":
        string = string + "01"

    bitmapF.write(string + '\n')


"""Helper function to decide if in range"""


def withinR(num, low, high):
    return num >= low and num <= high


main()
