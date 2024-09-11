import json
from fastapi import WebSocket

class WsConnectionManagerManyDeviceTypes:
    """Class defining socket events"""
    
    def __init__(self):
        self.connection_file = "ws_active_connections_by_data.json"
        self.load_connections()
        print("active_connections",self.active_connections)

    def load_connections(self):
        try:
            with open(self.connection_file, "r") as file:
                data = file.read()
                if data:
                    self.active_connections = json.loads(data)
                    
                    print("active_connections",self.active_connections)
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

    async def connect(self, data_type:str, client_id: str, device_id: str, device: str, websocket: WebSocket):
        user_id = f"{data_type}-{client_id}-{device_id}-{device}"
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        self.save_connections()

    def disconnect(self, websocket: WebSocket, data_type:str, client_id: str, device_id: str, device: str):
        user_id = f"{data_type}-{client_id}-{device_id}-{device}"
        
        if user_id in self.active_connections:
            self.active_connections[user_id] = [conn for conn in self.active_connections[user_id] if conn != websocket]
            if not self.active_connections[user_id]:  # If list is empty
                del self.active_connections[user_id]
            self.save_connections()









    async def send_personal_message(self, data_type:str, client_id: str, device_id: str, device: str, message: str):
        user_id = f"{data_type}-{client_id}-{device_id}-{device}"
        if user_id in self.active_connections:
            for websocket in self.active_connections[user_id]:
                await websocket.send_text(message)
        else:
            print("User not in active_connections")

    # async def send_one_time_message(self, client_id, device_id, device):
    #     await EnergyController.send_last_energy_data(client_id, device_id, device)