from exceptions import WrongUserInput
from utils import format_input_string
_CONVERT_TO_INT = (lambda i: int(i), "Your input doesn't seem to be a number")
_LOWER_CASE = (lambda s: s.lower(), "Why wouldn't this work on a string? You beat me.")
_STRIP_STRING = (lambda s: s.strip(), "I can't think of a reason why this would fail."
                                      "Have you tried turning it off and on again?")

# CONDITIONS:
def _BETWEEN(min, max):
    return (lambda n: min <= n <= max, "Your input doesn't seem to be between {0} and {1}".format(min, max))
_NO_SPACES_IN_STRING = (lambda s: " " not in s, "No spaces allowed in this field.")
_YES_OR_NO = (lambda s: s.lower() in 'yn', "You must answer Yes (y) or No (n).")
_IS_COLOR = (lambda s: s.lower() in ('red', 'yellow', 'blue', 'green'), "Your input doesn't seem to be a color")

def _safe_input(input_string, convertions_and_reasons_for_fail, conditions_and_reasons_for_fail):
    """Keep asking the user for input until he gives an accepted answer.

    @args:
    str: input_string = the text displayed to the user when expecting input

    [(f: a -> b, string)] convertions_and_reasons_for_fail = modifies the user input if it can
        as first element, possible explanation of why it couldn as second element

    [(f: a -> bool, string]) conditions_and_reasons_for_fail = conditions that the modified user
        input should pass as first element, show second element string if it didn't

    @return:
    z, if the last function on convertions_and_reasons_for_fail was of type f: w -> z:
        the user input, validated: it is assured to be of the the correct
        type after all the convertions and can pass all tests given as conditions.

    @sideffects:
    input() function accepted from user.
    """
    while True:
        user_input = input(format_input_string(input_string))
        try:
            correct_type_and_format_user_input = _converter(user_input, *convertions_and_reasons_for_fail)
            _condition_checker(correct_type_and_format_user_input, *conditions_and_reasons_for_fail)
            break
        except WrongUserInput as e:
            print("Woho, not so fast! Your input doesn't seem to be valid. \n"
                   "Maybe the problem has something to with this: \n{0}".format(e.reason))
    return correct_type_and_format_user_input

# YOU SHALL NOT PASS!
def _condition_checker(user_input, *test_condition_and_if_it_didnt_work_why_tuples):
    """Raise a WrongUserInput error if user_input doesn't pass one of the
    tests with its appropiate reason.

    @args:
    str: user_input = the input the user gave
    *(f: a -> bool, str): test_condition_and_if_it_didnt_work_why_tuples =
        arbitrary amount of tuples containing a tester function and an
        explaiation of why it might fail

    @return:
    None

    @raise:
    WrongUserInput
    """
    for condition, reason in test_condition_and_if_it_didnt_work_why_tuples:
        if not condition(user_input):
            raise WrongUserInput(reason)

# Wololo.
def _converter(user_input, *try_converting_and_if_it_did_not_work_why_tuples):
    """Tries to convert user_input according as instructed be the functions

    @args:
    str: user_input = the input the user gave
    *(f: a -> bool, str): test_condition_and_if_it_didnt_work_why_tuples =
        arbitrary amount of tuples containing a tester function and an
        explaiation of why it might fail

    @return:
    z, if the last function on try_converting_and_if_it_did_not_work_why_tuples
        was of type f: w -> z.

    @raise:
    WrongUserInput
    """
    for try_function, reason in try_converting_and_if_it_did_not_work_why_tuples:
        try:
            user_input = try_function(user_input)
        except:
            raise WrongUserInput(reason)
    return user_input

def choose_card(list_of_cards):
    convertions_and_reasons_for_fail = [_CONVERT_TO_INT]
    conditions_and_reasons_for_fail = [_BETWEEN(1, len(list_of_cards))]
    user_input = _safe_input("Choose the card you want to play from the available cards.",
            convertions_and_reasons_for_fail, conditions_and_reasons_for_fail)
    return user_input - 1

def want_to_add_ai_player():
    convertions_and_reasons_for_fail = []
    conditions_and_reasons_for_fail = [_YES_OR_NO]
    res = _safe_input("Do you want to add a new AI player? [Y/n]", convertions_and_reasons_for_fail,
            conditions_and_reasons_for_fail)
    return res.lower() == 'y'

def choose_color():
    convertions_and_reasons_for_fail = [_STRIP_STRING]
    conditions_and_reasons_for_fail = [_IS_COLOR]
    return _safe_input("Choose a color. Valid colors are RED, YELLOW, GREEN, BLUE",
            convertions_and_reasons_for_fail, conditions_and_reasons_for_fail)
