#!/usr/bin/env python3

import random, socket, subprocess, os, time, json
from datetime import datetime
import argparse

type_efu = 1


class ECDCServers:
    def __init__(self, filename):
        self.servers = []
        self.add_csv(filename)


    def getstatus(self, idx):
        return self.servers[idx][2]


    def setstatus(self, idx, flag):
        self.servers[idx][2] = self.servers[idx][2] | flag


    def clearstatus(self, idx, flag):
        self.servers[idx][2] = self.servers[idx][2] & ~flag


    def add_csv(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        for line in lines:
            line = line.replace(" ", "")
            line = line.replace("\n", "")
            if line[0] != "#" and line != "":
                name, type, status, ip, port, angle, xoff, yoff = line.split(',')
                type = int(type)
                status = int(status)
                port = int(port)
                angle = int(angle)
                xoff = int(xoff)
                yoff = int(yoff)
                server = [name, type, status, ip, port, angle, xoff, yoff]
                self.servers.append(server)
        file.close()



class Monitor:
    def __init__(self, serverlist, debug, refresh):
        self.s_ping =  0x80
        self.s_offline = 0x40
        self.s_service = 0x08
        self.s_stage3 = 0x04
        self.s_stage2 = 0x02
        self.s_stage1 = 0x01
        self.lab = serverlist
        self.debug = debug
        self.refresh = refresh
        self.starttime = self.gettime()


    def mprint(self, arg):
        self.file.write(arg + '\n')


    def dprint(self, arg):
        if self.debug:
            print(arg)


    def gettime(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")


    def is_offline(self, status):
        return status & self.s_offline


    def can_ping(self, status):
        return status & self.s_ping


    def has_service(self, status):
        return status & self.s_service


    # def check_ping_parallel(self, idx, ipaddr):
    #     num_threads = 2 * multiprocessing.cpu_count()
    #     p = multiprocessing.dummy.Pool(num_threads)
    #     p.map(ping, ["172.30.242.{}".format(x) for x in range(start,end)])

    # Check that server can be reached (ping)
    def check_ping(self, ipaddr):
        res = subprocess.Popen(["ping", "-c1", "-W1", ipaddr], stdout=subprocess.PIPE).stdout.read()
        if res.find(b"1 packets transmitted, 1 ") != -1:
            return True
        else:
            self.dprint("ping failed for {}".format(ipaddr))
            return False


    def check_efu_pipeline(self, ipaddr, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ipaddr, port))
            s.send(b"RUNTIMESTATS")
            data = s.recv(256)
            s.close()

            if (data.find(b"BADCMD") != -1):
                self.dprint(data)
                return 7
            data = int(data.split()[1])
            return data
        except:
            self.dprint("connection reset (by peer?)")
            return 0;


    # Check that service is running (accept tcp connection)
    def check_service(self, idx, type, ipaddr, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if sock.connect_ex((ipaddr, port)) == 0:
            self.lab.setstatus(idx, self.s_service) #
            if type == type_efu:
                status = self.check_efu_pipeline(ipaddr, port)
                if status == 0:
                    self.lab.clearstatus(idx, self.s_stage1 | self.s_stage2 | self.s_stage3)
                else:
                    self.lab.setstatus(idx, status)
            else:
                self.lab.setstatus(idx, self.s_stage1 | self.s_stage2 | self.s_stage3)
        else:
            self.lab.clearstatus(idx, self.s_service)
            self.dprint("no service for {}:{}".format(ipaddr, port))





    def getstatus(self):
        for idx, res  in enumerate(self.lab.servers):
            name, type, status, ip, port, ang, xo, yo = res
            if not self.is_offline(status):
                if self.check_ping(ip):
                    self.lab.setstatus(idx, self.s_ping)
                    self.check_service(idx, type, ip, port)
                else:
                    self.lab.clearstatus(idx, self.s_ping)


    def printbox(self, x, y, a, state, width=20):
        res = '<rect width="{}" height="10" '.format(width)
        res = res + 'x="{}" y="{}" transform="rotate({} 400 200)" '.format(x,y,a)
        res = res + 'fill="{}"'.format(state)
        res = res + '/>'
        self.mprint(res)


    def stagestatetocolor(self, stage, state):
        if state & stage:
            return 'green'
        else:
            return 'red'


    def statetocolor(self, stage, state):
        if self.is_offline(state):
            return '#C0C0C0'
        if not self.can_ping(state):
            return 'orange'
        if not self.has_service(state):
            return 'blue'
        if stage == 1:
            return self.stagestatetocolor(stage, state)
        elif stage == 2:
            return self.stagestatetocolor(stage, state)
        elif stage == 4:
            return self.stagestatetocolor(stage, state)
        else:
            return 'green'

    # Coordinates are a mess - center is (400, 200)
    def printinst(self, name, type, state, angle, ofsx, ofsy):
        boxy = 195 + ofsy
        texty = boxy + 8
        textx = 450 + ofsx
        common = '<text  class="names" y="{}" font-size="8px"  transform="rotate({} 400 200)"'.format(texty, angle)
        if type == type_efu:
            self.printbox(500 + ofsx, boxy, angle, self.statetocolor(1, state))
            self.printbox(522 + ofsx, boxy, angle, self.statetocolor(2, state))
            self.printbox(544 + ofsx, boxy, angle, self.statetocolor(4, state))
            self.mprint('{} x="450">{}</text>'.format(common, name))
        else:
            self.printbox(500 + ofsx, boxy, angle, self.statetocolor(1, state), 35)
            self.mprint('{} x="{}">{}</text>'.format(common, textx, name))
        self.mprint('')


    def makelegend(self):
        common = '<text class="names" x="630" font-size="8px"'
        self.printbox(600, 50, 0, '#c0c0c0')
        self.mprint('{}  y="57"  >Uncommissioned</text>'.format(common))
        self.printbox(600, 65, 0, 'orange')
        self.mprint('{}   y="72" >No NW connectivity</text>'.format(common))
        self.printbox(600, 80, 0, 'blue')
        self.mprint('{}   y="87" >Service not running</text>'.format(common))
        self.printbox(600, 95, 0, 'green')
        self.mprint('{}   y="102" >Service running</text>'.format(common))
        self.printbox(600, 110, 0, 'red')
        self.mprint('{}   y="117" >Service error</text>'.format(common))


    def generatesvg(self):
        datestr = self.gettime()
        self.mprint('<html>')
        self.mprint('<head><meta http-equiv="refresh" content="2"></head>')
        self.mprint('<body>')
        self.mprint('<svg viewBox="-20 -20 800 600" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">')

        for name, type, status, ip, port, angle, xo, yo in self.lab.servers:
            self.dprint("{} {} {} {}".format(name, type, status, ip))
            self.printinst(name, type, status, angle, xo, yo)

        self.mprint('<text x="50" y="45">Kafka brokers</text>')
        self.mprint('<text x="50" y="165">Other services</text>')

        self.makelegend()

        self.mprint('<rect y="-20" width="800" height="40" fill="#0094CA"/>')
        self.mprint('<rect y="380" width="800" height="5" fill="#0094CA"/>')
        #self.mprint('<path d="M400,210 L545,115 A 168,168 45 0,0 240,150 L400,205" stroke="black" fill="transparent"/>')
        #self.mprint('<path d="M400,190 L560,255 A 170,170 45 0,1 257,287 L354,220" stroke="black" fill="transparent"/>')
        self.mprint('<line x1="450" y1="200" x2="700" y2="200" style="stroke:rgb(0,0,0);stroke-width:2" />')
        self.mprint('<circle cx="400" cy="200" r="48" stroke-width="1" fill="white" />')
        self.mprint('<circle cx="400" cy="200" r="45" stroke-width="1" fill="#0094CA" />')
        self.mprint('<text x="385" y="205" fill="white">ESS</text>')
        self.mprint('<text x="350" y="12" fill="white" font-size="36px">YMIR</text>')
        self.mprint('<text x="10" y="5" fill="white" font-size="16px">{}</text>'.format(datestr))
        self.mprint('<text x="690" y="395" fill="black" font-size="8px">started {}</text>'.format(self.starttime))
        repo = "https://github.com/ess-dmsc/integration-test/tree/master/ikondemo"
        self.mprint('<text x="0" y="395" fill="black" font-size="8px">{}</text>'.format(repo))
        self.mprint('</svg></body></html>')


    def one_pass(self):
        self.file = open("tmp.svg", "w")
        self.getstatus()
        self.generatesvg()
        self.file.close()
        os.rename("tmp.svg", "index.html")

    def run(self):
        while (True):
            start = time.time()
            self.one_pass()
            dt = time.time() - start
            if (self.refresh - dt) > 0:
                time.sleep(self.refresh - dt)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-f', '--file', type = str, default = 'utgaard.csv')
    parser.add_argument('-r', '--refresh', type = int, default = 5)
    args = parser.parse_args()

    serverlist = ECDCServers(args.file)
    mon = Monitor(serverlist, args.debug, args.refresh)

    print("Dashboard generator is running ...")
    mon.run()

if __name__ == "__main__":
    main()
