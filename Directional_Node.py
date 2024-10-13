dir2str = {
            (0,1):"UP   ",
            (0,-1):"DOWN ",
            (-1,0):"RIGHT",
            (1,0):"LEFT ",
        }
class DNode:
    def __init__(self,location,next,prev,direction):
        self.location = location
        self.next = next
        self.prev = prev
        self.direction = direction 
    def __str__(self):
        
        if self.next == None:
            nloc = None
        else:
            nloc = self.next.location
        if self.prev == None:
            ploc = None
        else:
            ploc = self.prev.location

        return f"Loc: {self.location}   Dir: {dir2str[self.direction]}   Next: {nloc}   Prev: {ploc}"
