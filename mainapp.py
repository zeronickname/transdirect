import sys, Queue, threading, time
import transportd, listview
from PyQt4.QtCore import *
from PyQt4.QtGui import *

URL ="http://www.transportdirect.info/transportdirect/en/journeyplanning/jplandingpage.aspx?id=gman.me.uk&do=p&d=SW113TP&oo=en&on=cellID%20location&o=339892,405924&p=1"

progressB = ("|", "/", "-", "\\")

class getJOptions(threading.Thread):
    def __init__(self, result):
        threading.Thread.__init__(self)
        self.result = result

    def run(self):
        self.result.put(transportd.main(URL))


def main(debug):
    
    if debug == "debug":
        import cPickle
        f = open("example_data", "r")
        journeys = cPickle.load(f)
        f.close()
    else:
        result = Queue.Queue()
        t = getJOptions(result)
        t.start()
        #t.join()
        i = 0
        while t.isAlive():
            sys.stdout.write("\r%s" % progressB[i%4])
            sys.stdout.flush()
            i += 1
            time.sleep(0.2)

        journeys = result.get()

        if debug == "save":
            import cPickle
            f = open("example_data", "w")
            cPickle.dump(journeys, f)
            f.close()
    
    """
    line = ""
    print "-----------"
    for option in journeys:
        for index, cell in enumerate(option):
            if index == 0:
                for modes in cell:
                    line = line + str(modes) + ", "
                line = line + " | "
            elif index is not 5:
                line = line + str(cell) + " | "
        print line
        #print option[5]
        print "-------------"
        line = ""
    """

    viewList = []
    for option in journeys:
        modes = option[0]
        if modes[0] != "car":
            text = "Depart: %s -- Dur: %s" % (option[2], option[4])

            journey = [modes, text]
            viewList.append(journey)

    app = QApplication(sys.argv)
    w = listview.ListWindow(viewList)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv[1])
