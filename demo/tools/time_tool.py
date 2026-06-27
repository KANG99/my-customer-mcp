from datetime import datetime
from zoneinfo import ZoneInfo


def get_time(timezone: str = "UTC") -> str:
    """获取指定时区的当前时间。

    Args:
        timezone: IANA 时区名称，默认为 UTC（时区名称例如 Asia/Shanghai、America/New_York）。

    Returns:
        格式化后的时间字符串，如 "Current time (Asia/Shanghai): 14:09:14"。
     """
    return f"Current time ({timezone}): {datetime.now(ZoneInfo(timezone)).strftime('%H:%M:%S')}"
