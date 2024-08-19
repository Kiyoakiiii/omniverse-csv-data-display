import omni.ui as ui
from .models import MainModel

class MainView():
    def __init__(self, csvmodel: MainModel):
        self.csvmodel = csvmodel
        self._window = None

        # 初始化 UI
        self._init_ui()

    def _init_ui(self):
        # 创建窗口，设置颜色和样式
        self._window = ui.Window("data", width=400, height=200, dockPreference=ui.DockPreference.RIGHT_TOP)
        self._window.visible = True

        # 设置窗口的样式和框架布局
        with self._window.frame:
            with ui.ZStack():
                ui.Rectangle(style={"background_color": 0xaaffcccc})

                self.header_labels = []
                self.value_labels = []

                # 使用 VGrid 布局，设置列数为2，并定义布局风格
                with ui.VGrid(column_count=2, alignment=ui.Alignment.TOP, style={"margin": 20}):
                    # 初始化表头和数据标签，留空，稍后更新
                    for _ in range(2):  # 假设有两个数据列（CPU Usage 和 GPU Usage）
                        header_label = ui.Label("", style={"font_size": 20, "color": 0xffffffff, "alignment": ui.Alignment.CENTER})
                        value_label = ui.Label("", style={"font_size": 20, "color": 0xffffffff, "alignment": ui.Alignment.CENTER})
                        self.header_labels.append(header_label)
                        self.value_labels.append(value_label)

        # 初始化完成后，更新 UI 以显示初始数据
        self.update_ui()

    def update_ui(self):
        if not self._window or not self._window.frame:
            return

        # 读取 CSV 数据
        self.csvmodel.read_csv()
        headers, csv_data = self.csvmodel.get_csv_data()

        # 更新表头和数据
        for i in range(len(headers)):
            if i < len(self.header_labels):
                self.header_labels[i].text = headers[i]
            if i < len(self.value_labels):
                self.value_labels[i].text = csv_data[i]

    def destroy(self):
        if self._window:
            self._window.destroy()
            self._window = None
