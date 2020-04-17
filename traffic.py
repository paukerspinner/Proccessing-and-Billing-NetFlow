import pandas as pd

class Record:
    def __init__(self, time_start, srcAddr, dstAddr, inputBytes, outputBytes):
        self.ts = time_start
        self.sa = srcAddr
        self.da = dstAddr
        self.ibyt = inputBytes
        self.obyt = outputBytes
    
    def show(self):
        print("---".join([self.ts, self.sa, self.da, str(self.ibyt), str(self.obyt)]))


def getRecords(ipAddr):
    dstRecords = []
    srcRecords = []
    data = pd.read_csv('nfcapd.csv')
    for itm in data.values:
        if itm[3] == ipAddr:
            srcRecords.append(Record(itm[0], itm[3], itm[4], itm[12], itm[14]))
        if itm[4] == ipAddr:
            dstRecords.append(Record(itm[0], itm[3], itm[4], itm[12], itm[14]))
    return [srcRecords, dstRecords]

class Traffic:
    def __init__(self, ipAddr):
        self.srcRecords, self.dstRecords = getRecords(ipAddr)
    
    def calculateTraffic(self):
        total = 0
        for rc in self.srcRecords:
            total += rc.ibyt
        for rc in self.dstRecords:
            total += rc.obyt
        return total

    def calculateTarrif(self):
        return round(self.calculateTraffic() / 1024 * 1.5, 2)

    def trafficByTime(self):
        dicTraffic = {}
        for rc in self.srcRecords:
            old_value = dicTraffic.get(rc.ts) if dicTraffic.get(rc.ts) != None else 0
            dicTraffic.update({rc.ts : rc.ibyt + old_value})
        return dicTraffic