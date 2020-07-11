import os
import re
import subprocess
import time
from influxdb import InfluxDBClient

def send_influxdb(network_data):
  client = InfluxDBClient('influxdb', 8086, 'admin', 'admin', 'network_monitoring')

  data = [{
    "measurement": "speed",
    "fields": network_data
  }]
  client.write_points(data)


def get_network_info():
  print("Collectin speed test")
  response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
  print(response)
  ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
  download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
  upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

  ping = ping[0].replace(',', '.')
  download = download[0].replace(',', '.')
  upload = upload[0].replace(',', '.')

  speed_data = {
            "download": float(download),
            "upload": float(upload),
            "ping": float(ping)
  }



  try:
      f = open('tmp/speedtest.csv', 'a+')
      if os.stat('tmp/speedtest.csv').st_size == 0:
              f.write('Date,Time,Ping (ms),Download (Mbit/s),Upload (Mbit/s)\r\n')
      f.write('{},{},{},{},{}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, download, upload))

  except:
      print("fail save csv")

  send_influxdb(speed_data)


get_network_info()
