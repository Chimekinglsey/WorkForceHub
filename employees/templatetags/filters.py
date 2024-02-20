from django import template

register = template.Library()

@register.filter
def month_name(month_number):
    month_number = int(month_number)
    months = {
        1: 'Jan.',
        2: 'Feb.',
        3: 'Mar.',
        4: 'Apr.',
        5: 'May',
        6: 'Jun.',
        7: 'Jul.',
        8: 'Aug.',
        9: 'Sep.',
        10: 'Oct.',
        11: 'Nov.',
        12: 'Dec.',
    }
    return months.get(month_number, '')