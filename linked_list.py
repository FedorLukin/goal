class LinkedListItem:
    """Узел связного списка"""
    def __init__(self, data=None):
        self.data = data
        self._next = self
        self._previous = self

    @property
    def next_item(self):
        """Следующий элемент"""
        return self._next

    @next_item.setter
    def next_item(self, new_item):
        new_item._isolate()

        old_next = self._next
        
        self._next, old_next._previous = new_item, new_item
        new_item._next, new_item._previous = old_next, self

    @property
    def previous_item(self):
        """Предыдущий элемент"""
        raise NotImplementedError()

    @previous_item.setter
    def previous_item(self, new_item):
        new_item._isolate

        old_previous = self._previous
        
        self._previous, old_previous._next  = new_item, new_item
        new_item._previous, new_item._next = old_previous, self

    def __repr__(self):
        raise NotImplementedError()
    
    def _isolate(self):
        if self.next is not None:
            self._previous._next = self._next
            self._next._previous = self._previous
        self._next, self._previous = self, self 


class LinkedList:
    """Связный список"""
    def __init__(self, first_item=None):
        self.first_item = None

    @property
    def last(self):
        return self.first_item._previous if self.first_item else None

    def append_left(self, item):
        """Добавление слева"""
        if not self.head:
            self.head = item
        self.head.previous_item = item
        self.head = item

    def append_right(self, item):
        """Добавление справа"""
        if self.head:
            self.last.

    def append(self, item):
        """Добавление справа"""
        raise NotImplementedError()

    def remove(self, item):
        """Удаление"""
        raise NotImplementedError()

    def insert(self, previous, item):
        """Вставка справа"""
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def __getitem__(self, index):
        raise NotImplementedError()

    def __contains__(self, item):
        raise NotImplementedError()

    def __reversed__(self):
        raise NotImplementedError()
