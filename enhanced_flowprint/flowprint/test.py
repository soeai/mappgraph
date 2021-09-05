from flow_generator import FlowGenerator
# import pandas as pd

flow_generator = FlowGenerator()





# for k in flows.keys():
#     print('{}: {}'.format(k, flows[k]))

# import os

# li = []
# for f in os.listdir('data'):
#     app = os.path.join('data', f)
#     for filename in os.listdir(app):
#       path = os.path.join(app, filename)
#       li.append(path)

# print(li)  



####################
# from reader import Reader
# reader_obj = Reader()



# packets = reader_obj.read_tshark('zingmp3.pcap')

# print(packets)
# print(packets.shape)
# print(packets[3])
####################

####################
from reader import Reader
reader_obj = Reader()



# packets = reader_obj.read_csv('zingmp3.csv')
packets = reader_obj.read('zingmp3.pcap')

# print(packets)
# print(packets.shape)
# print(packets[3])
####################

flows = flow_generator.combine(packets)
# print(flows)
print(len(flows))