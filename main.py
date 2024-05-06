import numpy as np
import pandas as pd
import pyshark
from tqdm import tqdm
import time

from utils.clean_tcp import clean_tcp
from utils.mysql import insert_packet_data
from utils.os_rf import tcp_os
from utils.useragent import get_os

import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")

cap = pyshark.FileCapture('..\Data\ext01.pcap')
packets = (pkt for pkt in cap if 'TCP' in pkt)
cache={'ip': None, 'tcp_info': None}
tescnt=0

for pkt in packets:
    ip_layer=pkt['IP']
    tcp_layer=pkt['TCP'] 
    ip=ip_layer._all_fields
    tcp=tcp_layer._all_fields
    
    temp={}
    temp['t_flag']=tcp['tcp.flags']
    if (temp['t_flag']!='0x0002') & (temp['t_flag']!='0x0018'):
        continue

    if 'HTTP' in pkt:
        http_layer=pkt['HTTP']
        if hasattr(http_layer, 'user_agent'):
            temp['h_useragent']=http_layer.user_agent
        else:
            temp['h_useragent']=None
    
    else:
        temp['h_useragent']=None

    temp['ip_src']=ip['ip.addr']
    temp['ip_ver']=float(ip['ip.version'])
    temp['ip_ttl']=float(ip['ip.ttl'])
    temp['ip_totlen']=float(ip['ip.len'])

    if 'tcp.options.mss_val' in tcp:
        temp['t_mss']=float(tcp['tcp.options.mss_val'])
    else:
        temp['t_mss']=None

    temp['t_wsize']=float(tcp['tcp.window_size'])

    if 'tcp.options.wscale' in tcp:
        temp['t_wscale']=tcp['tcp.options.wscale']
    else:
        temp['t_wscale']=None

    if 'tcp.options' not in tcp:
        continue
        
    temp['t_options_hex']=str(tcp['tcp.options'])
    temp['ip_flags_df']=float(bool(ip['ip.flags.df']))
    temp['ip_dsfield']=ip['ip.dsfield']
    
    if temp['t_flag']=='0x0002':
        tcp_info=clean_tcp(temp)
        cache['ip']=temp['ip_src']
        cache['tcp_info']=tcp_info
        inp=tcp_info.reshape(1,-1)
        # a=time.time() 
        os=tcp_os(inp)
        # b=time.time()
        print(f"ip: {temp['ip_src']}, os: {os[0]}")
        # print(b-a)
    
    else:
        os_label=get_os(str(temp['h_useragent']))
        if (cache['ip'] is None) | (cache['ip']!=temp['ip_src']) | (temp['h_useragent'] is None) | (temp['h_useragent']=='') | (os_label is None):
            continue
        insert_packet_data(cache['tcp_info'],os_label)
        tescnt+=1
        if tescnt==300:
            break
        
