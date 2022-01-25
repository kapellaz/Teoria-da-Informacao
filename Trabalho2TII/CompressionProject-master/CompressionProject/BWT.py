def bwt_tranf(d):
    Input = d
    assert "£" not in Input                     # Input string cannot contain $
    Input = Input + "£"                         # Add "$" to the end of the string

    table = [Input[i:] + Input[:i] for i in range(len(Input))]  # Table of rotations of string

    table = sorted(table)

    last_column = [row[-1:] for row in table]             # Last characters of each row
    bwt = ''.join(last_column)
    return bwt