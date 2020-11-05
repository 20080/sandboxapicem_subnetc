import requests
import json
from tabulate import *

requests.packages.urllib3.disable_warnings()


def get_ticket():
    api_url = "https://sandboxapicem.cisco.com/api/v1/ticket"
    headers = {"content-type": "application/json"}
    body_json = {"username": "devnetuser", "password": "Cisco123!"}
    resp = requests.post(api_url, json.dumps(body_json), headers=headers, verify=False)
    response_json = resp.json()
    serviceTicket = response_json["response"]["serviceTicket"]
    return serviceTicket


# this function here shows code reuse
def get_json(url):
    ticket = get_ticket()
    headers = {"content-type": "application/json", "X-Auth-Token": ticket}
    resp = requests.get(url, headers=headers, verify=False)
    if resp.status_code != 200:
        raise Exception("Status code does not equal 200. Response text: " + resp.text)
    else:
        return resp.json()

# to get all connected devices
def get_ConnDevices():
    api_url = "https://sandboxapicem.cisco.com/api/v1/network-device"
    work = "\n*All connected devices list*"
    print(work)
    response_json = get_json(api_url)
    devices = []
    i = 0
    for item in response_json["response"]:
        i += 1
        list = [i, item["serialNumber"], item["family"], item["type"], item["role"], item["macAddress"],
                item["softwareVersion"], item["tagCount"], item["hostname"], item["managementIpAddress"]]
        devices.append(list)

    table_header = ["Number", "Device Family", "Type", "Role", "MAC", "SW ver", "TAG count", "HostName", "Mgmt IP"]
    print(tabulate(devices, table_header))


# Request type to be made in order to extract address pool
def get_add():
    api_url = "https://sandboxapicem.cisco.com/api/v1/ippool/"  # Your Id Here
    response_json = get_json(api_url)
    work = "\n*Address pool*"
    print(work)

    address = []
    i = 0
    for item in response_json["response"]:
        i += 1
        list = [i, item["apicAppName"], item["role"], item["nextAddress"], item["endAddress"],
                item["startAddress"], item["creationOrder"], item["usagePercentage"], item["freeIpCount"],
                item["ipPool"], item["id"]]
        address.append(list)

    table_header = ["Number", "APIC AppName", "Role", "Next Add", "End Add", "Start add", "Creation Order",
                    "Usage %", "FreeIp Count", "Ip Pool", "ID"]
    print(tabulate(address, table_header))


# prints all network device configuration file..
def get_configFile():
    api_url = "https://sandboxapicem.cisco.com/api/v1/file/namespace/config"
    response_json = get_json(api_url)
    work = "\n*Config files of the network*"
    print(work)
    netList = []
    i = 0
    for item in response_json["response"]:
        i += 1
        configF = [i, item["id"], item["name"], item["fileSize"], item["md5Checksum"], item["fileFormat"],
                   item["downloadPath"], item["nameSpace"]]
        netList.append(configF)

    table_header = ["Number", "ID", "File Name", "File Size", "MD5", "File Format", "Download Path", "Name Space"]
    print(tabulate(netList, table_header))


# #get all the connected devices
# def get_ConnectedDevices():


def print_hosts():
    api_url = "https://sandboxapicem.cisco.com/api/v1/host"
    response_json = get_json(api_url)
    work = "\n*All available Hosts*"
    print(work)

    host_list = []
    i = 0
    for item in response_json["response"]:
        i += 1
        host = [i, item["hostType"], item["hostIp"]]
        host_list.append(host)

    table_header = ["Number", "Type", "IP"]
    print(tabulate(host_list, table_header))


def print_devices():
    api_url = "https://sandboxapicem.cisco.com/api/v1/network-device"
    response_json = get_json(api_url)
    work = "\n*Connected devices Available*"
    print(work)
    devices_list = []
    i = 0
    for item in response_json["response"]:
        i += 1
        host = [i, item["hostname"], item["series"], item["serialNumber"]]
        devices_list.append(host)

    table_header = ["Number", "Hostname", "Series", "Serial Number"]
    print(tabulate(devices_list, table_header))


if __name__ == "__main__":
    print_hosts()
    print_devices()
    # Provides the config files list
    get_configFile()
    # ip ADDRESS POOL
    get_add()
    # CONNECTED dEVICES
    get_ConnDevices()
