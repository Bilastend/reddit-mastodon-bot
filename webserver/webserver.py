from aiohttp import web
import aiohttp
import asyncio
import socketio
from image_processor import ImageProcessor

# TODO: Maybe change cors_allowed_origins to something stricter(?)
sio = socketio.AsyncServer(cors_allowed_origins='*')


async def index(request):
    with open('webserver/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


async def image(request):
    return web.FileResponse('./image.png')


async def styles(request):
    return web.FileResponse('webserver/styles.css')


async def run_server():
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get('/image.png', image)
    app.router.add_get('/styles.css', styles)
    sio.attach(app)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)
    await site.start()
    await asyncio.Event().wait()


@sio.event
async def update(data):
    image_processor = ImageProcessor()
    await sio.emit('change label', image_processor.desc)


@sio.event
async def set_alt_text(data, text):
    if text == '':
        return
    image_processor = ImageProcessor()
    image_processor.desc = text
    await sio.emit('change label', image_processor.desc)