import pandas as pd
import pypokedex
import PIL.Image, PIL.ImageTk
import tkinter as tk
import urllib3
from io import BytesIO

# filepath of German spreadsheet
german_sheet = pd.read_csv("german-names.csv")

# builds array of German names for Pokémon
german = []
i = 0
x = True
while(x is True):
    try:
        german.append(german_sheet.iloc[i][2])
        i = i+1
    except:
        x = False

# main window
window = tk.Tk()
window.geometry("600x500")
window.title("English-German Pokédex")
# alt background color #910904
bg_color = "#0047ab"
font_color = "#dde2f0"
window.config(padx=10, pady=10, background=bg_color)



# title label
header = tk.Label(window, text="Englisch-Deutscher Pokédex", background=bg_color, fg=font_color)
header.config(font=("Arial", 32))
header.pack(padx=10, pady=10)

# image window
pokeimg = tk.Label(window)
pokeimg.config(font=("Arial", 20), background=bg_color, fg=font_color, text="Image")
pokeimg.pack()

# ID - English name
pokeinfo = tk.Label(window)
pokeinfo.config(font=("Arial", 20), background=bg_color, fg=font_color, text="ID - English")
pokeinfo.pack(padx=10, pady=10)

# German name
lang1name = tk.Label(window)
lang1name.config(font=("Arial", 30), background=bg_color, fg=font_color, text="German")
lang1name.pack(padx=6, pady=6)

# Pokémon type(s)
poketypes = tk.Label(window)
poketypes.config(font=("Arial", 12), background=bg_color, fg=font_color, text="Type 1 - Type 2")
poketypes.pack(padx=2, pady=2)

# load function when lookup is performed
def load_pokemon():
    # clears instructions text
    instructions.destroy()
    isgerman = False
    a = 0

    # lookup in German (this is broken right now)
    for x in german:
        if (text_box.get(1.0, "end-1c").lower().title() == x):
            pokemon = pypokedex.get(name=str(a))
            isgerman = True
        a = a + 1

    # looks up Pokémon in dex
    if (isgerman is False):
        pokemon = pypokedex.get(name=text_box.get(1.0, "end-1c"))

    # pulls image from URL
    http = urllib3.PoolManager()
    response = http.request('GET', pokemon.sprites.front.get('default'))
    image = PIL.Image.open(BytesIO(response.data))

    # displays image
    img = PIL.ImageTk.PhotoImage(image)
    pokeimg.config(image=img)
    pokeimg.image = img

    # displays pokemon info (German text is from array built from spreadsheet)
    pokeinfo.config(text=f"{pokemon.dex} - {pokemon.name}".title())
    lang1name.config(text=f"{german[pokemon.dex-1]}".title())
    poketypes.config(text=" - ".join([t for t in pokemon.types]).title())

    # clears text box
    text_box.delete("1.0","end")

# Instruction text that disappears after first lookup
instructions = tk.Label(window, text="Enter name or ID of a Pokémon to begin".upper())
instructions.config(font=("Roboto", 16), background="black", fg=font_color)
instructions.pack(padx=6, pady=6)

# text box for user input
text_box = tk.Text(window, height=1)
text_box.config(font=("Arial", 20), background="#0968ed", fg=font_color)
text_box.pack(padx=10, pady=10)

button = tk.Button(window, text="Load Pokémon", command=load_pokemon,  activeforeground="#ccd2e0", activebackground="#0968ed", background="#0c4da8", fg=font_color)
button.config(font=("Arial", 20))
button.pack(padx=10, pady=10)

window.mainloop()

