from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QPoint, QTimer, QSize, QRectF, pyqtSignal, QObject
import sys, random, math, time

class BubbleSort:
    @staticmethod
    def sort(target_list, increased_order, screen):
        if increased_order:
            list_size = len(target_list)
            count = 0
            for num in range(list_size - 1):
                done = True
                for compare in range(list_size - 1 - num):
                    count += 1
                    if target_list[compare] > target_list[compare + 1]:
                        target_list[compare], target_list[compare + 1] = target_list[compare + 1], target_list[compare]
                        screen.bubbleProgress(count, compare, compare + 1)
                        done = False
                if done:
                    break
            screen.bubbleProgress(count, -1, -1)
        return target_list

class visualObj(QObject):
    moveToDest = pyqtSignal()
    def __init__(self, x, y, val):
        super().__init__()
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.value = val
        # self.color = QColor(255, 5, 5, 100)
        self.glowing = False
        self.v = [0, 0]
        self.moving = False
        self.dest = [0, 0]
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(20)
    def color(self):
        if self.glowing:
            return QColor(255, 5, 5, 100)
        else:
            return QColor(255, 255, 255, 255)

    def move(self):
        if self.moving:
            if ((self.pos_x + self.v[0] - self.dest[0]) * Window.PER_COLUMN) ** 2 < ((self.pos_x - self.dest[0]) * Window.PER_COLUMN) ** 2 or \
                ((self.dest[1] - (self.pos_y + self.v[1])) * Window.PER_ROW) ** 2 < ((self.dest[1] - self.pos_y ) * Window.PER_ROW) ** 2:
                self.pos_x = self.pos_x + self.v[0]
                self.pos_y = self.v[1] + self.pos_y
            else:
                self.moving = False
                self.pos_x = float(round(self.pos_x))
                self.pos_y = float(round(self.pos_y))
                self.moveToDest.emit()    
    def stop():
        self.moving = False
            
    def setDest(self, x, y):
        self.dest[0] = float(round(x))
        self.dest[1] = float(round(y))
        self.v[0] = (x - self.pos_x) / 10
        self.v[1] = (y - self.pos_y) / 10
        self.moving = True
        

class Window(QWidget):
    #static var
    PER_ROW = 0
    PER_COLUMN = 0
    FIRST_ROW = QPoint(10, 10)
    def __init__(self,width, height):
        super().__init__()
        self.timeInterval = 1000 # 1 second
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle('BubbleSort')
        self.objects = []
        self.current = 0 #current index of comparison(first)
        self.walk_through = []
        self.total_compare = 0
        self.switching = False
        self.log = []
        self.switch_called = 0
        self.show()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(190)
        self.last_show_time = -1 #never shown
        rnd = [i for i in range(1,10)]
        random.shuffle(rnd)
        # self.init_data(5, 42, 85, 35, 20)
        self.init_data(*rnd)
        self.showBubbleSort()
        
        self.stage = 0
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawData(qp)
        qp.end()
    def drawData(self, qp):
        qp.setPen(Qt.blue)
        
        # qp.drawText(10, 10, str(self.log))
        row_index = 0
        size = self.size()
        for obj in self.objects:
            qp.setBrush(obj.color())
            qp.drawRect( Window.FIRST_ROW.x() + obj.pos_x * Window.PER_COLUMN, round(Window.FIRST_ROW.y() + obj.pos_y * Window.PER_ROW ), Window.PER_ROW * 2 / 3,\
                Window.PER_ROW * 2 / 3)
            text = QTextOption()
            text.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(Window.PER_ROW / 2)
            qp.setFont(font)
            qp.drawText(QRectF(Window.FIRST_ROW.x() + obj.pos_x * Window.PER_COLUMN , round(Window.FIRST_ROW.y() + obj.pos_y * Window.PER_ROW ),\
                 Window.PER_ROW * 2 / 3, Window.PER_ROW * 2 / 3), str(obj.value), text)
        self.update()
    def showBubbleSort(self):
        print(BubbleSort.sort([obj.value for obj in self.objects], True, self))
        print(self.log)
        cnt = 0
        for i in range(len(self.objects) - 1):
            for j in range(len(self.objects) - 1 - i):
                if cnt == self.total_compare:
                    return
                self.walk_through.append(j)
                self.walk_through.append(j + 1)
                cnt += 1
    def init_data(self, *args):
        for i in range(len(args)):
            newObj = visualObj(i, 0 , args[i])
            newObj.moveToDest.connect(self.switchItem)
            self.objects.append(newObj)

        
    def bubbleProgress(self, count, swap_index1, swap_index2):
        if swap_index1 == -1:
            self.total_compare = count
            return
        self.log.append((swap_index1, swap_index2))

    def animate(self):
        
        for obj in self.objects:
            obj.glowing = False
        
       
        if len(self.log) != 0:
            if self.walk_through[self.current - 1]== self.log[0][0] and self.walk_through[self.current ]  == self.log[0][1] and not self.switching:
                self.switchItem()
                self.switchItem()
                # pass
            if self.switching:
                self.objects[self.walk_through[self.current - 1]].glowing = True
                self.objects[self.walk_through[self.current ]].glowing = True
            else :
                self.objects[self.walk_through[self.current]].glowing = True
                self.objects[self.walk_through[self.current + 1]].glowing = True
                
            if not self.switching and self.current <= len(self.walk_through) - 1:
                self.current += 1
        
    def switchItem(self):
        self.switch_called += 1
        if self.switch_called % 2 != 1:
            return
        
        if len(self.log) > 0:
            # if( (self.objects[self.log[0][0]].moving or self.objects[self.log[0][1]].moving)):
            #     return     
            if self.stage == 0 :
                if not self.switching:
                    self.switching = True #start
                else:
                    self.switching = False #end
                    return
                self.objects[self.log[0][0]].setDest(self.objects[self.log[0][0]].pos_x, 1 + self.objects[self.log[0][0]].pos_y)
                self.objects[self.log[0][1]].setDest(self.objects[self.log[0][1]].pos_x, 2 + self.objects[self.log[0][1]].pos_y)
                
            elif self.stage == 1:
                self.objects[self.log[0][0]].setDest(self.objects[self.log[0][1]].pos_x, self.objects[self.log[0][0]].pos_y)
                self.objects[self.log[0][1]].setDest(self.objects[self.log[0][0]].pos_x, self.objects[self.log[0][1]].pos_y)
            elif self.stage == 2:
                self.objects[self.log[0][0]].setDest(self.objects[self.log[0][0]].pos_x, self.objects[self.log[0][0]].pos_y -  1 )
                self.objects[self.log[0][1]].setDest(self.objects[self.log[0][1]].pos_x, self.objects[self.log[0][1]].pos_y - 2)
                self.objects[self.log[0][0]], self.objects[self.log[0][1]] = self.objects[self.log[0][1]], self.objects[self.log[0][0]]
                self.log.pop(0)
                
            self.stage += 1
            if self.stage > 2:
                self.stage = 0
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.timer.stop()
        elif event.key() == Qt.Key_A:
            self.timer.start(190)
        event.accept()

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window.PER_ROW = int(QDesktopWidget().screenGeometry().height() / 5)
    Window.PER_COLUMN =  int(QDesktopWidget().screenGeometry().height() / 5)#int(QDesktopWidget().screenGeometry().width() / 40)
    mainWin = Window(int(QDesktopWidget().screenGeometry().width()), int(QDesktopWidget().screenGeometry().height()))
    sys.exit(app.exec_())
        



