import keyboard
import win32gui
import win32process
import psutil
import logging


_NEXT = "f3"
_PREVIOUS = "f2"
_UPDATE = "f4"


class WindowsManager:

    @property
    def account_names(self):
        return [title.split(" - ")[0].strip() for title in self.windows]

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.windows = []
        self.active = 0
        self.update()

    def update(self, *args, **kwargs):
        self.windows.clear()
        win32gui.EnumWindows(self._enum_callback, None)
        if self.verbose:
            print(f"Found {len(self.windows)} accounts: {', '.join(self.account_names)}")

    def _enum_callback(self, hwnd, extra):
        tid, pid = win32process.GetWindowThreadProcessId(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        if "ime" in class_name.lower():
            return False
        title = win32gui.GetWindowText(hwnd)
        exe_name = psutil.Process(pid).name()
        if "dofus" in exe_name.lower():
            self.windows.append(title)
        return True

    def next(self, *args, **kwargs):
        title = self.windows[0]
        hwnd = win32gui.FindWindow(None, title)
        keyboard.press_and_release("alt")  # weird fix to focus fighting
        win32gui.SetForegroundWindow(hwnd)
        self.windows.append(self.windows.pop(0))

    def previous(self, *args, **kwargs):
        self.windows.insert(0, self.windows.pop())
        title = self.windows[-1]
        hwnd = win32gui.FindWindow(None, title)
        keyboard.press_and_release("alt")
        win32gui.SetForegroundWindow(hwnd)


def main():
    window_manager = WindowsManager(verbose=True)

    keyboard.on_press_key(_NEXT, window_manager.next)
    keyboard.on_press_key(_PREVIOUS, window_manager.previous)
    keyboard.on_press_key(_UPDATE, window_manager.update)

    keyboard.wait()


if __name__ == '__main__':
    main()
