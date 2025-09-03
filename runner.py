import ast
import csv
import json
from pathlib import Path
import sys
from typing import Iterable
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

from ScrollableFrame import ScrollableFrame

def clean_df(df: pd.DataFrame):
    df = df.drop(labels = [
    'content_warning', 'defense', 'mtgo_id', 'arena_id', 'cardmarket_id', 'lang', 'printed_type_line', 'printed_text', 'life_modifier', 'hand_modifier',
'attraction_lights', 'color_indicator', 'layout', 'flavor_name',
    'loyalty', 'preview.previewed_at', 'frame_effects', 'highres_image', 'card_faces', 'preview.source', 'preview.source_uri', 'security_stamp', 'released_at', 'tcgplayer_etched_id', 'variation_of',
    'frame', 'full_art', 'artist', 'variation', 'reprint', 'promo', 
    'edhrec_rank', 'penny_rank', 'power', 'toughness', 'printed_name', 'related_uris.tcgplayer_infinite_articles',
    'related_uris.tcgplayer_infinite_decks', 'related_uris.gatherer', 'prices.eur', 'prices.eur_foil', 'prices.tix',
    'legalities.predh', 'legalities.alchemy', 'legalities.oldschool', 'legalities.oathbreaker', 'legalities.standard', 'legalities.commander',
    'legalities.brawl', 'legalities.alchemy', 'legalities.paupercommander', 'legalities.standardbrawl', 'legalities.penny',
    'legalities.pioneer', 'legalities.modern', 'legalities.vintage', 'legalities.historic', 'legalities.future',
    'digital', 'border_color', 'textless', 'booster', 'story_spotlight', 'card_back_id', 'artist_ids', 'illustration_id',
    'image_uris.normal', 'image_uris.large', 'image_uris.png', 'image_uris.art_crop', 'image_uris.border_crop',
    'legalities.timeless', 'legalities.gladiator', 'legalities.legacy', 'legalities.pauper', 'legalities.duel', 'legalities.premodern',
    'scryfall_set_uri', 'set_name', 'set_type', 'set_uri', 'set_search_uri', 'rulings_uri', 'produced_mana', 'games', 'oracle_text', ''
    'flavor_text', 'promo_types', 'watermark', 'prints_search_uri', 'foil', 'nonfoil', 'oversized', 'cmc', 'mana_cost', 'image_status', 'uri', 'scryfall_uri', 'object', 'multiverse_ids', 'tcgplayer_id', 'oracle_id',
    'mtgo_foil_id', 'purchase_uris.cardhoarder', 'purchase_uris.tcgplayer', 'purchase_uris.cardmarket',
    'related_uris.edhrec','all_parts', 'id', 'color_identity',
    'reserved', 'finishes', 'game_changer', 'keywords', 'type_line', 'prices.usd_foil', 'prices.usd_etched', 'image_uris.small'], axis =1)
    return df
# CHANGE THIS TO YOUR PATH
# DATA_PATH = Path('D://Repos/data/cards.json')
# with open(DATA_PATH, 'r',  encoding='utf-8') as in_file:
#     cards = json.load(in_file)

# card_df = pd.json_normalize(cards)

# df = clean_df(card_df)
# print(df.columns)
# df.to_csv('cards.csv')
df = pd.read_csv('cards.csv')   
# print(pd.json_normalize(cards))
# sys.exit(0)

def mapping(color: list):
    if isinstance(color, str):
        try:
            color = ast.literal_eval(color)
        except Exception:
            color = []
    match color:
        case []:
            return 0
        case ['W']:
            return 1
        case ['U']:
            return 2
        case ['B']:
            return 3
        case ['R']:
            return 4
        case ['G']:
            return 5
        case _:
            return 6
df['color_enum'] = df['colors'].map(mapping)
df.sort_values(['color_enum', 'name'], inplace = True)

def clear_results():
    for widget in results_frame.scrollable_frame.winfo_children():
        widget.destroy()
    current_rows.clear()
    row_vars.clear()

def show_results(df_matches: pd.DataFrame):
    clear_results()
    global current_rows, row_vars
    
    current_rows = df_matches.to_dict('records')
    row_vars = []

    for r_index, row in enumerate(df_matches.itertuples(index=False)):
  

        # ── Row name label ────────────────────────────────
        lbl = ttk.Label(results_frame.scrollable_frame, text=row.name, width=15)
        lbl.grid(row=r_index, column=1, sticky='w', padx=5, pady=2)

        # ──  5 radiobuttons (0‑4) ────────────────────────
        option_var = tk.IntVar(value=0)    # default 0
        for btn_val in range(5):
            rb = ttk.Radiobutton(
                results_frame.scrollable_frame,
                text=str(btn_val),
                variable=option_var,
                value=btn_val
            )
            rb.grid(row=r_index, column=2 + btn_val, padx=2, pady=2)
        for i in range(6):    
            results_frame.scrollable_frame.columnconfigure(i, weight=0) 
        # store the state objects for later use
        row_vars.append({
            'option':   option_var
        })
def on_search():
    q = search_entry.get().strip()
    if not q:
        messagebox.showwarning("Input needed", "Enter a set code.")
        return
    mask = df['set'] == str.lower(q)
    matches = df[mask]
    if matches.empty:
        messagebox.showinfo("No match", f"No rows matched '{q}'.")
        clear_results()
    else:
        show_results(matches)

# -----------------------------------------------------------
# Submit button callback – processes *all selected* rows
# -----------------------------------------------------------
def on_submit():
    expensive_cards = []
    cheap_cards = []
    for r, var in zip(current_rows, row_vars):
        if opt := var['option'].get():        # only process if checked
            row_series = pd.Series(r)
            if float(row_series.get('prices.usd')) < 1:
                cheap_cards.append([opt , row_series.get("name").replace('\'', '').replace('"', ''), f'[{row_series.get("set").upper()}]', row_series.get("collector_number")])
            else:
                expensive_cards.append([opt , row_series.get("name").replace('\'', '').replace('"', ''), f'[{row_series.get("set").upper()}]', row_series.get("collector_number")])
    print(expensive_cards)
    messagebox.showinfo("Done", f"All {len(expensive_cards) + len(cheap_cards)} cards have been processed.")
    with open(f'{row_series.get("set")}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', doublequote=False)
        writer.writerows(cheap_cards)
        writer.writerow(['', '', '', ''])
        writer.writerows(expensive_cards)









if __name__ == '__main__':
    

    root = tk.Tk()
    root.title("Card Selector")

    search_lbl = ttk.Label(root, text="Set Code:")
    search_lbl.grid(row=0, column=0, sticky='w', padx=5, pady=5)

    search_entry = ttk.Entry(root, width=30)
    search_entry.grid(row=0, column=1, columnspan=3, sticky='we', padx=5, pady=5)

    search_btn = ttk.Button(root, text="Set Code")
    search_btn.grid(row=0, column=4, padx=5, pady=5)

    results_frame = ScrollableFrame(root)
    results_frame.grid(row=1, column=0, columnspan=5, sticky='nsew', padx=5, pady=5)
    root.rowconfigure(1, weight=1)
    for col in range(5):
        root.columnconfigure(col, weight=1)
    # root.rowconfigure(1, weight=1)
    # root.columnconfigure(0, weight=1)   # all other columns inherit the weight from the span    

    # keep a reference to the rows that are currently shown
    current_rows = []          # list of dicts (one per row)
    row_vars = []              # list of dicts with 'selected', 'option', etc.

    submit_btn = ttk.Button(root, text="Submit")
    submit_btn.grid(row=0, column=5, columnspan=5, pady=10)

    search_btn.config(command=on_search)
    submit_btn.config(command=on_submit)

    root.mainloop()
