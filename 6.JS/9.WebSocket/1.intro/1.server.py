# pip install websockets
import asyncio
import websockets

# 클라이언트가 요청하면 부를 함수
async def handle_client(websocket):
    print('웹소켓 요청이 올 때마다 실행')
    await websocket.send('서버에 연결되었습니다.')

    try:
        async for message in websocket:
            print('클라이언트 메시지: ', message)
            await websocket.send(f'서버가 받은 메시지: {message}')
    except websockets.exceptions.ConnectionClosed:
        print('클라이언트가 연결을 종료했습니다.')

async def main():
    print('메인 함수 실행')
    async with websockets.serve(handle_client, 'localhost', 8000):
        print('웹소켓 오픈: ws://localhost:8000')
        await asyncio.Future()  # 요청이 올 때까지 대기

asyncio.run(main())