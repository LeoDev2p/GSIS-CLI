import re
from functools import wraps



date1 = "2026-10-12"
date2 = "2026/10/12"

if all (filter (validate_date, (date1, date2))):
    normalize = [x.replace ("/", "-") for x in (date1, date2)]
    print (normalize)