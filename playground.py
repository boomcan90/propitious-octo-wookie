from gcm import GCM



def send_gcm_message(message, reg_id):
    gcm = GCM("AIzaSyAf6J6MHvUlpnT_FIOoCws8Fs8oL7E0oOc")
    data = {'message': message}
    gcm.plaintext_request(registration_id=reg_id, data=data)

send_gcm_message("DRAW", "c198uVK7Dgw:APA91bEvUwogy4q0Px33WfHpOPvOZe6U7uCML1hd1e7LDuBfoGC7zdErxWvBpld-FczRi8hFc4z5brY-WEIXXsXFiAgTQ9Ligyk_acrMfClitaq9mzyNqgW8RB2r76Tz8FjCZVYJbEhF")


# # Plaintext request
# reg_id = '12'
# gcm.plaintext_request(registration_id=reg_id, data=data)

# # JSON request
# reg_ids = ['12', '34', '69']
# response = gcm.json_request(registration_ids=reg_ids, data=data)

# # Extra arguments
# res = gcm.json_request(
#     registration_ids=reg_ids, data=data,
#     collapse_key='uptoyou', delay_while_idle=True, time_to_live=3600
# )

# # Topic Messaging
# topic = 'foo'
# gcm.send_topic_message(topic=topic, data=data)