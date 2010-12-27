import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

iconDict = {"tube":"icon-tube.gif", "bus":"icon-buses.gif", "train":"icon-rail.gif", "dlr":"icon-dlr.gif",
            "coach":"icon-coach.gif", "cycle":"icon-cycle.gif", "tram":"icon-trams.gif", "walk":"icon-walk.gif",
            "river":"icon-rivers.gif"}

default_list = [(["tube"],1),(["train"],2),(["dlr"],3),(["cycle"],4)]
ICON_SPACING = 2
TEXT_SPACING = 5
LIST_HEIGHT_EXCESS = 10

####################################################################
def main(args):
    app = QApplication(sys.argv)
    w = ListWindow()
    w.show()
    sys.exit(app.exec_())

####################################################################
class ListWindow(QWidget):
    def __init__(self, list_data = default_list, *args):
        QWidget.__init__(self, *args)

        #print list_data
        lm = MyListModel(list_data, self)
        de = MyDelegate(self)
        lv = QListView()
        lv.setModel(lm)
        lv.setItemDelegate(de)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(lv)
        self.setLayout(layout)

####################################################################
class MyDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    def paint(self, painter, option, index):
        painter.save()

        # set background color
        painter.setPen(QPen(Qt.NoPen))
        linGrad = QLinearGradient(option.rect.left(), option.rect.top(),option.rect.left(), option.rect.bottom())

        if option.state & QStyle.State_Selected:
            linGrad.setColorAt(0, QColor(0xFF,0xFF,0xFF))
            linGrad.setColorAt(1, QColor(0xCC,0xCC,0xCC))

            painter.setBrush(QBrush(linGrad))
        else:
            linGrad.setColorAt(0, QColor(0xFF,0xFF,0xFF))
            linGrad.setColorAt(1, QColor(0xCC,0xFF,0xFF))
            painter.setBrush(QBrush(linGrad))
        painter.drawRect(option.rect)

        #draw icons
        model = index.model()
        jlist = model.listdata[index.row()]
        imageWidth = option.rect.left()
        for modes in jlist[0]:
            image = QImage(iconDict[modes])
            painter.drawImage(imageWidth, option.rect.top(), image)
            imageWidth += image.rect().right() + ICON_SPACING

        # set text color
        painter.setPen(QPen(Qt.black))
        value = index.data(Qt.DisplayRole)
        imageWidth += TEXT_SPACING
        textRect = QRect(imageWidth, option.rect.top(), option.rect.width()-imageWidth, option.rect.height())

        if value.isValid():
            text = str(jlist[1])
            painter.drawText(textRect, Qt.AlignLeft| Qt.AlignVCenter, text)
        painter.restore()

    
    def sizeHint(self, option, index):
        size = QItemDelegate.sizeHint(self, option, index)
        return QSize(size.width(), size.height()+LIST_HEIGHT_EXCESS)

####################################################################
class MyListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else:
            return QVariant()

####################################################################
if __name__ == "__main__":
    main(sys.argv[1:])

