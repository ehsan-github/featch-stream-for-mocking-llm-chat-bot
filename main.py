import asyncio
import random 

from starlette.applications import Starlette
from starlette.responses import StreamingResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route



import json 

sampleOutPut = []

with open('messages.json') as file:
    sampleOutPut = json.load(file)


async def slow_numbers(maximum):
    for number in range(maximum):
        yield f'data: {sampleOutPut[number]}\n\n' 
        await asyncio.sleep(random.random() * 1)

    yield f'data: [DONE]\n\n' 


async def stream(request):
    generator = slow_numbers(len(sampleOutPut))
    return StreamingResponse(generator, media_type='application/jsonl')

def startup():
    print('Ready to go')


routes = [
    Route('/', endpoint=stream),
    # Route('/user/me', user_me),
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

app = Starlette(debug=True, middleware=middleware, routes=routes, on_startup=[startup])





