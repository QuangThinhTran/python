NOT_STARTED = "Chưa bắt đầu"
IN_PROGRESS = "Đang thực hiện"
COMPLETED = "Đã hoàn thành"
STATUSES = [NOT_STARTED, IN_PROGRESS, COMPLETED]


class Util:
    def __init__(self, root):
        self.root = root

    def center_window(self, window, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")
