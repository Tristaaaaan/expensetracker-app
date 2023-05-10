import locale

def money(value):
    locale.setlocale(locale.LC_ALL, 'en_PH.UTF-8')

    if value >= 1000000:
        return '₱{:.2f}M'.format(value/1000000)
    else:
        return locale.currency(value, grouping=True)
