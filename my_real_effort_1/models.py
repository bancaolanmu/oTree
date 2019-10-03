from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Your name here'

doc = """
Real Effort Task: adding three two-digit integers within five minutes
"""


class Constants(BaseConstants):
    name_in_url = 'my_real_effort_1'
    players_per_group = None
    num_rounds = 60
    task_timer = 60
    bonus_per_round = 1
    rest_time = 10
    exchange_rate = 2.5
    show_up = c(10)

    def integer_lists(rounds):
        #creat the integers used in each round
        list_n = []
        for r in range(0, rounds):
            t = [random.randint(10, 99), random.randint(10, 99),
                 random.randint(10, 99)]
            list_n.append(t)
        return list_n

    int_list = integer_lists(num_rounds)


class Subsession(BaseSubsession):

    def before_session_starts(self):
        #real effort task display and answer
        players = self.get_players()
        for p in players:
            p.int1 = Constants.int_list[self.round_number - 1][0]
            p.int2 = Constants.int_list[self.round_number - 1][1]
            p.int3 = Constants.int_list[self.round_number - 1][2]
            p.solution = p.int1 + p.int2 + p.int3





class Group(BaseGroup):
    pass


class Player(BasePlayer):

    def score_round(self):
        #payoffs of players
        if self.solution == self.user_total:
            self.is_correct = 1
            self.payoff_score = Constants.bonus_per_round
        else:
            self.is_correct = 0
            self.payoff_score = 0



    user_total = models.IntegerField(min=0,
                                     max=300,
                                     doc="user's summation",
                                     widget=widgets.NumberInput(attrs={'autocomplete':'off'}))


    instructions = models.IntegerField(min=0,
                                       max=300,
                                       doc="user's summation",
                                       blank=True,
                                       widget=widgets.NumberInput(attrs={'autocomplete':'off'}))

    int1 = models.IntegerField(
        doc="the first int of this round"
    )

    int2 = models.IntegerField(
        doc="the second int of this round"
    )

    int3 = models.IntegerField(
        doc="the third int of this round"
    )

    solution = models.PositiveIntegerField(
        doc="this round's correct summation")

    is_correct = models.IntegerField(
        doc="the answer is correct or not"
    )

    total_attempts = models.IntegerField(
        doc="the answer is correct or not"
    )

    payoff_score = models.FloatField(
        doc="score in this task"
    )

    attempt = models.IntegerField(
        doc="the attempt the user made in this round"
    )

    cumulative_payoff = models.FloatField(
        doc="""The total payoff"""
    )
    cumulative_correct = models.IntegerField(
        doc="""The number of correct answers"""
    )

    cumulative_attempt = models.IntegerField(
        doc="""The number of attempts"""
    )

