import string
import random


# CREATE RANDOM UNIQUE ID
def invoke_uid(length=10, prefix="uid"):
    char_pool = string.ascii_lowercase + string.ascii_uppercase + string.digits
    uid = "".join(random.choices(char_pool, k=length))
    return f'{prefix}_{uid}'
