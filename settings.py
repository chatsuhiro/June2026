from os import environ


SESSION_CONFIGS = [
    dict(
        name='AG',
        display_name="再実験A",
        num_demo_participants=30,
        app_sequence=['再実験trust1','再実験trust2']
    ),
    dict(
        name='BG',
        display_name="再実験B",
        num_demo_participants=30,
        app_sequence=['再実験trust1','再実験trust3']
    ),
    dict(
        name='new_trust_trial',
        display_name='信頼ゲーム（再実験）',
        app_sequence=['new_trust_trial'],
        num_demo_participants=11,
    ),
    dict(
        name='new2_trust_trial',
        display_name='信頼ゲーム（名前付き）',
        app_sequence=['new2_trust_trial'],
        num_demo_participants=11,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ja'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    # ==== 【前半戦】信頼ゲームの同時実施用ルーム ====
    dict(
        name='room_trust_trial',
        display_name='1. 信頼ゲーム（再実験）用ルーム',
        # 必要に応じて、あらかじめ準備している学籍番号リストなどを指定（なければ削ってOK）
        # participant_label_file='_rooms/students.txt', 
    ),
    dict(
        name='room_name_trial',
        display_name='2. 信頼ゲーム（名前付き）用ルーム',
    ),

    # ==== 【後半戦】再実験A・Bの同時実施用ルーム ====
    dict(
        name='room_saizikken_a',
        display_name='3. 再実験A（AG）用ルーム',
    ),
    dict(
        name='room_saizikken_b',
        display_name='4. 再実験B（BG）用ルーム',
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '7320314530575'

INSTALLED_APPS = ['otree']
