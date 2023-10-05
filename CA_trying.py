# cellular automata
def trigram_creator(text):
    trigrams = []
    for item_index in range(len(text) - 2):
        addition = text[item_index:item_index+3]
        trigrams.append(addition)
    return trigrams


def main():
    starting_state = "0001000"
    trigrams = trigram_creator(starting_state)
    print(trigrams)


main()
