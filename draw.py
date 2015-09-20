#!/usr/bin/env python

import proja
import sys
from PyQt4 import QtCore, QtGui


class DragButton(QtGui.QPushButton):

    def mousePressEvent(self, event):
        self.mousePressPos = None
        self.mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePressPos = event.globalPos()
            self.mouseMovePos = event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.mouseMovePos = globalPos

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.mousePressPos is not None:
            moved = event.globalPos() - self.mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(DragButton, self).mouseReleaseEvent(event)


class Forest(QtGui.QWidget):

    left_clicked = QtCore.pyqtSignal(int)

    def __init__(self):
        super(Forest, self).__init__()
        self.initUI()

    def new_node(self, node, pos):
        btn = DragButton(node.content, self)
        btn.setToolTip(node.author.name)
        btn.resize(btn.sizeHint())
        btn.move(*pos)

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        for agent in agents:
            self.new_node(agent.root, (50, 50))

        qle = QtGui.QLineEdit(self)
        qle.move(60, 100)

        self.left_clicked[int].connect(self.left_click)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timeout)
        self.left_click_count = self.right_click_count = 0

        self.lines = []
        self.mousePressPos = None
        self.mouseMovePos = None

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Tooltips')
        self.show()

    def timeout(self):
        if self.left_click_count >= self.right_click_count:
            self.left_clicked.emit(self.left_click_count)
        else:
            self.right_clicked.emit(self.right_click_count)
        self.left_click_count = self.right_click_count = 0

    def left_click(self, nb):
        if nb > 1:
            pass

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.left_click_count += 1
            if not self.timer.isActive():
                self.timer.start()

            self.mousePressPos = event.globalPos()
            self.mouseMovePos = event.globalPos()

        super(Forest, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            globalPos = event.globalPos()
            self.mouseMovePos = globalPos
            self.update()
        super(Forest, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.mousePressPos is not None:
            o = self.mapFromGlobal(self.mousePressPos)
            n = self.mapFromGlobal(self.mouseMovePos)

            self.lines.append([o.x(), o.y(), n.x(), n.y()])

            self.mousePressPos = None
            self.mouseMovePos = None
            self.update()
        super(Forest, self).mouseReleaseEvent(event)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        for line in self.lines:
            qp.drawLine(*line)

        if app.mouseButtons() == QtCore.Qt.LeftButton:
            if self.mousePressPos is not None:
                pen.setStyle(QtCore.Qt.DashDotLine)
                qp.setPen(pen)
                orig_rel = self.mapFromGlobal(self.mousePressPos)
                cur_rel = self.mapFromGlobal(self.mouseMovePos)
                qp.drawLine(
                    orig_rel.x(), orig_rel.y(), cur_rel.x(), cur_rel.y())

        qp.end()

        super(Forest, self).paintEvent(event)

agents = [proja.Agent('Alice'),
          proja.Agent('Bob'),
          proja.Agent('Charlie')
          ]

G = proja.PolyForest(agents)

alice = G.agents[0]
bob = G.agents[1]
node_cinema = proja.Node(
    author=alice, content='Want to go to the cinema?')
alice.root.add_child(node_cinema)
bob.root.add_child(node_cinema)

app = QtGui.QApplication(sys.argv)
w = Forest()
sys.exit(app.exec_())
