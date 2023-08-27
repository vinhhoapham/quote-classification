from torch.utils.data import Dataset
from nltk import word_tokenize, download
import torch
import pandas as pd
from random import sample
import contractions

download('punkt')


def clean_quote(quote):
    quote = contractions.fix(quote)
    quote = quote.replace('""', "'")
    quote = quote.replace('"', "'")
    quote = quote.replace("“", "'").replace("”", "'")
    quote = quote.replace("``", "'").replace("''", "'")
    
    quote = quote.replace('"', " ")
    quote = quote.replace("&", "and")
    return quote

def tokenize(quote, word_embedder, device):
    quote = clean_quote(quote)
    tokens = word_tokenize(quote.lower())
    tokens = torch.stack([word_embedder[word] for word in tokens if word in word_embedder.stoi]).to(device)
    return tokens

def swap_keys_values(d):
    return {value: key for key, value in d.items()}

class QuotesDataset(Dataset):

    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.quotes = []
        self.categories = []

        unique_categories = set(';'.join(self.data['categories']).split(';'))
        self.category_to_idx = {category: index for index, category in enumerate(unique_categories)}
        self.idx_to_category = swap_keys_values(self.category_to_idx)


    def tokenized(self, embedder):
        for index, row in self.data.iterrows():
            quote = row['text']
            category_list = row['categories'].split(';')

            one_hot_category = torch.zeros(len(self.category_to_idx)).to(device)
            for category in category_list:
                one_hot_category[self.category_to_idx[category]] = 1

            self.quotes.append(tokenize(quote, embedder))
            self.categories.append(one_hot_category)

    def __len__(self):
        return len(self.quotes)

    def __getitem__(self, idx):
        return self.quotes[idx], self.categories[idx]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        display_str = ""
        num_of_samples_to_display = 10
        sample_data = sample(list(self.data.iterrows()), num_of_samples_to_display)

        for _, row in sample_data:
            display_str += f"{row['categories']}: {row['text']}\n"

        display_str += f"\nThis dataset has {len(self.quotes)} quotes"
        return display_str






