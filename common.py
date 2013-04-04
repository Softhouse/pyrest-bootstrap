import json
from collections import namedtuple
Response = namedtuple('response', 'status content')
OkResponse = lambda msg: Response('200 Ok', json.dumps(msg))
CreatedResponse = lambda msg: Response('201 Created', json.dumps(msg))
MalformedResponse = lambda msg: Response('400 Malformed Request', json.dumps(msg))
UnauthorizedResponse = lambda msg: Response('401 Unauthorized',json.dumps( msg))
NotFoundResponse = lambda msg: Response('404 Not found', json.dumps(msg))
UnsupportedResponse = lambda msg: Response('405 Method Not Allowed', json.dumps(msg))
ConflictResponse = lambda msg: Response('409 Conflict', json.dumps(msg))
ErrorResponse = lambda msg: Response('500 Internal Server Error', json.dumps(msg))