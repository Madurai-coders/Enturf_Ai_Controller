import os
import django
from channels.layers import get_channel_layer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Enturf_Ai_Controller.settings')
django.setup()
from controller.models import Gallery





# new_record = Gallery(videoPath='value1', my_array='value2')
# new_record.save()





async def send_message(room_group_name, message):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        room_group_name,
        {
            'type': 'AIControllerBroadCaste',
            'message': message
        }
    )

def update_database(path, message):
    # Check if a record with the given path exists
    existing_record = Gallery.objects.filter(videoPath=path).first()

    if existing_record:
        # If the record exists, update it by appending the new message
        updated_message = existing_record.my_array + ',' + message
        existing_record.my_array = updated_message
        existing_record.save()
    else:
        # If the record does not exist, create a new one
        new_record = Gallery(videoPath=path, my_array=message)
        new_record.save()