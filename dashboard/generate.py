#!/usr/bin/env python3

import htmlsvg
import random, socket, subprocess, os, time, json
from datetime import datetime
import argparse

type_efu = 1
type_text = 4

col1='#c0c0c0'
col2='red'
col3='orange'
col4='#444400'
col5='green'


class ECDCServers:
    def __init__(self, filename, directory):
        self.servers = []
        self.directory = directory
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
            if line != "" and line[0] != "#":
                name, type, status, ip, port, angle, xoff, yoff, grafana = line.split(',')
                type = int(type)
                status = int(status)
                port = int(port)
                angle = int(angle)
                xoff = int(xoff)
                yoff = int(yoff)
                server = [name, type, status, ip, port, angle, xoff, yoff, grafana, ""]
                self.servers.append(server)
        file.close()


class Monitor:
    def __init__(self, serverlist, args):
        self.s_ping    = 0x80
        self.s_offline = 0x40
        self.s_service = 0x08
        self.s_stage3  = 0x04
        self.s_stage2  = 0x02
        self.s_stage1  = 0x01
        self.lab = serverlist
        self.debug = args.debug
        self.refresh = args.refresh
        self.test = args.test
        self.directory = args.out
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
        if self.test:
            return True
        res = subprocess.Popen(["ping", "-c1", "-W1", ipaddr], stdout=subprocess.PIPE).stdout.read()
        if res.find(b"1 packets transmitted, 1 ") != -1:
            return True
        else:
            self.dprint("ping failed for {}".format(ipaddr))
            return False


    def efu_get_version(self, ipaddr, port):
        if self.test:
            return "test data"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ipaddr, port))
            s.send(b"VERSION_GET")
            data = s.recv(256)
            s.close()

            #return " ".join(data.split()[1:4])
            test = "<br>".join(data.decode("utf-8").split()[1:4])
            self.dprint(test)
            return test
        except:
            self.dprint("connection reset (by peer?)")
            return "connection reset (by peer?)";


    def check_efu_pipeline(self, ipaddr, port):
        if self.test:
            return 5
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
        if self.test:
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        if sock.connect_ex((ipaddr, port)) == 0:
            self.lab.setstatus(idx, self.s_service) #
            if type == type_efu:
                status = self.check_efu_pipeline(ipaddr, port)
                if status == 0:
                    self.lab.clearstatus(idx, self.s_stage1 | self.s_stage2 | self.s_stage3)
                else:
                    self.lab.setstatus(idx, status)
                self.lab.servers[idx][9] = self.efu_get_version(ipaddr, port)

            else:
                self.lab.setstatus(idx, self.s_stage1 | self.s_stage2 | self.s_stage3)
        else:
            self.lab.clearstatus(idx, self.s_service)
            self.dprint("no service for {}:{}".format(ipaddr, port))


    def getstatus(self):
        for idx, res  in enumerate(self.lab.servers):
            name, type, status, ip, port, ang, xo, yo, grafana, sw = res
            if not self.is_offline(status):
                if self.check_ping(ip):
                    self.lab.setstatus(idx, self.s_ping)
                    self.check_service(idx, type, ip, port)
                else:
                    self.lab.clearstatus(idx, self.s_ping)


    def printbox(self, x, y, a, color, efu, motext='', width=25):
        if efu:
            res = '<use href="#chevron" width="{}" height="10" '.format(width)
        else:
            res = '<rect width="{}" height="10" '.format(width)
        res = res + 'x="{}" y="{}" transform="rotate({} 400 200)" '.format(x,y,a)
        if motext != '' and color != col1:
          res = res + 'onmousemove="showTooltip(evt, \'{}\');" onmouseout="hideTooltip();" '.format(motext)

        if color == col4:
            res = res + 'fill="url(#dhatch)"'
        elif color == 'none':
            res = res + 'fill="none" stroke="black"'
        else:
            res = res + 'fill="{}"'.format(color)
        res = res + '/>'
        self.mprint(res)


    def stagestatetocolor(self, stage, state):
        if state & stage:
            return col5
        else:
            return col4


    def statetocolor(self, stage, state):
        if self.is_offline(state):
            return col1
        if not self.can_ping(state):
            return col2
        if not self.has_service(state):
            return col3
        if stage == 1:
            return self.stagestatetocolor(stage, state)
        elif stage == 2:
            return self.stagestatetocolor(stage, state)
        elif stage == 4:
            return self.stagestatetocolor(stage, state)
        else:
            return col5

    # TODO Coordinates are a mess - center is (400, 200)
    def printinst(self, name, mouseovertext, type, state, angle, ofsx, ofsy):
        boxy = 195 + ofsy
        texty = boxy + 8
        textx = 450 + ofsx
        common = '<text  class="names" y="{}" transform="rotate({} 400 200)"'.format(texty, angle)
        if type == type_efu:
            self.printbox(506 + ofsx, boxy, angle, self.statetocolor(1, state), 1, mouseovertext)
            self.printbox(528 + ofsx, boxy, angle, self.statetocolor(2, state), 1, mouseovertext)
            self.printbox(550 + ofsx, boxy, angle, self.statetocolor(4, state), 1, mouseovertext)
            self.mprint('{} font-size="8px" x="450">{}</text>'.format(common, name))
        elif type == type_text:
            self.mprint('{} font-size="12px" x="{}">{}</text>'.format(common, textx, name))
        else:
            self.printbox(505 + ofsx, boxy, angle, self.statetocolor(1, state), 0, mouseovertext, 35)
            self.mprint('{} font-size="8px" x="{}">{}</text>'.format(common, textx, name))
        self.mprint('')


    def makelegend(self):
        common = '<text class="names" x="630" font-size="8px"'
        self.printbox(600, 50, 0, col1, 0)
        self.mprint('{}  y="57"  >uncommissioned</text>'.format(common))
        self.printbox(600, 65, 0, col2, 0)
        self.mprint('{}   y="72" >no nw connectivity</text>'.format(common))
        self.printbox(600, 80, 0, col3, 0)
        self.mprint('{}   y="87" >server running</text>'.format(common))
        self.printbox(600, 95, 0, col5, 0)
        self.mprint('{}   y="102" >service running</text>'.format(common))
        self.printbox(600, 110, 0, col4, 0)
        self.mprint('{}   y="117" >service running (no data)</text>'.format(common))
        self.printbox(600, 125, 0, 'none', 1, 60)
        self.mprint('{}   y="132" >data flow</text>'.format(common))


    def generatesvg(self):
        self.mprint(htmlsvg.header)
        name = os.path.basename(os.path.normpath(self.directory))
        self.mprint(f'<text x="350" y="12" fill="white" font-size="36px">{name.upper()}</text>')
        self.mprint(f'<image x="0" y="300" height="100" width="100" href="{name}/logo.jpeg" />')

        for name, type, status, ip, port, angle, xo, yo, url, sw in self.lab.servers:
            self.dprint("{} {} {} {}".format(name, type, status, ip))
            if (url != "none"):
                self.mprint('<a href="{}" target="_blank">'.format(url))
            mouseovertext = '{}:{}<br>{}'.format(ip, port, sw)
            self.printinst(name, mouseovertext, type, status, angle, xo, yo)
            if (url != "none"):
                self.mprint('</a>')

        self.makelegend()
        self.mprint('<text x="10" y="5" fill="white" font-size="16px">{}</text>'.format(self.gettime()))
        self.mprint('<text x="690" y="395" fill="black" font-size="8px">started {}</text>'.format(self.starttime))

        self.mprint(htmlsvg.footer)

    def generaterefreshcomponent(self):
        # Use javascript to refresh the page every dynamically
        # This reserves the url path and query string
        self.mprint(f'''
        <script type="text/javascript">
            setInterval(function() {{
                const isChecked = document.getElementById('auto-refresh-check').checked;
                if (isChecked) {{
                    window.location.href = window.location.href;
                }}
            }}, {self.refresh * 1000});
        </script>
            <div style="text-align:right">
                <input type="checkbox" id="auto-refresh-check" checked/ > 
                <label for="auto-refresh-check">Auto-refresh</label>
            </div>
        ''')

    def one_pass(self):
        self.file = open(f"{self.directory}/tmp.svg", "w")
        self.getstatus()
        self.generatesvg()
        self.generaterefreshcomponent()
        self.file.close()
        os.rename(f"{self.directory}/tmp.svg", f"{self.directory}/index.html")

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
    parser.add_argument('-f', '--file', type = str, default = './config/utgaard.csv')
    parser.add_argument('-r', '--refresh', type = int, default = 5)
    parser.add_argument('-t', '--test', action='store_true')
    parser.add_argument('-o', '--out', type = str, default = '.')
    args = parser.parse_args()

    serverlist = ECDCServers(args.file, args.out)
    mon = Monitor(serverlist, args)

    print("Dashboard generator is running ...")
    mon.run()

if __name__ == "__main__":
    main()
