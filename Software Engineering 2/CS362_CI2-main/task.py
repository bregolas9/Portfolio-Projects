def my_datetime(num_sec):

    year = 1970
    month = 1
    day = 1

    secsRemaining = num_sec

    secInYear = 31536000
    secInLpYr = 31622400
    secInDay = 86400

    # calculate year
    while (secsRemaining / secInYear) >= 1 or (secsRemaining / secInLpYr) >= 1:
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            secsRemaining -= secInLpYr
            year += 1

        else:
            secsRemaining -= secInYear
            year += 1

    sec31DayMo = secInDay*31
    sec30DayMo = secInDay*30
    sec29DayMo = secInDay*29
    sec28DayMo = secInDay*28

    # months that have 30 and 31 days
    months31d = [1, 3, 5, 7, 8, 10, 12]
    months30d = [4, 6, 9, 11]

    # calculate month
    while (secsRemaining >= sec31DayMo):
        if month == 2:
            if year % 4 == 0:
                secsRemaining -= sec29DayMo
                month += 1
            else:
                secsRemaining -= sec28DayMo
                month += 1

        if month in months30d and (secsRemaining >= sec30DayMo):
            secsRemaining -= sec30DayMo
            month += 1

        if month in months31d and (secsRemaining >= sec31DayMo):
            secsRemaining -= sec31DayMo
            month += 1

    # calculate days
    while (secsRemaining / secInDay) >= 1:
        secsRemaining -= secInDay
        day += 1

    month = '{:02d}'.format(month)
    day = '{:02d}'.format(day)

    return f"{month}-{day}-{year}"


def char_to_base(char, base16=False):
    """
    Helper function for found_total function
    Converts a single char to a number and returns it
    Includes hexadecimal characters if base16 is True
    """

    # Set dictionary used for character to num conversions
    if base16:
        char_conversions = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
                            "9": 9, "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
    else:
        char_conversions = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}

    # Convert the given character to its numerical value using the conversion dictionary
    return char_conversions.get(char.upper(), None)


def found_total(num_str, hex_num, float_num, neg_num):
    """
    Calculates the numerical value of a given number string and returns it
    Helper function for conv_num, uses char from char_to_base
    """

    # Check for blank string
    if num_str == "":
        return None

    # Set num_base based on if hex or not
    if float_num:
        if hex_num:
            num_base = 16
        else:
            num_base = 10

    # Make base positive
    else:
        num_base = 1
    if neg_num:
        num_base *= -1
    total = 0

    # Go through each character in reverse, converts characters and then adds them to num_base
    i = len(num_str) - 1
    while i >= 0:
        cur_num = char_to_base(num_str[i], hex_num)
        if cur_num is None:
            return None
        total += cur_num * num_base
        if hex_num:
            num_base *= 16
        else:
            num_base *= 10
        i -= 1

    # Convert number to decimal if float and make value positive
    if float_num:
        total /= num_base
        if neg_num:
            total *= -1

    return total


def conv_num(num_str):
    """
    Converts the given number, given as a string, and converts it to a base 10 number
    Supports negatives, floats, and hexadecimal values
    Will return the converted number if valid, otherwise returns None
    """

    # Saves int calculation (used for floats), and final number calculation, then stores the decimal
    int_final, final = 0, 0
    hex_num, float_num, neg_num, done = False, False, False, False
    string_of_float = None

    # Check if negative, and strip '-' char from string
    if len(num_str) >= 1 and num_str[0] == "-":
        neg_num = True
        # Take "-" character from string
        num_str = num_str[1:]

    # Check if hexadecimal, and strip '0x' from string
    if len(num_str) >= 2 and num_str[0:2].lower() == "0x":
        hex_num = True
        num_str = num_str[2:]

    # Split the string between integer and decimal parts
    if "." in num_str:
        temp = num_str.split(".")
        if len(temp) > 2 or hex_num:
            return None

        # Replace blanks with "0"
        if temp[0] == "":
            num_str = "0"
        else:
            num_str = temp[0]
        if temp[1] == "":
            string_of_float = "0"
        else:
            string_of_float = temp[1]

    while not done:
        # Get the number's final value
        final = found_total(num_str, hex_num, float_num, neg_num)
        if final is None:
            return None

        # Check to make sure conversion is done, if it isn't add decimal and loop again
        elif string_of_float is None:
            done = True
        else:
            float_num = True
            num_str = string_of_float
            string_of_float = None
            int_final = final
            final = 0

    # Round to get rid of any repeating values
    return round(final + int_final, len(num_str))


def int_to_hex(num):
    """Turns an integer into a hexadecimal."""
    list_of_hex_chars = "0123456789ABCDEF"
    hex_string = ''
    while num > 0:
        hex_digit = list_of_hex_chars[num % 16]
        hex_string = hex_digit + hex_string
        num //= 16
    if not hex_string:
        hex_string = '0'
    return hex_string


def conv_to_even(hexi):
    """Adds a 0 to the front of a hexadecimal value to make it even."""
    if len(hexi) % 2 != 0:
        hexi = '0' + hexi
    return hexi


def conv_to_big(hexi):
    """Adds spaces in-between the bytes of the hexadecimal string. Returning a big-endian hexadecimal value."""
    big_endian = ''
    for i in range(0, len(hexi), 2):
        byte = hexi[i:i+2]
        if len(byte) < 2:
            byte += '0'  # Pad with 0 if necessary
        big_endian += byte + ' '
    return big_endian.strip()


def conv_to_little(big_endian):
    """Reverses the hexadecimal number to be in little-endian format. Returns a string."""
    bytes_arr = big_endian.split()
    bytes_arr.reverse()
    little_endian = ' '.join(bytes_arr)
    return little_endian


def conv_endian(num, endian='big'):
    """Takes an integer either positive or negative, and the flags 'big' or 'little' and returns a hexadecimal
    value of either a hexadecimal big-endian value if the flag used is 'big' or a hexadecimal little-endian
    value if the flag is 'little'. Returns None if the flag is passed as anything other than 'big' or 'little'."""
    if endian not in ['big', 'little']:
        return None

    hex_str = int_to_hex(abs(num))
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str

    if endian == 'big':
        hex_str = conv_to_big(hex_str)
    else:
        hex_str = conv_to_little(conv_to_big(hex_str))

    if num < 0:
        hex_str = '-' + hex_str

    return hex_str
