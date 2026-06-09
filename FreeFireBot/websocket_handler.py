import asyncio
import websockets
import json
from typing import Optional

class FreeFireWebSocket:
    def __init__(self):
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        # WebSocket الرسمي لـ Free Fire (يحتاج مفتاح API)
        self.WS_URL = "wss://api.freefirecommunity.com/v1/ws"
        
    async def connect(self, api_key: str):
        """الاتصال بخادم WebSocket"""
        try:
            self.websocket = await websockets.connect(
                self.WS_URL,
                extra_headers={"X-API-Key": api_key}
            )
            print("[WS] ✅ متصل بخادم Free Fire")
            return True
        except Exception as e:
            print(f"[WS] ❌ فشل الاتصال: {e}")
            return False
    
    async def send_like(self, player_id: str):
        """إرسال لايك للاعب"""
        if not self.websocket:
            return False
        
        message = {
            "action": "like",
            "player_id": player_id,
            "type": "normal"  # or "me", "clap"
        }
        await self.websocket.send(json.dumps(message))
        print(f"[WS] 👍 تم إرسال لايك للاعب {player_id}")
        return True
    
    async def get_player_stats(self, player_id: str):
        """جلب معلومات اللاعب"""
        if not self.websocket:
            return None
        
        message = {
            "action": "get_player",
            "player_id": player_id
        }
        await self.websocket.send(json.dumps(message))
        response = await self.websocket.recv()
        return json.loads(response)
    
    async def close(self):
        if self.websocket:
            await self.websocket.close()