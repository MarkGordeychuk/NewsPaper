from django import template


BAD_WORDS = (
    'badword',
    'badwords',
)


register = template.Library()


@register.filter()
def censor(content: str):
    new_content = ''
    word = ''
    for char in content:
        if char.isalpha():
            word += char
        else:
            new_content += ('*' * len(word) if word.lower() in BAD_WORDS else word) + char
            word = ''
    new_content += '*' * len(word) if word.lower() in BAD_WORDS else word
    return new_content


@register.filter()
def name_lastname(user):
    return f"{user.first_name} {user.last_name}" if user.first_name or user.last_name else user.username
