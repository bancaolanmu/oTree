from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time
import random


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.subsession.do_my_shuffle()


class Estimation(Page):
    form_model = 'player'
    form_fields = ['absolute_r', 'relative_r']

    def before_next_page(self):
        self.player.rank_round()
        self.player.est_correct = 0
        self.participant.vars['estimate_3'] = 0

        if self.timeout_happened:
            self.player.relative_r = -10
            self.player.relative_r = -10
        else:
            difference = abs(self.player.relative_r-self.player.better_session)

            if difference <= 5:
                self.player.est_correct = 1-difference*0.2
                self.participant.vars['estimate_3'] = Constants.est_reward-difference*Constants.est_cost

        self.player.participant_est3_dump = str(self.participant.vars['estimate_3'])
        # self.player.participant.payoff = c(
        #     self.player.participant.vars['total_payoff_3'] + self.participant.vars['estimate_3'])


        self.participant.vars['m'] = self.group.m
        self.participant.vars['manager_letter'] = self.group.manager_letter
        self.participant.vars['per_distance'] = self.group.per_distance




page_sequence = [
    ResultsWaitPage,
    Estimation,
]
