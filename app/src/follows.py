from atproto import Client
import os
import traceback
from client import get_client

import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from text import clean_text

DF = pd.DataFrame


class follows():
    def __init__(self):
        self.client = get_client() # init client outside class so that class can be initialized each time
        self.handle = None
        self.follows = None
        self.bios = None

    def set_handle(self, 
                   handle:str
                   )->None:
        
        self.handle = handle

    def get_all_follows(
            self
    )->None:
        if not self.handle:
            raise Exception('No target handle provided')

        try:
            raw_data = self.client.get_follows(actor = self.handle)
        except Exception as e:
            stack_trace = traceback.format_exc()
            raise Exception(f'Failed to get data\nStack trace:\n{stack_trace}')
        
        cursor = raw_data['cursor']
        follows = raw_data['follows']
        while cursor:
            raw_data = self.client.get_follows(actor = self.handle, cursor = cursor)
            follows += raw_data['follows']
            cursor = raw_data['cursor']
        
        self.follows = follows

    def compile_bios_to_DF(
            self,
    ) -> DF:
        if not self.follows:
            raise Exception("Follows data has not been gathered")
        bios = []
        for user in self.follows:
            bios.append(clean_text(user.description))

        self.bios = pd.DataFrame(bios)
    

    def plot_follow_bio_stats(
            self
    ):
        #if not isinstance(self.bios, DF):
        #    raise Exception("Follows bios have not been compiled")
        
        self.bios['len_url'] = self.bios['url'].apply(lambda x: len(set(x)) if type(x) == list else 0)
        self.bios['len_emojis'] = self.bios['emojis'].apply(lambda x: len(set(x)) if type(x) == dict else 0)
        kw_count = pd.Series([ i for j in self.bios['clean_text'].str.lower().str.split().tolist() if j is not None for i in j ]).value_counts()


        fig = plt.figure(figsize  = (12,7))

        ax1 = fig.add_subplot(2,3,1)
        tmp = self.bios['len_url'].apply(lambda x: 'Has URL in Bio' if bool(x) else 'Does not have URL in BIO').value_counts() * 100 / self.bios.shape[0]
        ax1.pie(tmp, labels = tmp.index.tolist(), autopct='%.0f%%', textprops={'fontsize': 8})
        ax1.set_title("% of follows who have urls in bio", fontsize = 10)

        ax2 = fig.add_subplot(2,3,2)
        sns.histplot(data = self.bios, x = 'len_url', stat = 'probability', ax = ax2)
        ax2.set_title('Distribution of # of unique URLs in Bio', fontsize = 10)
        plt.tight_layout()

        ax3 = fig.add_subplot(2,3,4)
        tmp = self.bios['len_emojis'].apply(lambda x: 'Has Emoji in Bio' if bool(x) else 'Does not have Emoji in BIO').value_counts() * 100 / self.bios.shape[0]
        ax3.pie(tmp, labels = tmp.index.tolist(), autopct='%.0f%%', textprops={'fontsize': 8})
        ax3.set_title("% of follows who have Emojis in bio", fontsize = 10)

        ax4 = fig.add_subplot(2,3,5)
        sns.histplot(data = self.bios, x = 'len_emojis', stat = 'probability', ax = ax4)
        ax4.set_title('Distribution of # of unique Emojis in Bio', fontsize = 10)

        ax5 = fig.add_subplot(1,3,3)
        sns.barplot(x = kw_count.head(20).tolist(), y = kw_count.head(20).index.tolist(), ax = ax5)
        ax5.set_title('Keyword Counts of Follows Bios', fontsize = 10)

        fig.suptitle(f'Follows Stats (# of Follows = {self.bios.shape[0]:.0f})')
        plt.tight_layout()
        
        return fig

        
    



    


