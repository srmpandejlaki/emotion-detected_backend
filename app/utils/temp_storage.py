# Penyimpanan sementara mirip cache
temp_data = []

def get_temp_data():
    return temp_data

def add_temp_data(item: dict):
    temp_data.append(item)

def clear_temp_data():
    temp_data.clear()
