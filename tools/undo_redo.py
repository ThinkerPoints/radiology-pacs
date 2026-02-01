class Command:
    def undo(self): pass
    def redo(self): pass

class UndoStack:
    def __init__(self):
        self.stack = []
        self.index = -1

    def push(self, cmd):
        self.stack = self.stack[:self.index+1]
        self.stack.append(cmd)
        self.index += 1
        cmd.redo()

    def undo(self):
        if self.index >= 0:
            self.stack[self.index].undo()
            self.index -= 1

    def redo(self):
        if self.index+1 < len(self.stack):
            self.index += 1
            self.stack[self.index].redo()
