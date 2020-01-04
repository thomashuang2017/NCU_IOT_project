import os


def ping_host():
    hostname = "118.161.173.98" #example
    response = os.system("ping -c 1 " + hostname)

    #and then check the response...
    if response == 0:
      print(hostname, 'is up!')
    else:
      print(hostname, 'is down!')
      
    return response
