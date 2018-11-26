"""

            Class for searching the most frequently used simplified chinese characters.

        Contains stroke order gifs, definitions and varaients for most simplified characters.

        use:

            import character_searcher

            cs = CharacterSearcher()
            results = cs.search_character('的')


        data sources:

            https://www.mdbg.net/chinese/dictionary?page=cc-cedict
            http://technology.chtsai.org/charfreq/sorted.html (utf-8)


more about cedict and 'cedict_1_0_ts_utf-8_mdbg.txt':

    >> pip install pycedict

    # download 'cedict_1_0_ts_utf-8_mdbg.txt' from
    #     https://www.mdbg.net/chinese/dictionary?page=cc-cedict
"""

#!/usr/bin/env

__filename__ = "CharacterSearcher.py"
__author__ = "L.J. Brown"


from pathlib import Path
from ast import literal_eval
import itertools

import cedict
import pandas as pd



class CharacterSearcher:
    
    def __init__(self):

        # load dfs
        self.character_frequency_csv_file = "character_searcher/data/character_frequency_dataframes/character_frequency_stroke.csv"
        self.cedict_df_csv_file = 'character_searcher/data/cedict_dataframes/cedict_df.csv'
        self.charcter_gif_file_template = "character_searcher/data/stroke_order_gifs/%s_stoke_order.gif"
        
        tf_data_converters_dict = {
            "frequency": literal_eval,
            "number_of_strokes": literal_eval
        }
        self.top_frequency_df = pd.read_csv(self.character_frequency_csv_file, converters=tf_data_converters_dict)

        #cedict_df = pd.read_csv(cedict_df_csv_file)
        ce_data_converters_dict = {
            "defs": literal_eval,
            "variants": literal_eval,
            "variants_ch": literal_eval,
            "variants_chs": literal_eval
        }
        self.cedict_df = pd.read_csv(self.cedict_df_csv_file,converters=ce_data_converters_dict)

    def search_cedict_character(self, character, simplified=True):
        if simplified:
            top_character_info_df = self.cedict_df.loc[self.cedict_df['chs'] == character]
        else:
            top_character_info_df = self.cedict_df.loc[self.cedict_df['ch'] == character]

        ch = top_character_info_df['ch'].tolist()
        chs = top_character_info_df['chs'].tolist()
        definitions = top_character_info_df['defs'].tolist()
        pinyin = top_character_info_df['pinyin'].tolist()

        variants_ch = top_character_info_df['variants_ch'].tolist()
        variants_chs = top_character_info_df['variants_chs'].tolist()

        # merge lists of lists
        ch = list(itertools.chain.from_iterable(ch))
        chs = list(itertools.chain.from_iterable(chs))
        definitions = list(itertools.chain.from_iterable(definitions))
        variants_ch = list(itertools.chain.from_iterable(variants_ch))
        variants_chs = list(itertools.chain.from_iterable(variants_chs))

        # pinyinize
        computer_pinyin = pinyin
        pinyin = [cedict.pinyinize(p) for p in pinyin]

        # get frequency and strokes if avaible
        searched_character_line_df = self.top_frequency_df.loc[self.top_frequency_df['character'] == character]
        frequency = searched_character_line_df.iloc[0]['frequency']
        number_of_strokes = searched_character_line_df.iloc[0]['number_of_strokes']
        
        # get stroke order gif file
        stroke_order_gif_file = None
        # check if exists
        check_file = Path(self.charcter_gif_file_template % character)
        if check_file.is_file():
            stroke_order_gif_file = self.charcter_gif_file_template % character
        
        
        results = {
            'ch' : ch,
            'chs' : chs,
            'defintions' : definitions,
            'pinyin' : pinyin,
            'computer_pinyin' : computer_pinyin,
            'variants_ch' : variants_ch,
            'variants_chs' : variants_chs,
            'frequency' : frequency,
            'number_of_strokes' : number_of_strokes,
            'stroke_order_gif_file' : stroke_order_gif_file
        }

        return results
 
    def search_character(self, character, simplified=True):
        results = self.search_cedict_character(character, simplified=simplified)

        character_traditional = list(set(results['ch']))[0]
        character_simplified = list(set(results['chs']))[0]
        computer_pinyin = results['computer_pinyin']
        pinyin = results['pinyin']
        variants_ch = results['variants_ch']
        variants_chs = results['variants_chs']
        definitions = results['defintions']
        frequency = results['frequency']
        number_of_strokes = results['number_of_strokes']
        stroke_order_gif_file = results['stroke_order_gif_file']

        search_results = {
            'search_character' : character,
            'character_traditional' : character_traditional,
            'character_simplified' : character_simplified,
            'computer_pinyin' : computer_pinyin,
            'pinyin' : pinyin,
            'variants_traditional' : variants_ch,
            'variants_simplified' : variants_chs,
            'definitions' : definitions,
            'frequency' : frequency,
            'number_of_strokes' : number_of_strokes,
            'stroke_order_gif_file' : stroke_order_gif_file
        }

        return search_results


if __name__ == '__main__':

    # testing
    cs = CharacterSearcher()
    print(cs.search_character('的'))

