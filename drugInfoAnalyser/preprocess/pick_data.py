from fuzzywuzzy import fuzz

from preprocess import e_analyser


def judge(sent):
    events = e_analyser.find_event(sent)
    if "metabolism" in events:
        return True
    elif "serum concentration" in events:
        return True
    elif "excretion rate" in events:
        return True
    elif "therapeutic efficacy" in events:
        return True
    elif ("risk" in events) or ("severity" in events):
        return True
    else:
        for e in events:
            if fuzz.partial_ratio(e, "activities") >= 99:
                return True
    return False
