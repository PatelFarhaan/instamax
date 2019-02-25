# class ServiceGraphRelationship():
#
#     def __init__(self,templatename,cname, serviceGraph_name,external_bd,internal_bd,sg_node_id=1):
#         self.templatename = templatename
#         self.cname = cname
#         self.serviceGraph_name = serviceGraph_name
#         self.external_bd = external_bd
#         self.internal_bd = internal_bd
#         self.sg_node_id = sg_node_id
#         self.serviceNodeRelationship = []
#         self.serviceNodeRelationship.append({})
#         self.serviceNodeRelationship[0]['serviceNodeRef'] = "".format(templatename)
#         self.serviceNodeRelationship[0]['providerConnector'] = {}
#         self.serviceNodeRelationship[0]['providerConnector']['connectorType'] = ''.format(self.cname)
#         self.serviceNodeRelationship[0]['providerConnector']['bdRef'] = ''.format(self.serviceGraph_name)
#         self.serviceNodeRelationship[0]['consumerConnector'] = {}
#         self.serviceNodeRelationship[0]['consumerConnector']['connectorType'] = ''.format(self.external_bd)
#         self.serviceNodeRelationship[0]['consumerConnector']['bdref'] = ''.format(self.internal_bd)
#
#     def get_services(self):
#         return self.serviceNodeRelationship
#
#     def serviceNodeRelationships(self):
#         snr_dict = self.serviceNodeRelationship
#         snr_dict[0]['serviceNodeRef'] = '/templates/{}/serviceGraphs/{}/serviceNodes/{}'.format(self.templatename,self.serviceGraph_name, 'node'+str(self.sg_node_id))
#         snr_dict[0]['providerConnector'] = {}
#         snr_dict[0]['providerConnector']['connectorType'] = 'general'
#         snr_dict[0]['providerConnector']['bdRef'] = '/templates/{}/bds/{}"'.format(self.templatename, self.internal_bd)
#         snr_dict[0]['consumerConnector'] = {}
#         snr_dict[0]['consumerConnector']['connectorType'] = 'general'
#         snr_dict[0]['consumerConnector']['bdref'] = '/templates/{}/bds/{}'.format(self.templatename, self.external_bd)
#         return snr_dict
#
#
# class Contract():
#
#     def print(self):
#         sg_obj = ServiceGraphRelationship('asdsd',2,3,4,5,6)
#         ans = sg_obj.serviceNodeRelationships()
#         return ans
#
#
# obj = Contract()
# ans = obj.print()
# print(ans)

class serviceNode():
    def __init__(self):
        self.service_graph_list = []
        self.service_graph_list.append({})
        self.service_graph_list[0]['name'] = ''
        self.service_graph_list[0]['serviceNodeRef'] = ''
        self.service_graph_list[0]['serviceNodeTypeId'] = ''
        self.service_graph_list[0]['index'] = ''

    def get_list(self):
        return self.service_graph_list


class serviceGraphs():

    def __init__(self,name,templatename,servicegraph_Name,sh_node_count=1):
        self.templatename = templatename
        self.name = name
        self.displayName = name
        self.service_graph_list = []
        self.service_graph_list.append({})
        self.service_graph_list[0]['name'] = ''
        self.service_graph_list[0]['displayName'] = ''
        self.service_graph_list[0]['serviceGraphRef'] = ''
        self.service_graph_list[0]['description'] = ''


    def get_service_graph(self):
        return self.service_graph_list

    def get_service_graph_dict(self):
        new_dict = self.service_graph_list
        new_dict[0]['name'] = '{}'.format(self.name)
        new_dict[0]['displayName'] = self.displayName
        new_dict[0]['serviceGraphRef'] = '/templates/{}/serviceGraphs/{}'.format(self.templatename, self.name)
        new_dict[0]['description'] = ''
        objs = serviceNode()
        ans = objs.get_list()
        self.service_graph_list[0]['serviceNodes'] = ans
        return new_dict


obj = serviceGraphs('first', 'second', 'third')
ans = obj.get_service_graph_dict()
print(ans)