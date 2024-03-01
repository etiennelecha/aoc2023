import re
from time import time

start = time()


class DLLNode:
    def __init__(self, label, focal) -> None:
        '''
        The famous doubly linked list. No head or tail, it loops on itself.
        '''
        self.label = label
        self.focal = focal
        self.next = self
        self.prev = self


    def add(self, node):
        '''
        adds self AFTER node. Yes this is arbitrary
        '''  
        self.prev = node
        self.next = node.next
        node.next = self
        self.next.prev = self


    def replace(self, new):
        self.prev.next = new
        self.next.prev = new
        new.prev = self.prev
        new.next = self.next

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
    


re_label = re.compile(r"[a-z]+")
re_op = re.compile(r"[=\-]")
re_focal = re.compile(r"[1-9]")

def hash(s):
    ans = 0
    for c in s:
        ans = ((ans + ord(c)) * 17) % 256
    return ans


if __name__ == "__main__":
    with open("inputs/day15.txt") as f:
        whole_input = f.read()
    strings = whole_input.split(",")
    ans1 = 0
    ans2 = 0
    boxes_head = []
    for i in range(256):
        head = DLLNode("HEAD", 0)
        boxes_head.append(head)
    for s in strings:
        h = hash(s)
        ans1 += h
        label = re_label.match(s).group()
        op = re_op.search(s).group()
        box_number = hash(label)

        head = boxes_head[box_number]
        ptr = head.next

        while ptr.label != label and ptr is not head:
            ptr = ptr.next
            
        if op == "-":
            if ptr.label == "HEAD":
                continue
            ptr.remove()
        else:
            focal = int(re_focal.search(s).group())
            new_lens = DLLNode(label, focal)
            if ptr.label != "HEAD":
                ptr.replace(new_lens)
            else:
                tail = head.prev # YUUUGE trick
                new_lens.add(tail)
                                
    for i, box in enumerate(boxes_head):
        ptr = box.next
        slot = 1
        while ptr is not box:
            ans2 += (i + 1) * slot * ptr.focal
            slot += 1
            ptr = ptr.next

    m, s = divmod(time() - start, 60)

    print(f"    \u2022 first part: {ans1}")
    print(f"    \u2022 second part: {ans2}")
    print(f"Done in {m:.0f}m{s:.4f}s")
