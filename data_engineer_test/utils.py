import moment
import re

def strip_whitespace(text):
    text = str(text).replace("\\n", "").replace("\\r", "").strip()
    if text == "":
        return None
    return text

def sanitise_string(text):
    regex = re.compile(r'\\+[\S]{1,5}', flags=re.IGNORECASE)
    text = strip_whitespace(text)
    text = regex.sub('', text)
    return text;

def title_check(text):
    return str(text).title()


def unix_time_to_date(text):
    try:
        date = moment.unix(int(text)).format("YYYY-MM-DD")
    except:
        date = text
    return date