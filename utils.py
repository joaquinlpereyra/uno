class Colors:
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    YELLOW = 'yellow'

def format_strings(*strings):
    """Take an arbitrary number of strings and format them nicely.
    Returns the nicely formatted string.
    """
    accum_string = ""
    for str in strings:
        accum_string = "{0} {1}\n".format(accum_string, str)
    return accum_string

def format_input_string(*strings):
    """Takes an arbitrary number of strings and format them nicely with a
    '>>>' added on a new line to show the user the program is waiting for
    its input.

    Return the nicely formatted string.
    """
    nice_string = format_strings(*strings)
    final_string = "{0}\n>>> ".format(nice_string) if nice_string else '>>> '
    return final_string

def pretty_print(*strings):
    """Print an arbtrary number of strings.

    Return None.
    """
    print(format_strings(*strings))

def pretty_print_as_supermarket_list(title, *strings):
    """Print a title (for no title, give a falsey value on first param)
    and an arbitrary number of strings like it was a nice supermarket list.
    """
    if title and strings:
        print('[{0}]'.format(title))

    for index, string in enumerate(strings, start=1):
        print('{0}.\t{1}'.format(index, string))

def pretty_print_as_supermarket_list_a_dictionary(titles_strings_dictionary):
    if not titles_strings_dictionary:
        print("No results for this query")

    for title, strings in titles_strings_dictionary.items():
        title  = title if title else 'No tag'
        pretty_print_as_supermarket_list(title, *strings)
