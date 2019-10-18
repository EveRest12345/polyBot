import os


# Путь до коренной папки `tele_bot`
BASE_PATH = os.path.dirname(os.path.dirname(__file__))


TG_TOKEN = "790515861:AAHYkyCYf9poK_149xBOH7kELZDSrwtAc3A"

# На сервере не используем прокси-URL
TG_API_URL = None

# Валютная пара для уведомления
NOTIFY_PAIR = "USD-BTC"
# ID чата для уведомлений о курсе BTC
NOTIFY_USER_ID = 720951086

# ID чата для уведомлений о курсе $
USD_NOTIFY_USER_ID = -1001386305123

# ID чата (владельца канала) для получения отзывов/заявок
FEEDBACK_USER_ID = 50512389
