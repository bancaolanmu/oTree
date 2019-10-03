from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time
import random


class InstructionExperiment(Page):
    def is_displayed(self):
        return self.round_number == 1

class Prepare(Page):
    form_model = "player"
    form_fields = ['instructions']

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        # user has ret_timer seconds to complete as many pages as possible
        self.participant.vars[
            'expiry_timestamp'] = time.time() + Constants.task_timer

        self.player.total_attempts = 0

class Task(Page):

    form_model = 'player'
    form_fields = ['user_total']

    def get_timeout_seconds(self):
        return self.participant.vars['expiry_timestamp'] - time.time()


    def is_displayed(self):
        return self.participant.vars['expiry_timestamp'] - time.time() > 1

    def before_next_page(self):
        if self.player.user_total != None:
            self.player.score_round()
            self.player.attempt = 1





class Rest(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


    def before_next_page(self):

        player_in_rounds = self.player.in_all_rounds()

        self.player.cumulative_payoff = sum(
            [p.payoff_score for p in player_in_rounds if
             p.payoff_score is not None])
        self.player.cumulative_correct = sum(
            [p.is_correct for p in player_in_rounds if
             p.is_correct is not None])
        self.player.cumulative_attempt = sum(
            [p.attempt for p in player_in_rounds if
             p.attempt is not None])

        if self.player.cumulative_payoff is not None:
            self.participant.vars['total_payoff_1'] = self.player.cumulative_payoff
        else:
            self.participant.vars['total_payoff_1'] = 0


    timeout_seconds = Constants.rest_time


page_sequence = [
    InstructionExperiment,
    Prepare,
    Task,
    Rest,
]
