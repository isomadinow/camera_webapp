from app.models.camera_model import CameraModel
from app.models.truck_model import TruckModel
from app.models.json_model import json_read_data

def get_trucks_with_cameras():
    trucks = TruckModel.get_all()
    cameras = CameraModel.get_all()
    others = json_read_data()

    truck_dict = {truck.Id: truck for truck in trucks}  # Словарь {id грузовика: объект}

    result_list = []
    for camera in cameras:
        truck = truck_dict.get(camera.TransportId)  # Находим грузовик по transportid
        if truck:
            result_list.append([
                truck.Name,
                truck.StateNumber,
                camera.Front,
                camera.Back,
                camera.Left,
                camera.Right
            ])

    for other in others:
        result_list.append([other["Name"], other["StateNumber"], other["Front"], other["Back"], other["Left"], other["Right"]])

    return result_list
