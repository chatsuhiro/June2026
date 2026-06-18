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
