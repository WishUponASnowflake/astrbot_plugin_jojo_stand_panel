"""
本文档由AI生成

UI文本资源文件，用于存储所有用户界面文本，实现代码与文本的分离
"""


class UITexts:
    """UI文本资源类"""

    # 觉醒替身处理器相关文本
    AWAKEN_SYSTEM_DISABLED = "❌ 觉醒系统已被管理员禁用！"

    AWAKEN_STAND_HELP = """📚 觉醒替身使用方法：
/觉醒替身

💡 说明：
- 系统将为你随机生成一个替身
- 包括随机的名字和能力值
- 每人每天只能觉醒一次

⚠️ 注意：每人每天只能觉醒一次"""

    AWAKEN_STAND_EXISTS = "🌱 你已经有替身了！如需重新觉醒，请使用 /重新觉醒"

    AWAKEN_STAND_SUCCESS = """🌟 替身觉醒成功！

{stand_info}

⏰ 觉醒时间：{awaken_time}

🎆 恭喜你获得了属于自己的替身！
{limit_hint}"""

    REAWAKEN_STAND_NO_EXISTING = (
        "🌱 你还没有替身，请使用 /觉醒替身 来获得你的第一个替身！"
    )

    REAWAKEN_STAND_SUCCESS = """🔥 替身重新觉醒成功！

🆕 新替身名：{stand_name}

🔋 新能力值：
{abilities}

⏰ 觉醒时间：{awaken_time}

🎆 你的替身已经进化，获得了全新的力量！
{limit_hint}"""

    # 基础处理器相关文本
    GROUP_NOT_IN_WHITELIST = "群聊不在白名单中: {group_id}"

    # 自定义替身处理器相关文本
    SET_STAND_DISABLED = "❌ 设置替身指令已被管理员禁用！"

    SET_STAND_HELP = """📚 设置替身使用方法：
/设置替身 <六个能力值> [替身名字]

💡 能力值格式：
- 使用A-E表示能力等级
- 必须输入恰好6个能力值
- 只支持直接连写格式，如：AAAAEE

📝 示例：
/设置替身 AABCDE
/设置替身 ABCDEE 白金之星
/设置替身 AAAAAA 钻石之星

👁️ 设置后可以使用 /我的替身 来查看你的替身面板"""

    SET_STAND_INVALID_ABILITIES = """❌ 能力值格式错误！

请输入恰好6个能力值（A-E），例如：
✅ AABCDE
✅ ABCDEE
✅ AAAAAA

当前输入无法识别为有效的6个能力值。"""

    SET_STAND_SUCCESS_WITH_NAME = "✅ 替身设置成功！\n替身名字：{stand_name}\n能力值：{abilities}\n\n使用 /我的替身 查看面板图片"

    SET_STAND_SUCCESS_WITHOUT_NAME = (
        "✅ 替身设置成功！\n能力值：{abilities}\n\n使用 /我的替身 查看面板图片"
    )

    CREATE_STAND_HELP = """📚 替身面板使用方法：
/替身 <六个能力值> [名字]

💡 能力值格式：
- 使用A-E表示能力等级
- 必须输入恰好6个能力值
- 只支持直接连写格式，如：AAAAEE

📝 示例：
/替身 AABCDE
/替身 ABCDEE 我的替身
/替身 AAAAAA 超级替身"""

    CREATE_STAND_INVALID_ABILITIES = """❌ 能力值格式错误！

请输入恰好6个能力值（A-E），例如：
✅ AABCDE
✅ ABCDEE
✅ AAAAAA

当前输入无法识别为有效的6个能力值。"""

    CREATE_STAND_SUCCESS_WITH_NAME = (
        "✨ 为 {stand_name} 创建的替身面板：\n\n能力值：\n{abilities}"
    )

    CREATE_STAND_SUCCESS_WITHOUT_NAME = "✨ 你创建的替身面板：\n\n能力值：\n{abilities}"

    # 随机替身处理器相关文本
    RANDOM_STAND_COOLDOWN = (
        "❌ 随机替身功能冷却中！\n\n{cooldown_info}\n\n⏰ 冷却时间结束后可再次使用"
    )

    RANDOM_STAND_RESULT = "🎲 你抽到的随机替身面板：\n\n能力值：\n{abilities}"

    TODAY_STAND_RESULT = "📅 你今日的替身面板：\n\n能力值：\n{abilities}"

    # 用户替身处理器相关文本
    MY_STAND_NO_STAND = """❌ 你还没有设置替身！

🔄 发送 /觉醒替身 来随机生成你的替身
🔧 发送 /设置替身 <能力值> [名字] 来设置你的专属替身
📝 例如：/设置替身 AABCDE 白金之星"""

    MY_STAND_WITH_NAME = """🌟 你的替身：{stand_name}

能力值：
{abilities}

获得方式：{acquisition_method}
设置时间：{created_at}"""

    MY_STAND_WITHOUT_NAME = """🌟 你的替身面板

能力值：
{abilities}

获得方式：{acquisition_method}
设置时间：{created_at}"""

    VIEW_STAND_DISABLED = "❌ 他的替身指令已被管理员禁用！"

    VIEW_STAND_HELP = """📚 查看替身使用方法：
/他的替身 @用户
或
/他的替身 <用户ID>

📝 示例：
- 在群聊中@某人：/他的替身 @张三
- 直接输入用户ID：/他的替身 123456789

⚠️ 注意：只能查看已设置替身的用户"""

    VIEW_STAND_NO_STAND = "❌ {user_name} 还没有设置替身！\n\n💡 用户可以使用 /设置替身 <能力值> [名字] 来设置专属替身"

    VIEW_STAND_WITH_NAME = """🔍 {user_name} 的替身：{stand_name}

能力值：
{abilities}

获得方式：{acquisition_method}
设置时间：{created_at}"""

    VIEW_STAND_WITHOUT_NAME = """🔍 {user_name} 的替身面板

能力值：
{abilities}

获得方式：{acquisition_method}
设置时间：{created_at}"""

    # 觉醒次数限制相关文本
    AWAKEN_LIMIT_EXCEEDED = """❌ 今日觉醒次数已用完！

你今天已经重新觉醒过了（{last_awaken_time}）
每天只能重新觉醒 {daily_limit} 次，请明天（{tomorrow}）再来尝试！"""
