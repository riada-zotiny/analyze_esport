import asyncio
from g3pylib import (
    DEFAULT_HTTP_PORT,
    DEFAULT_RTSP_LIVE_PATH,
    DEFAULT_RTSP_PORT,
    connect_to_glasses,
)
from g3pylib.zeroconf import DEFAULT_WEBSOCKET_PATH, G3ServiceDiscovery

G3_HOSTNAME = "TG03B-080202027181.local"

async def test_connect_with_service_using_ip(g3_hostname: str):
    g3_service = await G3ServiceDiscovery.request_service(g3_hostname)
    async with connect_to_glasses.with_service(g3_service, using_ip=False) as g3:
        serial = await g3.system.get_recording_unit_serial()
        print(f"Connecté à : {serial} ")
        
async def connect():
    async with connect_to_glasses.with_hostname( G3_HOSTNAME, using_zeroconf=False, using_ip=True) as g3:
        serial = await g3.system.get_recording_unit_serial()
        print(f"Connecté à : {serial} ")

        await g3.recorder.start()
        print("Enregistrement a comméncé !")

        await asyncio.sleep(10)

        await g3.recorder.stop()
        print("Enregistrement terminéé ")

       
       
async def test_connect_with_urls(g3_hostname: str):
    async with connect_to_glasses.with_url(
        f"ws://{g3_hostname}{DEFAULT_WEBSOCKET_PATH}",
        f"rtsp://{g3_hostname}:{DEFAULT_RTSP_PORT}{DEFAULT_RTSP_LIVE_PATH}",
        f"http://{g3_hostname}:{DEFAULT_HTTP_PORT}",
    ) as g3:
        serial = await g3.system.get_recording_unit_serial()
        assert type(serial) is str    

async def main():
    await test_connect_with_urls(G3_HOSTNAME)

asyncio.run(main())
