import multiprocessing.dummy
import multiprocessing, subprocess

def ping(ipaddr):
    res = subprocess.Popen(["ping", "-c1", "-W1", ipaddr], stdout=subprocess.PIPE).stdout.read()
    if res.find(b" 0.0%") != -1:
        print("{} good".format(ipaddr))
        return True
    else:
        print("{} bad".format(ipaddr))
        return False

def ping_range(start, end):
    num_threads = 2 * multiprocessing.cpu_count()
    p = multiprocessing.dummy.Pool(num_threads)
    p.map(ping, ["172.30.242.{}".format(x) for x in range(start,end)])


if __name__ == "__main__":
    ping_range(21, 35)
