def reset_file(filename: str):
    """
    :param filename: File to be reset.
    :returns Nothing: Resets a File by writing the empty string to it.
    """
    file = open(filename, "w")
    file.write("")
    file.close()


def write_to_file(filename: str, text: list, multiple_lines=False):
    """
    :param filename: File to be written to.
    :param text: Text to be written to file.
    :param multiple_lines: Flag for outputting to multiple lines of the file.
    :returns (Written to File): text
    """
    file = open(filename, "a")
    for data in text:
        if str(data) != "":
            file.write(str(data))
            if multiple_lines:
                file.write("\n")
    file.write("\n")
    file.close()
