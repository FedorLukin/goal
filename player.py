"""Модуль плеера."""

from mutagen import File


from PyQt6 import uic
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QInputDialog,
    QListWidgetItem,
    QLineEdit,
    QMainWindow,
)

from playlist import Composition, PlayList


class PlayerWindow(QMainWindow):
    """Главное окно музыкального плеера."""

    def __init__(self):
        super().__init__()

        uic.loadUi("main.ui", self)

        self.playlists = []
        self.current_playlist = None

        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(0.5)

        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)

        self.setup_connections()

        self.player.mediaStatusChanged.connect(self.media_status_changed)

    def setup_connections(self):
        """Подключить обработчики событий."""
        self.createPlaylistButton.clicked.connect(self.create_playlist)
        self.deletePlaylistButton.clicked.connect(self.delete_playlist)
        self.addTrackButton.clicked.connect(self.add_track)
        self.removeTrackButton.clicked.connect(self.remove_track)
        self.playButton.clicked.connect(self.toggle_play_pause)
        self.previousButton.clicked.connect(self.previous_track)
        self.nextButton.clicked.connect(self.next_track)
        self.playlistWidget.currentRowChanged.connect(self.select_playlist)
        self.trackWidget.setDragEnabled(True)
        self.trackWidget.setAcceptDrops(True)
        self.trackWidget.setDropIndicatorShown(True)
        self.trackWidget.setDragDropMode(
            QAbstractItemView.DragDropMode.InternalMove
            )
        self.trackWidget.itemClicked.connect(self.select_track)
        self.trackWidget.model().rowsMoved.connect(self.change_order)

    def create_playlist(self):
        """Создать новый плейлист.""" 

        name, ok = QInputDialog.getText(
            self,
            "Новый плейлист",
            "Название:",
            QLineEdit.EchoMode.Normal,
            f"Плейлист {len(self.playlists) + 1}"
        )

        if not ok or not name.strip():
            return

        playlist = PlayList(name.strip())
        self.playlists.append(playlist)

        self.playlistWidget.addItem(playlist.name)
        self.playlistWidget.setCurrentRow(len(self.playlists) - 1)

    def delete_playlist(self):
        """Удалить выбранный плейлист."""

        row = self.playlistWidget.currentRow()

        if row < 0:
            return

        self.player.stop()

        del self.playlists[row]

        self.playlistWidget.takeItem(row)

        if not self.playlists:
            self.current_playlist = None
            self.trackWidget.clear()
            return

        if row >= len(self.playlists):
            row = len(self.playlists) - 1

        self.playlistWidget.setCurrentRow(row)

    def select_playlist(self, row):
        """Выбрать плейлист."""

        if row < 0 or row >= len(self.playlists):
            self.current_playlist = None
            self.trackWidget.clear()
            return

        self.current_playlist = self.playlists[row]

        self.refresh_tracks()

    def add_track(self):
        """Добавить композицию в текущий плейлист."""

        if self.current_playlist is None:
            return

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите музыкальную композицию",
            "",
            "Audio (*.mp3 *.wav *.ogg *.flac)",
        )

        if not path:
            return

        audio = File(path)
        audio_artist = audio.get('artist', ['Неизвестен'])[0]
        audio_title = audio.get('title', ['Без названия'])[0]

        title, ok = QInputDialog.getText(
            self,
            "Название композиции",
            "Название:",
            QLineEdit.EchoMode.Normal,
            audio_title
        )

        if not ok:
            return

        artist, ok = QInputDialog.getText(
            self,
            "Исполнитель",
            "Исполнитель:",
            QLineEdit.EchoMode.Normal,
            audio_artist
        )

        if not ok:
            return

        composition = Composition(
            title=title or "Без названия",
            artist=artist or "Неизвестен",
            path=path,
        )

        self.current_playlist.append(composition)
        self.refresh_tracks()

    def remove_track(self):
        """Удалить выбранную композицию."""

        if self.current_playlist is None:
            return

        row = self.trackWidget.currentRow()

        if row < 0:
            return

        item = self.current_playlist[row]

        if item is self.current_playlist.current_item:
            self.player.stop()
            self.current_playlist.current_item = None

        self.current_playlist.remove(
            item.data
        )

        self.refresh_tracks()

    def toggle_play_pause(self):

        """Запустить или поставить на паузу текущую композицию."""

        if self.current_playlist is None:
            return

        if self.current_playlist.current_item is None:
            self.trackWidget.setCurrentRow(0)
            self.play_selected()
            return

        if self.player.playbackState() == (
            QMediaPlayer.PlaybackState.PlayingState
        ):
            self.player.pause()
            self.playButton.setText("Воспроизвести")
        elif self.player.playbackState() == (
            QMediaPlayer.PlaybackState.StoppedState
        ):
            print('zzz')
            self.play_selected()
        else:
            self.player.play()
            self.playButton.setText("Пауза")

    def play_selected(self):
        """Воспроизвести выбранную композицию."""

        if self.current_playlist is None:
            return

        row = self.trackWidget.currentRow()

        item = self.current_playlist[row]
        self.play_item(item)

    def play_item(self, item):
        """Начать воспроизведение указанной композиции."""

        composition = self.current_playlist.play_all(item)

        if composition is None:
            return

        self.player.setSource(
            QUrl.fromLocalFile(composition.path)
        )

        self.player.play()

        self.playButton.setText("Пауза")

        self.update_current_track()

    def next_track(self):
        """Перейти к следующей композиции."""

        if self.current_playlist is None:
            return

        composition = self.current_playlist.next_track()

        if composition is None:
            return

        self.player.setSource(
            QUrl.fromLocalFile(
                composition.path
            )
        )

        self.player.play()
        self.playButton.setText("Пауза")
        self.update_current_track()

    def previous_track(self):
        """Перейти к предыдущей композиции."""

        if self.current_playlist is None:
            return

        composition = (
            self.current_playlist.previous_track()
        )

        if composition is None:
            return

        self.player.setSource(
            QUrl.fromLocalFile(
                composition.path
            )
        )

        self.player.play()
        self.playButton.setText("Пауза")
        self.update_current_track()

    def media_status_changed(self, status):
        """Запустить следующий трек после окончания текущего."""

        if status != QMediaPlayer.MediaStatus.EndOfMedia:
            return

        self.next_track()

    def refresh_tracks(self):
        """Обновить виджет треков."""
        self.trackWidget.clear()

        if self.current_playlist is None:
            return

        for item in self.current_playlist:
            list_item = QListWidgetItem(item.data.display_name)
            list_item.setData(Qt.ItemDataRole.UserRole, item)
            self.trackWidget.addItem(list_item)

    def update_current_track(self):
        """Выделить текущий трек в списке."""

        if self.current_playlist is None:
            return

        current = self.current_playlist.current_item

        if current is None:
            return

        for index, item in enumerate(
            self.current_playlist
        ):
            if item is current:
                self.trackWidget.setCurrentRow(index)
                break

    def change_order(self, *_):
        """Изменить порядок композиций."""
        items = [
            self.trackWidget.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self.trackWidget.count())
        ]

        self.current_playlist.first_item = items[0]

        for i, item in enumerate(items):
            item._previous = items[i - 1]
            item._next = items[(i + 1) % len(items)]

        self.refresh_tracks()

    def select_track(self, item):
        """Выбрать композицию мышью."""
        composition = self.current_playlist[self.trackWidget.row(item)]

        if self.player.playbackState() == (
            QMediaPlayer.PlaybackState.PlayingState
        ):
            self.play_selected()
        else:
            self.player.stop()
            self.current_playlist.current_item = composition

        self.update_current_track()
