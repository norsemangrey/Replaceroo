"""
                     ,--.
,--.--. ,---.  ,---. |  | ,--,--. ,---. ,---. ,--.--. ,---.  ,---.
|  .--'| .-. :| .-. ||  |' ,-.  || .--'| .-. :|  .--'| .-. || .-. |
|  |   \   --.| '-' '|  |\ '-'  |\ `--.\   --.|  |   ' '-' '' '-' '
`--'    `----'|  |-' `--' `--`--' `---' `----'`--'    `---'  `---'
              `--'

#######################################################################################################################
# Name        : replaceroo
# Description : Text Search and Replace from List
# Author      : Jan Magnus Røkke
# Email       : jan.magnus.rokke@km.kongsberg.com / jan.magnus.roekke@gmail.com
#######################################################################################################################

This script allows the user to replace multiple strings in a plain text file from a list of strings that for instance
can be copied from a spreadsheet column. Files can be dragged-and-dropped into the command line tool.

The user can choose between multiple replacement methods; replacing the original strings with strings in a
corresponding list (l), adding a prefix (p) or adding a suffix (s) to the original strings, or a combination the three.

The tool will accept any file containing plain text as the source file in which the strings will be searched for and
replaced. For now the list of strings to be replaced and (if used) the list of strings to replace the originals must
be text(.txt) file with the strings separated by newline (i.e as one would get by pasting a column from an Excel file
directly into Notepad).

Example:

    Replacement method: lps

    (the strings found in the file from.txt will be replaced with strings in a corresponding list read from to.txt,
    in addition to a prefix and a suffix specified by the user)

    source_text.txt
    ------------------------------------------------------------------------------------------------------------------
    This example text demonstrates the replacement of the strings "word1", "word2" and "word3" in a text file provided
    as the source text. The program will look for the strings in the list read from from.txt, like "word1" and replace
    them according to the specified replacement method.

    To avoid replacing parts of strings like "word10" and "word20", if these are not listed in from.txt, a search
    -prefix and -suffix can be specified so that the replacement function does not identify the 'word1' part of
    'word10' as a string to replace. A search prefix / suffix can for instance be ' ' or '"' depending on the source
    text.
    ------------------------------------------------------------------------------------------------------------------

    from.txt    to.txt
    --------    --------
    word1       new_word1
    word2       new_word2
    word3       new_word3

    Prefix = p_
    Suffix = _s

    Search prefix = "
    Search suffix = "

    After providing the above input and running the replacement function the new modified text will look like this:

    source_text_mod.txt
    ------------------------------------------------------------------------------------------------------------------
    This example text demonstrates the replacement of the strings "p_new_word1_s", "p_new_word2_s" and "p_new_word3_s"
    in a text file provided as the source text. The program will look for the strings in the list read from from.txt,
    like "p_new_word1_s" and replace them according to the specified replacement method.

    To avoid replacing parts of strings like "word10" and "word20", if these are not listed in from.txt, a search
    -prefix and -suffix can be specified so that the replacement function does not identify the 'word1' part of
    'word10' as a string to replace. A search prefix / suffix can for instance be ' ' or '"' depending on the source
    text.
    ------------------------------------------------------------------------------------------------------------------

"""

import tabulate
from typing import List, Tuple


# Main program.
def main():
    """Get source text and replace details from user, replace strings in text, provide summary and save modified file.

    The main program runs the user input-function to prepare the source text and the lists of strings to search for
    and replace, as well as the replace-function that performs the actual search-and-replace according to the lists and
    search strings.

    The function prints a summary of the string replacement and saves the modified text to a new file as well as the
    replacement summary on user acceptance.
    """

    # Get user input (replacement methods, source file and search text).
    input_details, source_text, replace_list, replacement_list = get_user_input()

    # Replace strings in text according to user input.
    modified_text, replace_summary, replace_details = replace_strings(source_text,
                                                                      replace_list,
                                                                      replacement_list,
                                                                      input_details.get("Search Prefix"),
                                                                      input_details.get("Search Suffix"))

    # Prepare a summary of the user input.
    summary_text = "\nInput Details\n"
    summary_text += tabulate.tabulate(input_details.items()) + "\n"

    # Prepare a summary of the string replacement.
    summary_text += "\nReplacement Summary\n"
    summary_text += tabulate.tabulate(replace_summary.items()) + "\n"

    # Prepare a list of the replacements.
    header_details = replace_details[0].keys()
    rows_details = [x.values() for x in replace_details]
    summary_text += "\n" + tabulate.tabulate(rows_details, header_details)

    # Print complete summary.
    print(summary_text)

    # Ask if user wants to save file.
    save_file = input("\nPlease review above summary. Save modified file? [y/n]: ")

    save_summary = input("\nSave a text file with above replacement summary? [y/n]: ")

    # Create text file with summary details.
    if save_summary == "y":
        # Save summary details to new text file.
        summary_path = input_details.get("Source Text File").rsplit(".", 1)[0] + "_mod_summary.txt"
        summary_file = open(summary_path, 'w')
        summary_file.write(summary_text)
        summary_file.close()

        # Inform location.
        print("\nSummary saved as {}".format(summary_path))

    # Create new file or exit without saving.
    if save_file == "y":

        # Save modified text to new file.
        new_path = input_details.get("Source Text File").replace(".", "_mod.")
        new_file = open(new_path, 'w', newline='\n')
        new_file.write(modified_text)
        new_file.close()

        # Inform location.
        print("\nModified file saved as {}".format(new_path))

    else:

        # Inform of exit without saving.
        print("\nExiting without saving modifications.")


# Collect input function.
def get_user_input() -> Tuple[dict, str, list, list]:
    """Gets the input data from the user and prepares the search-and-replace lists.

     The function will query the user for a replacement method where a search-and-replace based on a replacement list,
     a prefix, a suffix, or a combination of the three can be selected. Th user must provide the paths to the source
     text and the search list as well the path replacement list and prefix/suffix strings dependent of the options
     selected. selected.

     The user will also be queried for optional search strings that will be added before and after all the strings
     in the search list when searching for them in the source text.

    Returns:
        details (dict): A dictionary containing the replacement details
                        (file paths, replacement method and search strings).
        text (str): The original text from the source file in which the strings will be replaced.
        from_list (list): A list of strings to replace in the original text.
        to_list (list): A list of string to replace the strings in the original text.

    Raises:
        ValueError: If from_list contains duplicate elements.

    """

    # Initialize
    to_prefix: str = ""
    to_suffix: str = ""
    details: dict = {}

    # Define replacement methods:
    replace_methods = {'l': "List",
                       'p': "Prefix",
                       's': "Suffix",
                       'lp': "List / Prefix",
                       'ls': "List / Suffix",
                       'ps': "Prefix / Suffix",
                       'lps': "List / Prefix / Suffix"}

    # Replacement method.
    while True:

        # Query user for replacement method.
        method = input("Allowed Replacement Methods \n" +
                       tabulate.tabulate(replace_methods.items()) +
                       "\n\nPlease select one of the above methods: ")

        # Check if valid method provided.
        if method in replace_methods.keys():

            # Update input details.
            details["Replace Method"] = replace_methods.get(method)

            # Exit loop.
            break

        else:

            # Inform of invalid input.
            print("\nYour input did not match a valid method.")

    # Source file preparation.
    while True:

        # Get file path:
        source_path = input("\nProvide source file (path): ").replace('"', '')

        try:

            # Open file.
            source_file = open(source_path, 'U')

            # Read the source file.
            text = source_file.read()

        except (IOError, OSError, ValueError) as err:

            # Inform of error.
            print("\nThere was an error opening the file. Please check the path/file and try again.")
            print(err)

            # Retry input.
            continue

        else:

            # Close original file.
            source_file.close()

            # Update input details.
            details["Source Text File"] = source_path

            # Exit loop.
            break

    # 'From' reference list preparation.
    while True:

        # Get file path:
        from_list_path = input("\nProvide 'from' reference list file (path): ").replace('"', '')

        try:

            # Open file.
            from_list_file = open(from_list_path, 'r')

            # Make list of words from reference file and remove duplicates.
            from_list = [line for line in from_list_file.read().splitlines()]

        except (IOError, OSError, ValueError) as err:

            # Inform of error.
            print("\nThere was an error opening the file. Please check the path/file and try again.")
            print(err)

        else:

            # Check for identical elements/strings.
            if len(from_list) != len(set(from_list)):

                # Raise exception.
                raise ValueError("\nThere are duplicate elements in the list. Please revise and try again.")

            # Close the reference file.
            from_list_file.close()

            # Update input details.
            details["Replace List File"] = from_list_path

            # Exit loop.
            break

    # Handle the selected replacement method.
    if method.count('l'):

        # 'To' reference list preparation.
        while True:

            # Get file path.
            to_list_path = input("\nProvide 'to' reference list file (path): ").replace('"', '')

            try:

                # Open file.
                to_list_file = open(to_list_path, 'r')

                # Make list of words from reference file and remove duplicates.
                to_list = [line for line in to_list_file.read().splitlines()]

            except (IOError, OSError, ValueError) as err:

                # Inform of error.
                print("\nThere was an error opening the file. Please check the path/file and try again.")
                print(err)

            else:

                # Check for identical elements/strings.
                if len(to_list) != len(set(to_list)):
                    print("\nNote: There are duplicate elements in the list.")

                # Update input details.
                details["Replacement List File"] = to_list_path

                # Close the reference file.
                to_list_file.close()

                # Exit loop.
                break

        # Transfer to temporary list.
        temp_list = to_list

    else:

        # Transfer 'from' list to temporary list.
        temp_list = from_list

    # Check if prefix selected.
    if method.count('p'):

        # Get prefix from user.
        to_prefix = input("\nPlease provide the prefix to be added to all strings in 'from' list: ")

        # Update input details.
        details["Replacement Prefix"] = to_prefix

    # Check if suffix selected.
    if method.count('s'):

        # Get suffix from user.
        to_suffix = input("\nPlease provide the suffix to be added to all strings in 'from' list: ")

        # Update input details.
        details["Replacement Suffix"] = to_suffix

    # Create 'to' list.
    to_list = [to_prefix + fromStr + to_suffix for fromStr in temp_list]

    # Check for identical number of elements in 'from' and 'to' list.
    if len(from_list) != len(to_list):
        print("\nNote: The 'from' and 'to' list does not contain equal number of elements.")

    # Search prefix and suffix.
    while True:

        # Word list prefix and suffix if any.
        print("\nPlease provide source file search prefix and suffix for unique ID"
              "\n(e.g. so not to match 80TE4000 in 80TE4000A)\n")

        search_prefix = input(r"Search prefix (use \n for newline): ")
        search_suffix = input(r"Search suffix (use \n for newline): ").replace('\\n', '\n')

        # Provide example from list.
        print("\nWill search for strings with the following format: ",
              search_prefix + "<string from list>" + search_suffix,
              " (e.g. \'", search_prefix + from_list[0] + search_suffix, "\')")

        # Confirm with user.
        if input("\nRe-enter string search parameters? [y]") != 'y':

            # Update input details.
            if search_prefix != "":

                details["Search Prefix"] = search_prefix

            # Update input details.
            if search_suffix != "":

                details["Search Suffix"] = search_suffix

            # Exit loop.
            break

    # Return input data.
    return details, text, from_list, to_list


# Replace function.
def replace_strings(text: str, from_list: list, to_list: list, prefix: str = "", suffix: str = "") \
        -> Tuple[str, dict, list]:
    """Search and replaces strings in text by lists with original/new strings.

    The function takes a text (as string) as well as two lists (of strings) of equal lengths, searches the text for
    strings in the first list and replaces them with the corresponding strings in the second list.

    In addition optional search prefix and suffix strings can be specified that will be added to every string when
    searching the text.

     The first list cannot contain duplicate elements and both lists must be of equal lengths. However, both lists can
     contain empty strings (although the first list can only contain one instance).

    Args:
        text (str): A text (for instance from a file) in which strings will be replaced according to the two lists.
        from_list (List[str]): A list of strings that will be searched for in the source text.
        to_list (List(str)): A list of strings that will replace the strings from the first list in the source text.
        prefix (Optional[str]): A string added as prefix to the string to be replaced when searching the source text.
        suffix (Optional[str]): A string added as a suffix to the string to be replaced when searching the source text.

    Returns:
        text (str): The modified text with replaced strings.
        summary (dict): A dictionary with a summary of the replacement (number of strings replaced etc.).
        details (List[dict]): A list of dictionaries with all the replacements including search strings.
    """

    # Initialize variables.
    index: int = 0
    count: int = 0
    not_found: List[str] = []
    details: List[dict] = []

    # Do search and replace for all the words in the list.
    for from_string, to_string in zip(from_list, to_list):

        # Add search prefix and suffix to strings.
        replace_from = prefix + from_string + suffix
        replace_to = prefix + to_string + suffix

        # Count number if instances of word in file.
        instances = text.count(replace_from)

        # Check if word is in file and replace or log not found.
        if instances > 0:

            # Replace word with new text.
            text = text.replace(replace_from, replace_to, instances)

            # Increment total 'replaced' count.
            count = count + instances

        else:

            # Append to list of words not found.
            not_found.append(from_string)

        # Increment list index counter.
        index += 1

        # Gather replacement details in dictionary.
        detail = {
            "Original String": from_string,
            "Full Search String": replace_from,
            "New String": to_string,
            "Full Replace": replace_to,
            "Instances": instances}

        # Append to list.
        details.append(detail)

    # Sort the list of details by number of instances.
    details = sorted(details, key=lambda k: k['Instances'])

    # Gather summary info.
    summary = {
        "Searched for Strings": index,
        "Strings Found": sum(i.get('Instances') > 0 for i in details),
        "Strings Not Found": sum(i.get('Instances') == 0 for i in details),
        "Total Replaced": count,
        "Multiple Instances": sum(i.get('Instances') > 1 for i in details)}

    # Return data.
    return text, summary, details


# Check if direct call of module.
if __name__ == "__main__":

    # Print the module documentation to the user.
    print(__doc__)

    # Will execute the program main function when the module is executed directly.
    main()
