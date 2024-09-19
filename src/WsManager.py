from typing import List, Dict
from fastapi import WebSocket

class WsManager:
    def __init__(self):
        self.heart = '0'  # 初期心拍数
        # 複数の部屋を管理するために辞書を使用します
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        self.active_connections[room_id].remove(websocket)
        if not self.active_connections[room_id]:  # もし部屋に接続が無ければ部屋を削除
            del self.active_connections[room_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, room_id: str):
        for connection in self.active_connections.get(room_id, []):
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message: {e}")

    def set_heart(self, heart_value: str):
        self.heart = heart_value

    def get_heart(self):
        return self.heart