from wakeonlan import send_magic_packet
import subprocess as sp
import datetime
import smtplib

time = str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

servers = {'local-print': ['192.168.1.210', '00:22:19:c8:0e:d7'],
           'print-backup': ['192.168.1.211', '00:22:19:ae:a1:29'],
           'kvm1': ['192.168.1.5', '00:22:19:A0:0D:96'],
           'broadcast-0': ['192.168.1.14', '3c:d9:2b:07:93:16'],
           'broadcast-1': ['192.168.1.15', 'd4:85:64:78:51:28'],
           'novocr1': ['192.168.1.16', '30:9c:23:60:d7:0b'],
           'novocr2': ['192.168.1.17', '30:9c:23:60:d7:36'],
           'novstt1': ['192.168.1.18', '30:9c:23:60:d7:10'],
           'synology-2': ['192.168.1.91', '00:11:32:79:3D:8D'],
           #'novclus1-node1': ['192.168.1.11', '00:22:19:B7:79:0F']
          }


def send_mail(svr):
    log_file = open('/var/log/wake-on-lan.log', 'r')
    log_msg = log_file.read()
    mail_srv = 'mail.novusgroup.co.za'
    mail_port = '25'
    mail_name = 'itmonitor@novusgroup.co.za'
    mail_recip = ['itmonitor@novusgroup.co.za']
    mail_sub = 'Wake-on-lan sent to {}'.format(svr)
    mail_msg = 'Subject: {}\n\n{}'.format(mail_sub, log_msg)
    smtpServ = smtplib.SMTP(mail_srv, mail_port)
    smtpServ.sendmail(mail_name, mail_recip, mail_msg)
    log_file.close()
    smtpServ.quit()
    print('Sending email notification to: %s' % mail_recip)



def wake_up(svr, mac):
    print(time, 'sending wake-on-lan request to ' + svr, mac)
     
    send_magic_packet(mac)
    send_mail(svr)



for server in servers.values():
    ping = 'ping -c1 ' + server[0]
    res = sp.Popen(ping, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    output,error = res.communicate()
    output = output.decode('ascii')
    error = error.decode('ascii')

    if '1 received' in output:
        print(time, server[0], 'is online')
    elif '0 received' in output:
        print(time, server[0], 'is offline')
        wake_up(server[0], server[1])
    elif error:
        print(time, 'ERROR: ' + error)



print()
print('-' * 40)
print()
