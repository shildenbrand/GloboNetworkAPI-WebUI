# -*- coding:utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from CadVlan.messages import request_vip_messages, pool_messages

def populate_expectstring_choices(client):
    expectstring_choices = client.create_ambiente().listar_healtchcheck_expect_distinct()
    expectstring_choices['healthcheck_expect'].insert(0, {'expect_string': u'-', 'id': u''})

    return expectstring_choices


def populate_enviroments_choices(client):
    enviroments = client.create_ambiente().list_all()

    # Format enviroments
    enviroments_choices = [('', '-')]
    for obj in enviroments['ambiente']:
        enviroments_choices.append((obj['id'], "%s - %s - %s" % (obj['divisao_dc_name'],
                                                                 obj['ambiente_logico_name'],
                                                                 obj['grupo_l3_name'])))

    return enviroments_choices


def populate_optionsvips_choices(client, tips = 'Balanceamento'):
    optionsvips = client.create_option_vip().get_all()

    # Filter options vip
    optionsvips_choices = [('', '-')]
    for obj in optionsvips['option_vip']:
        if obj['tipo_opcao'] == tips:
            optionsvips_choices.append((obj['nome_opcao_txt'], obj['nome_opcao_txt']))

    return optionsvips_choices


def populate_optionspool_choices(client, environment):
    optionspool_choices = [('', '-')]
    if environment:
        optionspools = client.create_pool().get_opcoes_pool_by_ambiente(environment)
        for obj in optionspools['opcoes_pool']:
            optionspool_choices.append((obj['opcao_pool']['description'], obj['opcao_pool']['description']))

    return optionspool_choices


def populate_pool_members_by_lists(client, ports_reals, ips, id_ips, id_equips, id_pool_member, priorities, weight):
    pool_members = []
    ip_list_full = []
    if len(ports_reals) > 0 and len(ips) > 0:
        for i in range(0, len(ports_reals)):
            nome_equipamento = client.create_equipamento().listar_por_id(id_equips[i])
            pool_members.append({'id': id_pool_member[i],
                                 'id_equip': id_equips[i],
                                 'nome_equipamento': nome_equipamento['equipamento']['nome'],
                                 'priority': priorities[i],
                                 'port_real': ports_reals[i],
                                 'weight': weight[i],
                                 'id_ip': id_ips[i],
                                 'ip': ips[i]
                                 })

            ip_list_full.append({'id': id_ips[i], 'ip': ips[i]})

    return pool_members, ip_list_full


def populate_pool_members_by_obj(client, server_pool_members):
    pool_members = []

    if len(server_pool_members) > 0:
        for obj in server_pool_members:
            equip = client.create_pool().get_equip_by_ip(obj['ip']['id'])

            ip = ''
            if obj['ip']:
                ip = obj['ip']['ip_formated']
            elif obj['ipv6']:
                ip = obj['ipv6']['ip_formated']

            pool_members.append({'id': obj['id'], 'id_equip': equip['equipamento']['id'],
                                 'nome_equipamento': equip['equipamento']['nome'], 'priority': obj['priority'],
                                 'port_real': obj['port_real'], 'weight': obj['weight'], 'id_ip': obj['ip']['id'],
                                 'ip': ip})

    return pool_members