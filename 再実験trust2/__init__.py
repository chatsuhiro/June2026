from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = '再実験trust2'
    PLAYERS_PER_GROUP = 2
    # 2人プレイヤー
    NUM_ROUNDS = 1
    # 1期のみ
    ENDOWMENT = cu(10)
    # プレイヤー1の初期保有額は10ポイント
    MULTIPLIER = 3
    # プレイヤー3はポイントを3倍にする


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    give_amount = models.CurrencyField(
        choices = currency_range(cu(0), C.ENDOWMENT, cu(1)),
        # プレイヤー1がプレイヤー2に渡すポイント
        label = 'あなたはプレイヤー2にいくら渡しますか？',
    )
    back_amount = models.CurrencyField(
        # プレイヤー2がプレイヤー1に返すポイント
        label = 'プレイヤー2はプレイヤー1にいくら返しますか？',
    )


class Player(BasePlayer):
    participant_name = models.StringField(
        label="あなたの学籍番号の下4桁を入力してください"
    )


import random


def creating_session(subsession):
    players = subsession.get_players()
    players_A = [p for p in players if p.id_in_group == 1]
    players_B = [p for p in players if p.id_in_group == 2]

    random.shuffle(players_B)

    new_structure = []
    for p_A, p_B in zip(players_A, players_B):
        new_structure.append([p_A, p_B])

    subsession.set_group_matrix(new_structure)


def compute(group: Group):
    p1 = group.get_player_by_id(1)
    # プレイヤー1の情報を取得
    p2 = group.get_player_by_id(2)
    # プレイヤー2の情報を取得
    p1.payoff = C.ENDOWMENT - group.give_amount + group.back_amount
    # プレイヤー1の利得は初期保有額からプレイヤー2に渡したポイントを引いてプレイヤー2から返ってきたポイントを足す
    p2.payoff = group.give_amount * C.MULTIPLIER - group.back_amount
    # プレイヤー2の利得はプレイヤー1から受け取ったポイントをC.MULTIPLIER倍にして，プレイヤー1に返したポイントを引く


def back_amount_choices(group: Group):
    return currency_range(cu(0), cu(group.give_amount * C.MULTIPLIER),
                          cu(1))
    # プレイヤー2が返すポイントの選択肢は0からプレイヤー1から受け取ったポイントをC.MULTIPLIER倍したものまでとします


# PAGES
class SecondWaitPage(WaitPage):
    title_text = "次の実験の準備中"
    body_text = "全員のラウンド１の実験が終了するまで、この画面のまましばらくお待ちください。"

    @staticmethod
    def wait_for_all_groups(subsession):
        return True  # 全員が揃うまで絶対に次へ進ませない


class Page0(Page):
    form_model = 'player'
    form_fields = ['participant_name']


class Page1(Page):
    pass


class Page2(Page):
    form_model = 'group'
    form_fields = ['give_amount']
    # プレイヤー1がプレイヤー2に渡すポイントを入力する


    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
        # プレイヤー1だけがこのページを表示する



class Page3(WaitPage):
    pass


class Page4(Page):
    form_model = 'group'
    form_fields = ['back_amount']
    # プレイヤー2がプレイヤー1に返すポイントを入力する


    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2
        # プレイヤー2だけがこのページを表示する


    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            multi_amount = group.give_amount * C.MULTIPLIER
        )
    # group.give_amountをC.MULTIPLIER倍して，multi_amountとして 画面に表示できるようにする



class Page5(WaitPage):
    after_all_players_arrive = compute
    # 全プレイヤーがこのページに到達したらcompute関数を実行する


class Page6(Page):
    pass

class Page7(Page):
    pass


page_sequence = [SecondWaitPage, Page0, Page1, Page2, Page3, Page4, Page5, Page6, Page7]
