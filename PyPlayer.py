from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys
from PyQt5.QtMultimedia import QMediaRecorder, QCameraInfo

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("player.ico"))
        self.setWindowTitle("PyPlayer")
        self.setGeometry(350, 100, 700, 500)

        p=self.palette()
        p.setColor(QPalette.Window, Qt.red)
        self.setPalette(p)

        self.create_player()

    def create_player(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videowidget = QVideoWidget()
        self.openBtn = QPushButton('Open Video')
        self.openBtn.clicked.connect(self.open_file)

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.cropBtn = QPushButton()
        self.cropBtn.setEnabled(False)
        self.cropBtn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.cropBtn.clicked.connect(self.crop_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)


        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.cropBtn)
        hbox.addWidget(self.slider)

        vbox = QVBoxLayout()
        vbox.addWidget(self.videowidget)
        vbox.addLayout(hbox)

        self.mediaPlayer.setVideoOutput(self.videowidget)

        self.setLayout(vbox)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            self.cropBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()



    def crop_video(self):
        start = self.slider.minimum()
        end = self.slider.maximum()
        if start == end:
            return
        filename, _ = QFileDialog.getSaveFileName(self, "Save Video", "", "Video Files (*.mp4)")
        if filename != '':
            self.mediaPlayer.pause()
            self.mediaPlayer.setPosition(start)
            self.mediaPlayer.setVideoOutput(None)
            camera = QCameraInfo.defaultCamera()
            self.mediaRecorder = QMediaRecorder(self.mediaPlayer.mediaObject(), camera)
            self.mediaRecorder.setOutputLocation(QUrl.fromLocalFile(filename))
            self.mediaRecorder.setVideoSettings(self.mediaPlayer.media().canonicalVideoSettings())
            self.mediaRecorder.record()
            while self.mediaPlayer.position() < end:
                QApplication.processEvents()
            self.mediaRecorder.stop()
            self.mediaPlayer.setVideoOutput(self.videowidget)
            self.mediaPlayer.setPosition(start)





    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))   

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)       

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)  

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())          