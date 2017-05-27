# coding=utf-8
from django.db.models import Q
from yuntu.models import Opac, Province, Library, NodeServer, IPSegment
import datetime
import json

with open('static/tem/opac.txt') as f:
    items = []
    for line in f:
        opac = json.loads(line)
        items.append(Opac(**opac))
    Opac.objects.bulk_create(items)

with open('static/tem/provinces.json') as f:
    items = json.load(f)
    for item in items:
        Province.objects.create(**item)

with open('static/tem/libraries.txt') as f:
    items = []
    for line in f:
        param = {}
        library = json.loads(line)
        param['id'] = int(library['id'])
        param['name'] = library['name']
        if len(library['node_ip']) > 0:
            param['mirror_ip'] = library['node_ip']
        param['status'] = {u'停用': 1, u'试用': 2, u'启用': 3, }.get(library['status'])
        province = library['province']
        if len(province) > 0:
            param['province'] = Province.objects.get(name=province)
        if len(library['opac_url']) > 0:
            param['opac_url'] = library['opac_url']
        if len(library['remarks']) > 0:
            param['remarks'] = library['remarks']
        for opac in Opac.objects.all():
            if opac.name + opac.version == library['opac_version']:
                param['opac_version'] = opac
        start_date = library['start_date']
        if len(start_date) > 0:
            param['start_date'] = datetime.date(*[int(i) for i in start_date.split()[0].split('-')])
        else:
            param['start_date'] = datetime.date(2014, 1, 1)
        try:
            items.append(Library(**param))
        except TypeError, e:
            print e
    for i in items:
        try:
            Library.objects.get(id=i.id)
        except:
            i.save()

            # Library.objects.bulk_create(items)

with open('static/tem/node_servers.txt') as f:
    items = []
    for line in f:
        param = {}
        node = json.loads(line)
        param['name'] = node['name']
        deploy_date = node['deploy_date']
        if len(deploy_date) > 0:
            param['deploy_date'] = datetime.date(*[int(i) for i in deploy_date.split()[0].split('-')])
        if len(node['level']) > 0:
            param['level'] = {u'一级中心': 1, u'二级中心': 2, u'加速服务器': 3, }.get(node['level'])
        mirror_ip = node['mirror_ip']
        if len(mirror_ip) > 0:
            param['mirror_ip'] = mirror_ip.strip()
        server_ip = node['server_ip']
        if len(server_ip) > 0:
            param['server_ip'] = server_ip.strip()
        netmask = node['netmask']
        if len(netmask) > 0:
            param['netmask'] = netmask.strip()
        gateway = node['gateway']
        if len(gateway) > 0:
            param['gateway'] = gateway.strip()
        public_ip = node['public_ip']
        if len(public_ip) > 0:
            param['public_ip'] = public_ip.strip()
        dns = node['dns']
        if len(dns) > 0:
            param['dns'] = dns.split(u'，')[0]
        os = node['os']
        if len(os) > 0:
            param['os'] = os.strip()
        if len(node['ownership']) > 0:
            param['ownership'] = {u'校方': 0, u'公司': 1}.get(node['ownership'])
        nic_bond = node['nic_bond']
        if nic_bond == u'是':
            param['nic_bond'] = True
        hardware = node['hardware']
        if len(hardware) > 0:
            param['hardware'] = hardware.strip()
        remarks = node['remarks']
        if len(remarks) > 0:
            param['remarks'] = remarks.strip()
        print param
        n = NodeServer(**param)
        n.save()
        if len(node['library']) > 0:
            n.library.add(Library.objects.get(Q(name=node['library']) | Q(former=node['library'])))
        print n

with open('static/tem/node_servers.txt') as f:
    for line in f:
        node = json.loads(line)
        if len(node['library']) > 0:
            print node['library']
            n = NodeServer.objects.get(name=node['name'])
            n.library = Library.objects.get(Q(name=node['library']) | Q(former=node['library']))
            n.save()

with open('static/tem/libraries.txt') as f:
    for line in f:
        library = json.loads(line)
        if len(library['node_server']) > 0:
            print library['node_server']
            l = Library.objects.get(id=int(library['id']))
            try:
                l.node_server = NodeServer.objects.get(name=library['node_server'])
                l.save()
            except:
                pass

with open('static/tem/libraries.txt') as f:
    for line in f:
        library = json.loads(line)
        if library['client_ip'] is not u'':
            lid = int(library['id'])
            for i in library['client_ip'].split():
                if '---' in i:
                    start = i.split('---')[0]
                    end = '.'.join(start.split('.')[:3]) + '.' + i.split('---')[1]
                    param = (start, end)
                    IPSegment.objects.create(start=start, end=end, library=Library.objects.get(id=lid))
                elif '--' in i:
                    start = i.split('--')[0]
                    end = i.split('--')[1]
                    IPSegment.objects.create(start=start, end=end, library=Library.objects.get(id=lid))
                elif '-' in i:
                    start = i.split('-')[0]
                    end = i.split('-')[1]
                    IPSegment.objects.create(start=start, end=end, library=Library.objects.get(id=lid))
                else:
                    IPSegment.objects.create(start=i, end=i, library=Library.objects.get(id=lid))
