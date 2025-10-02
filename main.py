from PyQt5 import uic 
from .ClassWidgets.base import PluginBase, SettingsBase  # 导入CW的基类 
import tempfile 
import os 
import json 
import time 
import sys 

class Plugin(PluginBase):  # 插件类 
    def __init__(self, cw_contexts, method):  # 初始化 
        super().__init__(cw_contexts, method)  # 调用父类初始化方法 
        self.plugin_dir = self.cw_contexts['PLUGIN_PATH'] 
        self.temp_dir = tempfile.gettempdir() 

    def execute(self): 
        pass 

    def listen(self): 
        # 检查是否存在 unread 文件作为信号
        unread_file = os.path.join(self.temp_dir, "SecRandom_unread")
        if os.path.exists(unread_file):
            # 读取 SecRandom_message_received.json 文件
            res_file = os.path.join(self.temp_dir, "SecRandom_message_sent.json")
            
            # 如果 JSON 文件存在，优先处理 JSON 消息
            if os.path.exists(res_file):
                try:
                    with open(res_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    # 删除信号文件，表示已处理
                    os.remove(unread_file)
                    
                    # 根据消息类型处理
                    msg_type = data.get("type", "")
                    
                    if msg_type == "selection_result":
                        # 处理抽选结果
                        name = data.get("name", "未知")
                        display_time = data.get("display_time", 3)
                        time_str = data.get("time", "")
                        
                        # 构建通知内容
                        title = "抽选结果"
                        subtitle = "被抽中的幸运儿"
                        content = f"恭喜 {name}!"
                        
                        # 发送通知
                        self.method.send_notification(
                            state=4,
                            title=title,
                            subtitle=subtitle,
                            content=content,
                            icon=f'{self.plugin_dir}/assets/SecRandom.png',
                            duration=display_time * 1000
                        )
                    
                    elif msg_type == "reward_result":
                        # 处理抽奖结果
                        reward = data.get("reward", "未知奖品")
                        display_time = data.get("display_time", 3)
                        time_str = data.get("time", "")
                        
                        # 构建通知内容
                        title = "抽奖结果"
                        subtitle = "被抽中的奖品是"
                        content = f"恭喜获得 {reward}!"
                        
                        # 发送通知
                        self.method.send_notification(
                            state=4,
                            title=title,
                            subtitle=subtitle,
                            content=content,
                            icon=f'{self.plugin_dir}/assets/SecRandom.png',
                            duration=display_time * 1000
                        )
                    
                    else:
                        # 未知消息类型，尝试显示原始数据
                        display_time = data.get("display_time", 3)
                        self.method.send_notification(
                            state=4,
                            title="收到消息",
                            subtitle="未知类型的消息",
                            content=str(data),
                            icon=f'{self.plugin_dir}/assets/SecRandom.png',
                            duration=display_time * 1000
                        )
                
                except Exception as e:
                    print(f"处理 JSON 消息失败: {e}")

    def update(self, cw_contexts): 
        super().update(cw_contexts) 
        self.listen()
