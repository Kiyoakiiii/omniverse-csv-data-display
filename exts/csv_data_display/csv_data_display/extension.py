import carb
import omni.ext
import omni.kit.app
import time  # 引入 Python 的 time 模块
from .models import MainModel
from .views import MainView

class MyExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        carb.log_info(f"[CSV_Reader] MyExtension startup")
        self.model = MainModel()
        self._window = MainView(self.model)

        # 初始化时间
        self._last_update_time = time.time()

        # 注册更新事件，每帧都会调用
        self._update_event_sub = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(
            self._on_update
        )

    def _on_update(self, dt):
        # 获取当前时间
        current_time = time.time()

        # 如果距离上次更新超过 30 秒，则更新窗口
        if current_time - self._last_update_time > 5:
            self.update_data()
            self._last_update_time = current_time

    def update_data(self):
        carb.log_info("[CSV_Reader] Reading CSV and Updating UI")
        # 强制重新读取 CSV 数据
        self.model.read_csv()
        self._window.update_ui()

    def on_shutdown(self):
        carb.log_info(f"[CSV_Reader] MyExtension shutdown")
        if self._update_event_sub:
            self._update_event_sub = None  # 取消订阅更新事件
        if self._window:
            self._window.destroy()
            self._window = None
