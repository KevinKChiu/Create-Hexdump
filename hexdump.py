import sys


def createBytesList(data: str) -> list:
    """Return the hex data grouped in bytes as a list."""
    dataList = []

    for i in range(0, len(data), 2):
        dataList.append(data[i : i + 2])

    return dataList


def hexToPerusalFormat(line: str) -> str:
    """Return the perusal format of the given hex string line as a string."""
    perusal_line = "|"
    hexList = line.split(" ")[0:-1]
    for i in range(0, len(hexList)):
        hex_to_num = int(hexList[i], 16)
        if hex_to_num in range(32, 127):
            perusal_line += chr(hex_to_num)
        else:
            perusal_line += "."
    return perusal_line + "|"


def createOffset(byteCount: int) -> str:
    """Return the offset of the number of bytes in hex as a string."""
    return format(byteCount, "08x")


def isLastElem(idx: int, dataList: list) -> bool:
    """Return true if the index is at the last element of the given list."""
    return idx == len(dataList) - 1


def createEmptyHexWhitespace(dataList: list) -> list:
    """Return a list of white spaces for the missing bytes of one line."""
    spaces = []
    count = 16 - (len(dataList) % 16)
    if count == 8:
        spaces.append(" ")
    while count != 0:
        spaces.append("   ")
        count -= 1
        if count % 8 == 0:
            spaces.append(" ")
    return spaces


def createHexdump(data: str) -> list:
    """Return a string list of the entire hexdump of the given data."""
    dataList = createBytesList(data)
    result = []
    if dataList:
        result.append("0" * 8 + "  ")  # Create first offset
    temp_line = ""
    line = ""
    byte_count = 0
    total_byte_count = 0
    for i in range(0, len(dataList)):  # Loop through hex data list
        temp_line += dataList[i] + " "  # Add the current byte to the line
        byte_count += 1
        total_byte_count += 1

        if byte_count == 8 or isLastElem(i, dataList):
            result.append(temp_line)
            if not isLastElem(i, dataList) or total_byte_count % 16 == 0:
                result.append(" ")
            byte_count = 0  # Reset byte counter
            line += temp_line  # Append line of 8 bytes to the current line
            temp_line = ""

        # Reach end of hexdump line
        # Create extra whitespace for missing bytes
        # Finish off the current line with the perusal format of the bytes
        # Add the offset of bytes as a new line
        if total_byte_count % 16 == 0 or isLastElem(i, dataList):
            if len(dataList) % 16 != 0 and isLastElem(i, dataList):
                result += createEmptyHexWhitespace(dataList)
            result.append(hexToPerusalFormat(line))
            result.append("\n")
            offset = createOffset(total_byte_count)
            if isLastElem(i, dataList):
                result.append(offset)
            else:
                result.append(offset + "  ")
            line = ""

    return result


def printHexdump(data: str) -> None:
    """Print the hexdump of the given data."""
    if data:
        hexdump = createHexdump(data)
        hexdump_str = "".join(hexdump)
        print(hexdump_str)


if __name__ == "__main__":
    """Open the file given in the command line in binary mode, read the
    file contents as hex bytes, and print the hexdump of the given file.
    """
    filename = sys.argv[1]
    with open(filename, "rb") as filedes:
        data = filedes.read().hex()
        printHexdump(data)
