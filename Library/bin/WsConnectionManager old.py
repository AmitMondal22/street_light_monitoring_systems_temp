import json
from fastapi import WebSocket
from typing import Dict, List

class WsConnectionManager:
    """Class defining socket events"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.connection_file = "active_connections.json"
        self.load_connections()

    def load_connections(self):
        try:
            with open(self.connection_file, "r") as file:
                data = file.read()
                if data:
                    self.active_connections = json.loads(data)
                else:
                    self.active_connections = {}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.active_connections = {}

    def save_connections(self):
        connections_data = {}
        for user_id, sockets in self.active_connections.items():
            connections_data[user_id] = [str(socket) for socket in sockets]
        with open(self.connection_file, "w") as file:
            json.dump(connections_data, file)

    async def connect(self, client_id: str, device_id: str, device: str, websocket: WebSocket):
        user_id = f"{client_id}-{device_id}-{device}"
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        self.save_connections()

    def disconnect(self, websocket: WebSocket, client_id: str, device_id: str, device: str):
        user_id = f"{client_id}-{device_id}-{device}"
        
        if user_id in self.active_connections:
            self.active_connections[user_id] = [conn for conn in self.active_connections[user_id] if conn != websocket]
            if not self.active_connections[user_id]:  # If list is empty
                del self.active_connections[user_id]
            self.save_connections()








    async def send_personal_message(self, client_id: str, device_id: str, device: str, message: str):
        user_id = f"{client_id}-{device_id}-{device}"
        print("activity connections///////////////",self.active_connections)
        if user_id in self.active_connections:
            for websocket in self.active_connections[user_id]:
                await websocket.send_text(message)
        else:
            print("user_id not in active_connections")
            
    async def broadcast(self, message: str):
        """Broadcast message to all active connections"""
        for connection in self.active_connections.values():
            for websocket in connection:
                await websocket.send_text(message)

    # async def send_one_time_message(self, client_id, device_id, device):
    #     await EnergyController.send_last_energy_data(client_id, device_id, device)