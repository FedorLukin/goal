"""Модуль плейлиста."""


from linked_list import LinkedList


class Composition:
    """Музыкальная композиция."""

    def __init__(self, path, title="Без названия", artist="Неизвестен", ):
        self.title = title
        self.artist = artist
        self.path = path

    @property
    def display_name(self):
        """Имя автора и название композиции."""
        return f"{self.artist} — {self.title}"

    def __str__(self):
        return self.display_name

    def __repr__(self):
        return (
            f"Composition("
            f"title={self.title!r}, "
            f"artist={self.artist!r}, "
            f"path={self.path!r})"
        )


class PlayList(LinkedList):
    """Плейлист, основанный на кольцевом двусвязном списке."""

    def __init__(self, name):
        super().__init__()
        self.name = name
        self._current = None

    def play_all(self, item):
        """Начать проигрывание с указанного элемента."""
        if item is None:
            self._current = None
            return None

        self._current = item
        return self.current

    def next_track(self):
        """Перейти к следующему треку."""
        if self._current is None:
            return None

        self._current = self._current.next_item
        return self.current

    def previous_track(self):
        """Перейти к предыдущему треку."""
        if self._current is None:
            return None

        self._current = self._current.previous_item
        return self.current

    @property
    def current(self):
        """Текущая композиция."""
        return None if not self._current else self._current.data

    @property
    def current_item(self):
        """Текущий элемент плейлиста."""
        return self._current
