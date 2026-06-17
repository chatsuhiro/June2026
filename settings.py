from os import environ


SESSION_CONFIGS = [
    dict(
        name='guess_two_thirds',
        display_name="Guess 2/3 of the Average",
        app_sequence=['guess_two_thirds', 'payment_info'],
        num_demo_participants=3,
    ),
    dict(
        name='prisoner0514',
        display_name="囚人のジレンマ0514",
        app_sequence=['prisoner0514', 'payment_info'],
        num_demo_participants=2,
    ),
    dict(
        name='survey', app_sequence=['survey', 'payment_info'], num_demo_participants=1
    ),
    dict(
        name='PG3',
        display_name="はじめての公共財ゲーム",
        num_demo_participants=3,
        app_sequence=['publicgoods_trial']
    ),
    dict(
        name = 'UG',
        display_name = "はじめての最終提案ゲーム",
        app_sequence = ['ultimatum_trial'],
        num_demo_participants = 2,
    ),
    dict(
        name='TG',
        display_name="はじめての信頼ゲーム",
        num_demo_participants=2,
        app_sequence=['trust_trial']
    ),
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
    )
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
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '7320314530575'

INSTALLED_APPS = ['otree']
