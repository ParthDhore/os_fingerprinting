import re
def get_os(agent):
  os_names = [
        "Android", "iPhone OS", "Windows", "Mac OS", "Linux", "FreeBSD", "OpenBSD",
        "Solaris", "OpenVMS", "NeXTSTEP", "Tru64", "NMap",
        "Blackberry", "Nintendo"
  ]
  os_name=None
  flavor=None
  if agent is None or agent=="":
    return {'os_name': os_name, 'flavor': flavor}
    
  for os in os_names:
      match = re.search(rf'{os}[^;xrl())/]*', agent)
      if match:
          os = match.group(0)
          os_name=os.split(" ")[0]
          if os_name=='Mac':
            os_name='Mac OS'
            flavor=' '.join(os.split(" ")[2:])
            break
          if os_name=='iPhone':
            os_name='iPhone OS'
            flavor=' '.join(os.split(" ")[2:])
            break
          flavor=' '.join(os.split(" ")[1:])
          break

  if os_name is None and flavor is None:
     return None
  elif flavor is None:
     return os_name
  else:
     return os_name+" "+flavor