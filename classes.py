class Composition:
    def __init__(self):
        pass

class LinkedList:
    def __init__(self):
        self.head = None

    def append_left(self, item):
        if not self.head:
            item.prev, item.next = item, item
        else:
            last_item = self.last()
            item.prev, item.next = last_item, self.head
            last_item.next = item
        self.head = item

    def append_right(self, item):
        if not self.head:
            return self.append_left(item=item)

        last_item = self.last()
        item.prev, item.next = last_item, self.head
        last_item.next, self.head.prev = item, item

    def append(self, item):
        self.append_right(item=item)

    def remove(self, item):
        if item == self.head:
            self.head = self.head.next
            self.head.prev = self.tail
            self.tail.next = self.head
            return

        curr_item = self.head.next
        while curr_item != self.head:
            if curr_item != item:
                curr_item = curr_item.next
                continue

            curr_item.prev.next = curr_item.next
            curr_item.next.prev = curr_item.prev

            match curr_item:
                case self.head: self.head = curr_item
                case self.tail: self.tail = curr_item
            return

        raise ValueError
             

    def insert(self, previous, item):
        pass

    def last(self):
        return self.tail

class PlayList(LinkedList):
    pass