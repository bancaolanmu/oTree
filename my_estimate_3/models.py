from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from random import randint
import math

author = 'Nanxu Su'
doc = """
Real Effort Task: adding three two-digit integers within five minutes
"""


class Constants(BaseConstants):
    name_in_url = 'my_estimate_3'
    num_rounds = 1
    bonus_per_round = 1
    players_per_group = 4
    exchange_rate = 4
    show_up = c(10)
    est_reward = 1.25
    est_cost = 0.25
    est_time = 210




class Subsession(BaseSubsession):

    def do_my_shuffle(self):
        # Save the performance data from the previous section into a dictionary
        pla_perf_pair = {}
        totaln = self.get_players()
        for pla in totaln:
            pla.participant.vars['a'] = pla.participant.vars['total_payoff_1']+\
                                        pla.participant.vars['total_payoff_2']+\
                                        pla.participant.vars['total_payoff_3']
            pla_perf_pair[pla.id_in_subsession] = pla.participant.vars['a']
            pla.n = len(totaln) - 1


        # b_sorted = [(k, b[k]) for k in sorted(b, key=b.get, reverse=True)]
        sorted_players = sorted(pla_perf_pair, key=pla_perf_pair.get, reverse=True)

        # make group matrix for it
        group_matrix = []
        ppg = Constants.players_per_group

        for i in range(0, len(sorted_players), ppg):
            group_matrix.append(sorted_players[i:i + ppg])

        self.set_group_matrix(group_matrix)
        self.session.vars['group_matrix'] = group_matrix

        # matrix = self.session.vars['group_matching']
        # self.set_group_matrix(matrix)
        for gro in self.get_groups():
            roles = ['H', 'Z', 'O', 'K']
            players = gro.get_players()
            gro.m = randint(1, 4)  # assign manager
            per_group = []

            for count, pla in enumerate(players):
                pla.role_letter = roles[count]
                pla.participant.vars['role_letter'] = pla.role_letter

                if pla.id_in_group == gro.m:
                    gro.manager_letter = pla.role_letter

                per_group.append(pla.participant.vars['a'])

            gro.per_distance = math.ceil(max(per_group) - min(per_group))



class Group(BaseGroup):

    manager_letter = models.StringField(
        doc="""label of the manager"""
    )

    per_distance = models.FloatField(
        doc="""The average performance distance with other group members."""
    )

    m = models.IntegerField(
        doc="""who is the manager"""
    )
class Player(BasePlayer):

    def rank_round(self):
        # performance rankings of players
        self.better_session = 0
        for p in self.subsession.get_players():
            if p.participant.vars['total_payoff_3'] > self.participant.vars['total_payoff_3']:
                self.better_session += 1


    absolute_r = models.IntegerField(min=0,
                                     max=100,
                                     doc="user's beliefs about their absolute performance",
                                     widget=widgets.NumberInput(attrs={'autocomplete':'off'}))

    relative_r = models.IntegerField(min=0,
                                     max=32,
                                     doc="user's beliefs about their relative performance",
                                     widget=widgets.NumberInput(
                                         attrs={'autocomplete': 'off'}),
                                     )

    n = models.IntegerField(
        doc="how many people play with the participant"
    )
    est_correct = models.FloatField(
        doc="estimation correct or not"
    )

    better_session = models.IntegerField(
        doc="""how many players in the session is better than this player"""
    )

    cumulative_payoff = models.FloatField(
        doc="""The total payoff"""
    )
    cumulative_correct = models.IntegerField(
        doc="""The number of correct answers"""
    )


    participant_est3_dump = models.StringField(
        doc="""show the data saved across apps"""
    )

    manager_dump = models.IntegerField(
        doc="""show who the manager is"""
    )

    role_letter = models.StringField(
        doc="""labels of players"""
    )