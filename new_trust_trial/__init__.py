from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'double_trust'
    PLAYERS_PER_GROUP = None      # ← 全員を1人グループにする
    NUM_ROUNDS = 2
    ENDOWMENT = cu(10)
    MULTIPLIER = 3

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    random_id = models.StringField()
    sent_amount = models.CurrencyField(
        min=0, max=C.ENDOWMENT,
        label='送金額を入力してください（0〜10）',
    )
    received_amount = models.CurrencyField()
    sent_back_amount = models.CurrencyField(
        min=cu(0),
        label='返送額を入力してください',
    )
    matched_sender_id = models.StringField()

    # ----------------------------------------
    # アンケートA：A役での送信理由
    # ----------------------------------------
    expected_return_pct = models.IntegerField(
        label='Q1. あなたがA役として送るポイントを決めたとき、'
              'B役の相手はどの程度返してくれると思いましたか。\n'
              '0％＝まったく返してくれないと思った　'
              '100％＝多くを返してくれると思った',
        min=0, max=100
    )
    reason_1 = models.IntegerField(
        label='１. 相手が返してくれるか分からなかったから。',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelect
    )
    reason_2 = models.IntegerField(
        label='２. 相手を信用できないと感じたから。',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelect
    )
    reason_3 = models.IntegerField(
        label='３. 損をする可能性を避けたかったから。',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelect
    )
    reason_4 = models.IntegerField(
        label='４. 自分のポイントを確実に残したかったから。',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelect
    )
    reason_5 = models.IntegerField(
        label='５. 相手が誰であっても、不確実な選択は避けたいから。',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelect
    )
    reason_6 = models.IntegerField(
        label='６. 同じゼミの相手には協力すべきだと思ったから。',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelect
    )
    reason_7 = models.IntegerField(
        label='７. 相手に悪いことをしたくないと感じたから。',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelect
    )
    reason_8 = models.IntegerField(
        label='８. 自分の選択が知られる可能性が気になったから。',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelect
    )
    reason_9 = models.IntegerField(
        label='９. 今後の人間関係に影響するかもしれないと思ったから。',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelect
    )

    # ----------------------------------------
    # アンケートB：リスク選好
    # ----------------------------------------

    risk_invest = models.IntegerField(
        label='Q1. あなたに10ポイントがあります。\n'
              '使ったポイントは、3分の2の確率で失われ、3分の1の確率で2.5倍になります。\n'
              'あなたは何ポイント使いますか。（0～10）',
        min=0, max=10
    )

    risk_donate_willingness = models.IntegerField(
        label='Q2. 見返りを期待せずに、良い目的のために寄付をすることに'
              'どのくらい意欲的ですか？（0〜10）',
        min=0, max=10
    )

    risk_donate_amount = models.IntegerField(
        label='Q3. 想像してください。あなたは思いがけず「10万円」を受け取りました。'
              'あなたはそのうちいくらを寄付しますか？（0円〜10万円）',
        min=0, max=100000
    )

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        used_ids = set()
        for player in subsession.get_players():
            while True:
                new_id = str(random.randint(1000, 9999))
                if new_id not in used_ids:
                    used_ids.add(new_id)
                    player.random_id = new_id
                    break
    else:
        # ラウンド2ではラウンド1のIDを引き継ぐ
        for player in subsession.get_players():
            player.random_id = player.in_round(1).random_id


def assign_amounts(subsession: Subsession):
    """
    ラウンド1の送金額をシャッフルして各プレイヤーに割り当てる。
    同一人物に当たらないよう保証する。
    """
    players = subsession.get_players()
    round1_players = [p.in_round(1) for p in players]

    senders = list(range(len(players)))

    # 完全マッチング：自分に当たらないシャッフル（攪乱順列）
    while True:
        shuffled = senders[:]
        random.shuffle(shuffled)
        # 誰も自分自身に当たっていないか確認
        if all(shuffled[i] != i for i in range(len(players))):
            break

    for i, player in enumerate(players):
        sender = round1_players[shuffled[i]]
        player.received_amount = sender.sent_amount * C.MULTIPLIER
        player.matched_sender_id = sender.random_id

class Introduction(Page):
    def is_displayed(player):
        return player.round_number == 1
    def vars_for_template(player):
        return dict(endowment=C.ENDOWMENT, multiplier=C.MULTIPLIER)

class SendPage(Page):
    form_model = 'player'
    form_fields = ['sent_amount']
    def is_displayed(player):
        return player.round_number == 1
    def vars_for_template(player):      # ← これを追加
        return dict(endowment=C.ENDOWMENT)

class WaitForAssignment(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        assign_amounts(subsession)

    def is_displayed(player):
        return player.round_number == 2

class SendBackPage(Page):
    form_model = 'player'
    form_fields = ['sent_back_amount']

    def is_displayed(player):
        return player.round_number == 2

    def vars_for_template(player):
        return dict(
            received_amount=player.received_amount,
            matched_sender_id=player.matched_sender_id,
            total_amount=player.received_amount + C.ENDOWMENT,  # ← 追加
        )

    def sent_back_amount_max(player):
        return player.received_amount + C.ENDOWMENT  # 受け取った金額＋初期保有額10点

    def error_message(player, values):  # エラーメッセージ
        total = player.received_amount + C.ENDOWMENT
        if values['sent_back_amount'] > total:
            return f'返送額は合計保有額（{total} points）以下にしてください。'

class Results(Page):
    def vars_for_template(player):
        if player.round_number == 1:
            return dict(round=1, sent_amount=player.sent_amount)
        else:
            payoff = C.ENDOWMENT + player.received_amount - player.sent_back_amount
            player.payoff = payoff
            return dict(
                round=2,
                received_amount=player.received_amount,
                sent_back_amount=player.sent_back_amount,
                payoff=payoff,
            )

class Survey(Page):
    form_model = 'player'
    form_fields = [
        'expected_return_pct',
        'reason_1',
        'reason_2',
        'reason_3',
        'reason_4',
        'reason_5',
        'reason_6',
        'reason_7',
        'reason_8',
        'reason_9',
        'risk_invest',
        'risk_donate_willingness',
        'risk_donate_amount',
    ]

    def is_displayed(player):
        return player.round_number == 2  # 最終ラウンドのみ表示

page_sequence = [
    Introduction,
    SendPage,
    WaitForAssignment,
    SendBackPage,
    Results,
    Survey,
]
