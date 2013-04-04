from common import *
ITEMS = {}

def get(item=None):
    if item == None:
        return OkResponse(ITEMS)
    elif not item in ITEMS:
        return NotFoundResponse('Could not find ' + str(item))
    return OkResponse(ITEMS[item])


def post(item, content):
    if item in ITEMS:
        return ConflictResponse('Already exists')
    ITEMS[item] = content
    return CreatedResponse(content)

def delete(item):
    if not item in ITEMS:
        return NotFoundResponse('Could not find ' + str(item))
    removed = ITEMS[item]
    del ITEMS[item]
    return OkResponse({'removed': removed})


def put(item, content):
    if not item in ITEMS:
        return NotFoundResponse('Could not find ' + str(item))
    updated = ITEMS[item]
    ITEMS[item] = content
    return OkResponse({'old': updated, 'new': content})
