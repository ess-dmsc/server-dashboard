#!/usr/bin/env python3
import argparse
from datetime import datetime
import json
import logging
import html
import os
import socket
import subprocess
import time
import htmlsvg
import sys
from enum import Enum

type_efu = 1
type_fw = 5
type_text = 4

col1 = "#c0c0c0"
col2 = "red"
col3 = "orange"
col4 = "#444400"
col5 = "green"

# Setting up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

class Status(Enum):
    INVALID = -1
    SERVER_RUNNING = 0
    SERVICE_RUNNING = 1
    TEST = 5
    BAD_COMMAND = 7

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
                name, type, status, ip, port, angle, xoff, yoff, grafana = line.split(
                    ","
                )
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
        self.s_ping = 0x80
        self.s_offline = 0x40
        self.s_service = 0x08
        self.s_stage3 = 0x04
        self.s_stage2 = 0x02
        self.s_stage1 = 0x01
        self.lab = serverlist
        self.buffer = ""
        self.debug = args.debug
        self.refresh = args.refresh
        self.test = args.test
        self.directory = args.out
        self.starttime = self.gettime()

        if self.debug:
            logger.setLevel(logging.DEBUG)

    def mprint(self, arg):
        self.buffer += arg + "\n"

    def sync_write_fs(self, filename, content):
        with open(f"{self.directory}/.tmp_file", "w") as file:
            file.write(content)
            file.flush()
            os.fsync(file.fileno())
        os.replace(f"{self.directory}/.tmp_file", f"{self.directory}/{filename}")

    def flush(self):
        self.sync_write_fs("dashboard.svg", self.buffer)
        self.buffer = ""

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
        res = subprocess.Popen(
            ["ping", "-c1", "-W1", ipaddr], stdout=subprocess.PIPE
        ).stdout.read()
        if res.find(b"1 packets transmitted, 1 ") != -1:
            return True
        else:
            logger.error(f"ping failed for {ipaddr}")
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

            # return " ".join(data.split()[1:4])
            test = "&#60;br /&#62;".join(data.decode("utf-8").split()[1:4])
            logger.debug(test)
            return test
        except Exception as e:
            logger.error(f"connection reset (by peer?): {e}")
            return "connection reset (by peer?)"

   
    def check_fw_pipeline(self, ipaddr, port):
        if self.test:
            return Status.TEST
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3.0)
            s.connect((ipaddr, port))
            s.settimeout(20.0)
            s.shutdown(socket.SHUT_WR)
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
            parsed_json = json.loads(data.decode("utf-8", errors="ignore").strip())
            for entry in parsed_json:
                for key, value in entry.items():
                    if key.endswith(".worker_state"):
                        return Status(int(value))
            return Status.SERVER_RUNNING
        except ValueError as e:
            logger.exception(f"Failed to load JSON response from Filewriter {ipaddr}:{port}")
            return Status.SERVER_RUNNING
        except OSError as e:
            logger.exception(f"Failed to read from Filewriter socket {ipaddr}:{port}")
            return Status.SERVER_RUNNING

    def check_efu_pipeline(self, ipaddr, port):
        if self.test:
            return Status.TEST.value
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ipaddr, port))
            s.send(b"RUNTIMESTATS")
            data = s.recv(256)
            s.close()

            if data.find(b"BADCMD") != -1:
                logger.debug(data)
                return Status.BAD_COMMAND.value
            data = int(data.split()[1])
            return data
        except:
            logger.exception("connection reset (by peer?)")
            return Status.SERVER_RUNNING.value


    # Check that service is running (accept tcp connection)
    def check_service(self, idx, type, ipaddr, port):
        if self.test:
            return Status.TEST
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        if sock.connect_ex((ipaddr, port)) == 0:
            self.lab.setstatus(idx, self.s_service)  #
            if type == type_efu:
                status = self.check_efu_pipeline(ipaddr, port)
                if status == 0:
                    self.lab.clearstatus(
                        idx, self.s_stage1 | self.s_stage2 | self.s_stage3
                    )
                else:
                    self.lab.setstatus(idx, status)
                self.lab.servers[idx][9] = self.efu_get_version(ipaddr, port)
            elif type == type_fw:
                status = self.check_fw_pipeline(ipaddr, port)
                if status in (Status.INVALID, Status.SERVER_RUNNING):
                    self.lab.clearstatus(
                        idx, self.s_stage1 | self.s_stage2 | self.s_stage3
                    )
                else:
                    # If there is no status we change it to "server running"
                    self.lab.setstatus(idx, status.value)
            else:
                self.lab.setstatus(idx, self.s_stage1 | self.s_stage2 | self.s_stage3)
        else:
            self.lab.clearstatus(idx, self.s_service)
            logger.info("no service for {}:{}".format(ipaddr, port))


    def getstatus(self):
        for idx, res in enumerate(self.lab.servers):
            name, type, status, ip, port, ang, xo, yo, grafana, sw = res
            if not self.is_offline(status):
                if self.check_ping(ip):
                    self.lab.setstatus(idx, self.s_ping)
                    self.check_service(idx, type, ip, port)
                else:
                    self.lab.clearstatus(idx, self.s_ping)


    def printbox(self, x, y, a, color, efu, motext="", width=25):
        if efu:
            res = '<use href="#chevron" width="{}" height="10" '.format(width)
        else:
            res = '<rect width="{}" height="10" '.format(width)
        res = res + 'x="{}" y="{}" transform="rotate({} 400 200)" '.format(x, y, a)
        if motext != "" and color != col1:
            res = (
                res
                + "onmousemove=\"if(!window.parent.location.href.endsWith('.svg'))window.parent.showTooltip(evt, '{}');\" onmouseout=\"if(!window.parent.location.href.endsWith('.svg'))window.parent.hideTooltip();\" ".format(
                    motext
                )
            )

        if color == col4:
            res = res + 'fill="url(#dhatch)"'
        elif color == "none":
            res = res + 'fill="none" stroke="black"'
        else:
            res = res + 'fill="{}"'.format(color)
        res = res + "/>"
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
        texty = boxy + 7
        textx = 450 + ofsx
        common = '<text class="names" y="{}" transform="rotate({} 400 200)"'.format(
            texty, angle
        )
        if type == type_efu:
            self.printbox(506 + ofsx, boxy, angle, self.statetocolor(1, state), 1, mouseovertext)
            self.printbox(528 + ofsx, boxy, angle, self.statetocolor(2, state), 1, mouseovertext)
            self.printbox(550 + ofsx, boxy, angle, self.statetocolor(4, state), 1, mouseovertext)
            self.mprint('{} font-size="8px" x="450">{}</text>'.format(common, name))
        elif type == type_text:
            self.mprint('{} font-size="12px" x="{}">{}</text>'.format(common, textx, name))
        else:
            self.printbox(505 + ofsx, boxy,angle, self.statetocolor(1, state), 0, mouseovertext)
            self.mprint('{} font-size="8px" x="{}">{}</text>'.format(common, textx, name))
        self.mprint("")

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
        self.printbox(600, 125, 0, "none", 1, 60)
        self.mprint('{}   y="132" >data flow</text>'.format(common))

    def generatesvg(self):

        svg_buffer = ""

        self.mprint(htmlsvg.HEADER)
        name = os.path.basename(os.path.normpath(self.directory))
        self.mprint(
            f'<text x="350" y="12" fill="white" font-size="36px">{name.upper()}</text>'
        )
        self.mprint(f'<image x="0" y="300" height="100" width="100" href="/{self.directory}/logo.jpeg" />')

        for name, type, status, ip, port, angle, xo, yo, url, sw in self.lab.servers:
            logger.debug("{} {} {} {}".format(name, type, status, ip))
            if url != "none":
                self.mprint('<a href="{}" target="_blank">'.format(html.escape(url)))
            mouseovertext = "{}:{}&#60;br /&#62;{}".format(ip, port, sw)
            self.printinst(
                name.replace("&nbsp;", "&#160;"),
                mouseovertext,
                type,
                status,
                angle,
                xo,
                yo,
            )
            if url != "none":
                self.mprint("</a>")

        self.makelegend()
        self.mprint(
            '<text x="10" y="5" fill="white" font-size="16px">{}</text>'.format(
                self.gettime()
            )
        )
        self.mprint(
            '<text x="690" y="395" fill="black" font-size="8px">started {}</text>'.format(
                self.starttime
            )
        )
        self.mprint("</svg>")

    def one_pass(self):
        self.getstatus()
        self.generatesvg()
        self.flush()

    def run(self):
        while True:
            start = time.time()
            self.one_pass()
            dt = time.time() - start
            if (self.refresh - dt) > 0:
                time.sleep(self.refresh - dt)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-f", "--file", type=str, default="./config/utgaard.csv")
    parser.add_argument("-r", "--refresh", type=int, default=5)
    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("-o", "--out", type=str, default=".")
    args = parser.parse_args()
    # edit refresh into index rather than svg, in case of svg issues
    # file already in place from start-up script
    with open(f"{args.out}/index.html", "r", encoding="utf8") as f:
        newlines = []
        for line in f.readlines():
            newlines.append(line.replace("###refresh###", f"{args.refresh * 1000}")
                            .replace("dashboard.svg", f"/{args.out}/dashboard.svg"))
    serverlist = ECDCServers(args.file, args.out)
    mon = Monitor(serverlist, args)
    mon.sync_write_fs("index.html", "".join(newlines))

    print("Dashboard generator is running ...")
    mon.run()


if __name__ == "__main__":
    main()
