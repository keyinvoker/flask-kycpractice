def _get_date(date_string):
    string_to_date = date_string.split('-')
    date_split = [int(x) for x in string_to_date]
    return date(date_split[0], date_split[1], date_split[2])

def _get_expiration_date(date_string):
    string_to_date = date_string.split('-')
    date_split = [int(x) for x in string_to_date]
    last_verified_at = date(date_split[0], date_split[1], date_split[2])
    expiration_date = last_verified_at + datetime.timedelta(days=334)
    return expiration_date