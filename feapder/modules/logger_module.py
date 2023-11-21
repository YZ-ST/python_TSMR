from loguru import logger
import sys
import os
from tabulate import tabulate

# rotation="10 MB" --> 設定日誌文件的大小，超過 10 MB 會自動分割
# rotation="00:00" --> 設定日誌文件的分割時間，每天凌晨 00:00 分割 (log的時間自己需要UTC+8，所以是早上8點才會分割成新的檔案)
# rotation="4s" --> 設定日誌文件的分割時間，每 4 秒分割一次
# retention="7 days" --> 設定日誌文件的保留時間，只保留最近 7 天的日誌
# retention="1 min" --> 設定日誌文件的保留大小，只保留最近 1分鐘的日誌


# ANSI 顏色代碼
class Colors:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    BRIGHT_RED = "\033[91m"
    RESET = "\033[0m"

# 根據日誌級別返回相應的顏色
def get_color(level):
    return {
        "TRACE": Colors.CYAN,
        "DEBUG": Colors.BLUE,
        "INFO": Colors.GREEN,
        "SUCCESS": Colors.MAGENTA,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
        "CRITICAL": Colors.BRIGHT_RED,
    }.get(level, Colors.RESET)

# 定義一個自定義的日誌格式函數
def table_format(record):
    headers = ["Time", "Level", "Message"]
    level_color = get_color(record["level"].name)
    colored_level = f"{level_color}{record['level'].name}{Colors.RESET}"
    colored_message = f"{level_color}{record['message']}{Colors.RESET}"
    data = [[record["time"].strftime("%Y-%m-%d %H:%M:%S"), colored_level, colored_message]]
    return tabulate(data, headers=headers, tablefmt="grid")


# 配置 logger 使用自定義的格式
logger.remove()                           # 移除默認的輸出(這個一定要加，不然會有重複輸出)
logfile = "logs/{time:YYYYMMDD}.log"
logger.add(
    sink=os.path.join(logfile),
    rotation='00:00',                     # 每天凌晨00:00分割(要自己換算成UTC+8)
    retention='30 days',                  # 最长保留30天
    format=table_format,                  # 日志显示格式
    compression="zip",                    # 压缩形式保存
    encoding='utf-8',                     # 编码
    level='DEBUG',                        # 日志级别
    enqueue=True,                         # 默认是线程安全的，enqueue=True使得多进程安全
)
logger.add(sys.stdout, colorize=True, format=table_format)



logger.trace("這是一條追蹤日誌")
logger.debug("這是一條除錯日誌")
logger.info("這是一條信息日誌")
logger.success("這是一條成功日誌")
logger.warning("這是一條警告日誌")
logger.error("這是一條錯誤日誌")
logger.critical("這是一條關鍵日誌")