# mtfwiki.py
import RLE
from typing import List, Tuple, Union
# Instead of always transmitting an "original" dictionary, it is simpler to just agree on an initial set.
# Here we use the 256 possible values of a byte:
common_dictionary = list(range(256))

def encode(plain_text: str) -> List[int]:
    # Change to bytes for 256.
    plain_text = plain_text.encode('utf-8')

    # Changing the common dictionary is a bad idea. Make a copy.
    dictionary = common_dictionary.copy()

    # Transformation
    compressed_text = list()          # Regular array
    rank = 0

    # Read in each character
    for c in plain_text:
        rank = dictionary.index(c)    # Find the rank of the character in the dictionary [O(k)]
        compressed_text.append(rank)  # Update the encoded text

        # Update the dictionary [O(k)]
        dictionary.pop(rank)
        dictionary.insert(0, c)

    return compressed_text            # Return the encoded text

