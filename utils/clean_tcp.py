import numpy as np
from utils.sgt import get_enc


def temp_wscale(wscale):
  if wscale=="":
    return -1
  temp=wscale.split(':')
  return int(temp[2],16)

def get_options_arr(olayout: str):
  TCPOptions=[]
  if olayout is None or olayout=="":
    return TCPOptions

  hex_list=olayout.split(':')
  i=0
  while i < len(hex_list):
    kind=int(hex_list[i],16)
    if kind == 0:
      TCPOptions.append("eol")
      while i < (len(hex_list)-1) and hex_list[i+1]=='01':
        TCPOptions.append("nop")
        i+=1
      break  # End of options

    elif kind == 1:
      TCPOptions.append("nop")
      i += 1  # Skip NOP, which has no length

    elif kind == 2:
      TCPOptions.append("mss")
      i += 4  # Skip MSS (2 bytes Kind + 2 bytes Length)

    elif kind == 3:
      TCPOptions.append("ws")
      i += 3  # Skip WSCALE (2 bytes Kind + 1 byte Length)

    elif kind == 4:
      TCPOptions.append("sok")
      i += 2  # Skip SOK, which has no length

    elif kind == 8:
      TCPOptions.append("ts")
      i += 10  # Skip TS (2 bytes Kind + 8 bytes Length)

    else:
      TCPOptions.append(f"?{kind}")
      length = int(hex_list[i + 1], 16)
      i += length + 1

  return TCPOptions

def clean_tcp(tcp_info):
  if tcp_info['t_mss'] is None:
    tcp_info['t_mss']=-1

  if tcp_info['t_wscale'] is None:
    tcp_info['t_wscale']=''
  
  tcp_info['t_wscale']=temp_wscale(tcp_info['t_wscale'])

  t_options_arr=get_options_arr(tcp_info['t_options_hex'])

  options_arr=get_enc(t_options_arr)

  tcp_info['ip_dsfield']=int(tcp_info['ip_dsfield'],16)

  temp_arr=np.array([tcp_info['ip_ttl'],tcp_info['ip_totlen'],tcp_info['t_mss'],tcp_info['t_wsize'], tcp_info['t_wscale'],tcp_info['ip_flags_df'],tcp_info['ip_dsfield']])
  temp_arr2=np.array(options_arr).flatten()
  
  return np.concatenate((temp_arr, temp_arr2))