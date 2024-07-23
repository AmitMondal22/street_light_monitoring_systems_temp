from fastapi import WebSocket
from typing import Dict,List
from controllers.device_to_server import EnergyController

class WsConnectionManager:
    """Class defining socket events"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

# ====================================================================
# ====================================================================
    async def connect(self, client_id: str, device_id: str, device: str, websocket: WebSocket):
        user_id = f"{client_id}-{device_id}-{device}"
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        
        

    def disconnect(self, websocket: WebSocket, client_id: str, device_id: str, device: str):
        user_id = f"{client_id}-{device_id}-{device}"
        if user_id in self.active_connections:
            self.active_connections[user_id] = [conn for conn in self.active_connections[user_id] if conn != websocket]

# ====================================================================
# ====================================================================

    async def send_personal_message(self, client_id: str, device_id: str, device: str, message: str):
        user_id = f"{client_id}-{device_id}-{device}"
        if user_id in self.active_connections:
            for websocket in self.active_connections[user_id]:
                await websocket.send_text(message)
        else:
            print("user_id not in active_connections")
            
    # async def send_text_to_all(self, text: str):
    #     for connection in self.active_connections:
    #         await connection.send_text(text)
            
    
    async def broadcast(self, message: str):
        """Broadcast message to all active connections"""
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def send_one_time_message(self, client_id, device_id, device):
        await EnergyController.send_last_energy_data(client_id, device_id, device)