import datetime


def search4vowels(word: str) -> set:
    """ Return any vowels found in word"""
    vowels = set('aeiou')
    return vowels.intersection(set(word))


def search4letters(phrase: str, letters: str = 'aeiou') -> set:
    """ Return any letters found in phrase """
    return set(letters).intersection(set(phrase))

def log_request(req: 'flask_request', res: str) -> None:
    """ logger for web operations """
    with open('search.log', 'a') as log:
        #print(str(dir(req)), '=', res, file=log)
        print(req.form, req.remote_addr, req.user_agent, res, str(datetime.datetime.today()),file=log, sep='|')