Description

For this project, you and your team will have to implement three functions based on the specifications laid out below. All of your code must be housed in the same file called task.py. This will ensure that everyone has to work on the same file, increasing the chances of merge conflicts. While this may seem counterintuitive, this is a learning exercise, and part of the goal is to practice how to handle things when issues arise.

You are required to use the Continuous Integration workflow you set up in Part 1 of this project. Failure to do so will result in lost points. This means that you are not permitted to change the branch rules to allow for merging without Code Reviews.

You are not permitted to use any Python built-in/library that could make these tasks trivial. Some of these are explicitly forbidden, but it is impossible to list them all, so you need to use your judgment and, when there is any doubt, ask.
Function 1 Specification

This function must have the following header: def conv_num(num_str). This function takes in a string and converts it into a base 10 number, and returns it. It has the following specifications:

    Must be able to handle strings that represent integers
    Must be able to handle strings that represent floating-point numbers
    Must be able to handle hexadecimal numbers with the prefix 0x
        Must be case insensitive
        Negative numbers are indicated with a - like -0xFF
        Only integers are valid inputs for hexadecimal numbers (i.e., no 0xFF.02)
    The type returned must match the type sent. For example, if a string of an integer is passed in, conv_num must return an int.
    Invalid formats should return None (n.b. this is not a string, but the actual None value), including, but not limited to:
        strings with multiple decimal points
        strings with alpha that aren't part of a hexadecimal number
        strings with a hexadecimal number without the proceeding 0x
        values for num_str that are not strings or are empty strings

Some examples:

    conv_num('12345') returns 12345
    conv_num('-123.45') returns -123.45
    conv_num('.45') returns 0.45
    conv_num('123.') returns 123.0
    conv_num('0xAD4') returns 2772
    conv_num('0xAZ4') returns None
    conv_num('12345A') returns None
    conv_num('12.3.45') returns None

You are not permitted to use any of the following: 

    int()
    float()
    hex()
    eval()
    literal_eval()

Function 2 Specification

This function must have the following header: def my_datetime(num_sec). This function takes in an integer value that represents the number of seconds since the epoch: January 1st, 1970. The function takes num_sec and converts it to a date and returns it as a string with the following format: MM-DD-YYYY. It has the following specifications:

    It may be assumed that num_sec will always be an int value
    It may be assumed that num_sec will always be a non-negative value
    Must be able to handle leap years

Some examples:

    my_datetime(0) returns 01-01-1970
    my_datetime(123456789) returns 11-29-1973
    my_datetime(9876543210) returns 12-22-2282
    my_datetime(201653971200) returns 02-29-8360

Your function handle all the computation itself. You are not permitted to use any library that can convert seconds to a date. This includes, but is not limited to:

    datetime
    arrow
    moment
    maya
    delorean
    freezegun

Function 3 Specification

This function must have the following header: def conv_endian(num, endian='big'). This function takes in an integer value as num and converts it to a hexadecimal number. The endian type is determined by the flag endian. The function will return the converted number as a string. It has the following specifications:

    It may be assumed that num will always be an integer
    Must be able to handle negative values for num
    A value of big for endian will return a hexadecimal number that is big-endian
    A value of little for endian will return a hexadecimal number that is little-endian
    Any other values of endian will return None (n.b. this is not a string, but the actual None value)
    The returned string will have each byte separated by a space
    Each byte must be two characters in length

Some examples:

    conv_endian(954786, 'big') returns '0E 91 A2'
    conv_endian(954786) returns '0E 91 A2'
    conv_endian(-954786) returns '-0E 91 A2'
    conv_endian(954786, 'little') returns 'A2 91 0E'
    conv_endian(-954786, 'little') returns '-A2 91 0E'
    conv_endian(num=-954786, endian='little') returns '-A2 91 0E'
    conv_endian(num=-954786, endian='small') returns None

Your function must handle all the computation itself. You are not permitted to use any built-ins such as, but not limited to, to_bytes, bytes, or unpack. You also may not use helpers such as bin or hex.