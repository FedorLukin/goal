"""Модуль кольцевого двусвязного списка."""


class LinkedListItem:
    """Элемент двусвязного списка."""

    def __init__(self, data=None):
        self.data = data
        self._next = None
        self._previous = None

    @property
    def next_item(self):
        """Следующий элемент."""
        return self._next

    @next_item.setter
    def next_item(self, new_item):
        self._next = new_item

        if new_item is self:
            self._previous = self
        elif new_item is not None:
            new_item._previous = self

    @property
    def previous_item(self):
        """Предыдущий элемент."""
        return self._previous

    @previous_item.setter
    def previous_item(self, new_item):
        self._previous = new_item

        if new_item is self:
            self._next = self
        elif new_item is not None:
            new_item._next = self

    def __eq__(self, other):
        """Сравнение элемента с другим элементом или его данными."""
        if isinstance(other, LinkedListItem):
            return self.data == other.data

        return self.data == other

    def __repr__(self):
        return f"LinkedListItem({self.data!r})"

    def _isolate(self):
        """Удалить элемент из цепочки."""
        previous = self._previous
        next_item = self._next

        if previous is not None and previous is not self:
            previous._next = next_item

        if next_item is not None and next_item is not self:
            next_item._previous = previous

        self._next = None
        self._previous = None


class LinkedList:
    """Кольцевой двусвязный список."""

    def __init__(self, first_item=None):
        self.first_item = first_item
        self._next_item = None
        self._iteration_start = None

    @property
    def last(self):
        """Последний элемент списка."""
        if self.first_item is None:
            return None

        return self.first_item.previous_item

    def append_left(self, item):
        """Добавить элемент в начало списка."""
        new_item = LinkedListItem(item)

        if self.first_item is None:
            new_item.next_item = new_item
            self.first_item = new_item
            return new_item

        old_first = self.first_item
        old_last = self.last

        new_item.next_item = old_first
        new_item.previous_item = old_last

        self.first_item = new_item

        return new_item

    def append_right(self, item):
        """Добавить элемент в конец списка."""
        new_item = LinkedListItem(item)

        if self.first_item is None:
            new_item.next_item = new_item
            self.first_item = new_item
            return new_item

        old_first = self.first_item
        old_last = self.last

        old_last.next_item = new_item
        new_item.next_item = old_first

        return new_item

    def append(self, item):
        """Добавить элемент в конец списка."""
        return self.append_right(item)

    def remove(self, item):
        """Удалить первый элемент с указанными данными."""
        for current in self:
            if current.data == item:
                if current is self.first_item:
                    if current is self.last:
                        self.first_item = None
                    else:
                        self.first_item = current.next_item

                current._isolate()
                return current

        raise ValueError("Элемент отсутствует в списке.")

    def insert(self, previous, item):
        """Вставить новый элемент после указанного."""
        new_item = LinkedListItem(item)
        next_item = previous.next_item

        previous.next_item = new_item
        new_item.next_item = next_item

        return new_item

    def __len__(self):
        """Количество элементов."""
        return sum(1 for _ in self)

    def __iter__(self):
        """Начать итерацию по списку."""
        self._next_item = self.first_item
        self._iteration_start = self.first_item

        return self

    def __next__(self):
        """Получить следующий элемент."""
        if self._next_item is None:
            raise StopIteration

        result = self._next_item
        self._next_item = result.next_item

        if self._next_item is self._iteration_start:
            self._next_item = None

        return result

    def __getitem__(self, index):
        """Получить элемент по индексу."""
        if index < 0:
            index += len(self)

        if index < 0:
            raise IndexError("Некорректный индекс.")

        for current_index, item in enumerate(self):
            if current_index == index:
                return item

        raise IndexError("Некорректный индекс.")

    def __contains__(self, item):
        """Проверка наличия элемента."""
        return any(current.data == item for current in self)

    def __reversed__(self):
        """Итерация по списку в обратном направлении."""
        if self.first_item is None:
            return

        start = self.last
        current = start

        while True:
            yield current

            current = current.previous_item

            if current is start:
                break
