SNAKE_CASE_BREAK_CHARACTERS = set([' ','_'])


def snake_case(subject, ignore_suffix=''):
    """ Convert the given subject string from NotSnakeCase to snake_case. """

    suffix_length = len(ignore_suffix)
    subject_length = len(subject)
    result = ''

    # NOTE: Not sure if I want to use >= here since it has potential to omit an
    # empty string, and does it really count as a suffix if it's the entire
    # string anyway? *ponder*

    if ignore_suffix and subject_length > suffix_length:
        offset = suffix_length * -1

        # Truncate the suffix if it's a match
        if subject[offset:].lower() == ignore_suffix.lower():
            subject = subject[:offset]

        # Reset subject_length since we've modified it
        subject_length = len(subject)

    for index in range(subject_length):
        character = subject[index]

        if character in SNAKE_CASE_BREAK_CHARACTERS:
            continue

        next_character = character.lower()

        # Ensure that we don't check the first or last index
        if 1 < index+1 < subject_length:
            next_character_is_break = subject[index+1] in SNAKE_CASE_BREAK_CHARACTERS 
            was_lower_cased = subject[index] != next_character

            if next_character_is_break or was_lower_cased:
                result += '_'

        result += next_character

    return result


def permit_import_errors(name):
    """ Skip ImportError since it only means that the module doesn't exist. """

    if issubclass(sys.exc_info()[0], ImportError):
        return

    raise
