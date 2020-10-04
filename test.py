import json

categories = {
    1: 
    {
        'name': 'Excerpt',
        "parent": None
    },

    2:
    {
        'name': 'Thoughts',
        'parent': None
    },
    
    3:
    {
        'name': 'Testimony',
        'parent': None
    },

    4:
    {
        'name': 'Others',
        'parent': None
    }
}

permissions = {
    1: 
    {
        'name': 'members', 
        'power': 0
    },

    2:
    {
        'name': 'admins',
        'power': 10
    },

    3:
    {
        'name': 'devs',
        'power': 100
    }
}

with open('tables/permissions.JSON', 'r') as txt:    
    yeet = json.load(txt)

print(str(yeet))