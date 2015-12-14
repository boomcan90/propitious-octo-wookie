# from gcm import GCM



# def send_gcm_message(message, reg_id):
#     gcm = GCM("AIzaSyAf6J6MHvUlpnT_FIOoCws8Fs8oL7E0oOc")
#     data = {'message': message}
#     gcm.plaintext_request(registration_id=reg_id, data=data)

# send_gcm_message("DISCARD", "c198uVK7Dgw:APA91bEvUwogy4q0Px33WfHpOPvOZe6U7uCML1hd1e7LDuBfoGC7zdErxWvBpld-FczRi8hFc4z5brY-WEIXXsXFiAgTQ9Ligyk_acrMfClitaq9mzyNqgW8RB2r76Tz8FjCZVYJbEhF")


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
#

from transitions import Machine

class Matter(object):
    def __init__(self): self.set_environment()
    def set_environment(self, temp=0, pressure=101.325):
        self.temp = temp
        self.pressure = pressure
    def print_temperature(self): print("Current temperature is %d degrees celsius." % self.temp)
    def print_pressure(self): print("Current pressure is %.2f kPa." % self.pressure)

lump = Matter()
machine = Machine(lump, ['solid', 'liquid'], initial='solid')
machine.add_transition('melt', 'solid', 'liquid', before='set_environment')

lump.melt(45)  # positional arg
lump.print_temperature()
print lump.state
print lump.print_temperature()
machine.set_state('solid')  # reset state so we can melt again
lump.melt(pressure=300.23)  # keyword args also work
lump.print_pressure()
machine.set_state('liquid')
print lump.state
