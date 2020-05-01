from routes import app

import hypercorn.asyncio
import asyncio


async def main():
    await hypercorn.asyncio.serve(app, hypercorn.Config())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
