# 第 4 步：logging 基础
import logging  # 导入日志模块：logging 是 Python 自带的「记日记」工具，专门给程序写运行记录

# 配置日志：级别 + 格式（时间 | 级别 | 消息）
logging.basicConfig(  # 一次性配置日志的「总开关」，只需设置一次，整个程序生效
    filename="app.log",  # 日志写进 app.log 文件（而不是打印到屏幕），方便事后翻查
    level=logging.INFO,  # 记录 INFO 及以上级别；DEBUG 比 INFO 低，会被过滤掉
    format="%(asctime)s | %(levelname)s | %(message)s"  # 每行日志的格式：时间 | 级别 | 内容
)  # 配置结束，后面的 logging.xxx 都会按这套规则写日志

logging.debug("这是DEBUG:最啰嗦的细节")  # DEBUG：最啰嗦的细节日志，因为级别低于 INFO，本例不会写进文件
logging.info("程序开始运行了")  # INFO：普通信息，程序正常运行的消息，会写进 app.log
logging.warning("警告：文件快满了")  # WARNING：警告，还没出错但要引起注意，会写进 app.log
logging.error("出错啦！文件读不了")  # ERROR：出错啦，程序还能继续跑，但要记下这笔账，会写进 app.log
logging.critical("崩溃了！救命啊")  # CRITICAL：最严重的级别，程序要崩溃了，会写进 app.log
