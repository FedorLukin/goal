
class Composition:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class LinkedList:
    def __init__(self):
        self.head = None

    def append_left(self, item):
        if not self.head:
            item.next = item
            item.prev = item
            self.head = item
        else:
            last_item = self.last()
            item.prev = self.head.prev
            item.next = self.head
            self.head = item
            last_item.next = item
    
    def last(self):
        return self.head.prev




song1 = Composition('Мия гойка - я экспат')
song2 = Composition('Игорь вихорьков - ты сука не моя')
song3 = Composition('Реп игрок 2006 - женщины сосут')
playlist = LinkedList()
playlist.append_left(song1)
playlist.append_left(song2)
playlist.append_left(song3)
print(playlist.head.next.next.next.next)