import asyncio
from g3pylib import connect_to_glasses

G3_HOSTNAME = "192.168.75.51"

async def connect():
    async with connect_to_glasses.with_hostname( G3_HOSTNAME, using_zeroconf=False, using_ip=True) as g3:
        serial = await g3.system.get_recording_unit_serial()
        print(f"Connecté à : {serial} ")

        await g3.recorder.start()
        print("Enregistrement a comméncé !")

        await asyncio.sleep(10)

        await g3.recorder.stop()
        print("Enregistrement terminéé ")

       
       
async def main():
    await connect()


asyncio.run(main())
"""
['APIComponent', 'Any', 'AsyncIterator', 'Calibrate', 'Coroutine', 'DEFAULT_HTTP_PORT', 'DEFAULT_RTSP_LIVE_PATH',
 'DEFAULT_RTSP_PORT', 'DEFAULT_WEBSOCKET_PATH', 'FeatureNotAvailableError', 'G3Service', 'G3ServiceDiscovery',
 'G3WebSocketClientProtocol', 'Generator', 'Glasses3', 'LoggerLike', 'Optional', 'Recorder', 'Recordings', 'Rudimentary',
 'Settings', 'Streams', 'System', 'TracebackType', 'Tuple', 'Type', 'URI', '__builtins__', '__cached__', '__doc__', '__file__',
 '__loader__', '__name__', '__package__', '__path__', '__spec__', '__version__', '_logger', '_utils', 'annotations',
 'asynccontextmanager', 'calibrate', 'cast', 'connect_to_glasses', 'exceptions', 'g3pylib', 'g3typing', 'logging', 'recorder',
 'recordings', 'rudimentary', 'settings', 'streams', 'system', 'websocket', 'zeroconf']"""