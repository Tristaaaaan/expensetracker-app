
def money(value):

    if value >= 1000000:
        return '${:.2f}M'.format(value/1000000)
    else:
        return '${:.2f}'.format(value)
