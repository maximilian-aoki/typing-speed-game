
def score_check(correct_version, to_check, secs_elapsed):
    # create lists of the API/player paragraphs containing all words separated by spaces
    correct_list = correct_version.split(" ")
    check_list = to_check.split(" ")

    # simple algorithm for matching words and counting total correct words
    total_words = len(correct_list)
    total_correct = 0
    while len(correct_list) > 0 and len(check_list) > 0:
        if check_list[0] == correct_list[0]:
            total_correct += 1

        correct_list.remove(correct_list[0])
        check_list.remove(check_list[0])

    # get values and convert to string format
    wpm = total_correct * (60 / secs_elapsed)
    wpm_str = "{:.1f}".format(total_correct * (60 / secs_elapsed))

    accuracy = int((total_correct / total_words) * 100)
    accuracy_str = str(accuracy) + "%"

    # This formula was calculated using an actual multivariate linear regression of data that was purely guess-timated
    # see resources/ballpark-score-values.csv
    score = (wpm * 0.322) + (accuracy * 0.547)

    # ranking system
    if score > 90:
        rank = "Grand Typemaster"
    elif score > 80:
        rank = "Potentially a Bot"
    elif score > 70:
        rank = "Could be a Secretary"
    elif score > 60:
        rank = "Deserves a Raise"
    elif score > 50:
        rank = "Absolutely Average"
    elif score > 40:
        rank = "Sub-Par Pleb"
    elif score > 30:
        rank = "You use 2 fingers"
    elif score > 20:
        rank = "Sleep-Deprived Anteater"
    elif score > 10:
        rank = "3-Cell Organism"
    else:
        rank = "Amoeba"

    # returns a dictionary
    return {
        "wpm": wpm_str,
        "accuracy": accuracy_str,
        "score": score,
        "rank": rank
    }
