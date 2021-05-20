from urllib import request

base_url = "http://oeis.org/A{}/b{}.txt"

# Stores sequences which have been searched for
cache = {}

# Base length of sequence to retrieve
l = 25


def fit_sequence_number(num):
    # Match A000000 format
    out = str(num)
    while len(out) < 6:
        out = "0" + out
    return out


def get_sequence_from_b_file(sequence_name):
    sequence_name = fit_sequence_number(sequence_name)

    # Return existing sequence from cache
    if sequence_name in cache:
        return "A" + sequence_name + ": " + cache[sequence_name]

    # Grab the b-file
    html = request.urlopen(base_url.format(sequence_name, sequence_name)).read().decode("utf-8")
    split_html = html.split("\n")

    # Grab the members of the sequence
    out = []
    for k in range(min(len(split_html), l)):
        split = split_html[k].split(" ")
        if len(split) == 2:
            out.append(split[1])

    # Cache and return
    cache[sequence_name] = ", ".join(out)
    return "A" + sequence_name + ": " + ", ".join(out)
