from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import generator
import scorer

# -------------------------------- INITIALIZE RESOURCES ----------------------------------- #

# use generator.py module to get the paragraph-to-type from an API
paragraph_to_type = generator.get_paragraph()

# get the local high score from the .txt file
with open("resources/high_score.txt", mode="r") as text_file1:
    high_score = float(text_file1.read())

# initializes a variable to be used for the typing test "clock"
time_start = None

# initialize Tkinter window
window = Tk()
window.title("Typing Speed Test")
window.config(padx=70, pady=70)


# -------------------------------- FUNCTIONS ----------------------------------- #

# key press bind function - for when player starts typing anything in the text box
def key_func(event):
    global time_start
    # start the player "clock"
    time_start = datetime.now()
    window.unbind('<KeyPress>')


# "return" key press bind function - for when player finishes typing and effectively submits attempts
def return_func(event):
    global time_start
    # end the player "clock"
    time_end = datetime.now()

    # stops the player from typing anything else
    paragraph_entry.config(state=DISABLED)
    window.unbind('<Return>')

    # get the values from the displayed API paragraph and the player's paragraph
    player_entry = paragraph_entry.get("1.0", END).strip()
    check_entry = to_type_paragraph_label.get("1.0", END).strip()
    # get the time on the "clock" between start of key press and "return" key
    total_secs_elapsed = (time_end - time_start).total_seconds()
    # use module scorer.py to get the wpm, accuracy, score, and rank (in a dict form) based on performance
    player_values = scorer.score_check(
        correct_version=check_entry,
        to_check=player_entry,
        secs_elapsed=total_secs_elapsed)

    # change the Tkinter labels to reflect performance on latest round
    your_speed.config(text=f'Your Speed: {player_values["wpm"]} WPM')
    your_accuracy.config(text=f'Your Accuracy: {player_values["accuracy"]}')
    your_score.config(text=f'Your Score: {"{:.1f}".format(player_values["score"])}')
    your_rank.config(text=f'Your Rank: {player_values["rank"]}')

    # update the high score file and label if necessary
    if player_values["score"] > high_score:
        with open(file="resources/high_score.txt", mode="w") as text_file2:
            text_file2.write("{:.1f}".format(player_values["score"]))
        high_score_label.config(text=f'High Score: {"{:.1f}".format(player_values["score"])}')

# monitor the return key and any other key for start of player "clock"
window.bind('<Return>', return_func)
window.bind('<KeyPress>', key_func)


# if the "new paragraph" Tkinter button is clicked, refresh the label values and re-bind the keys
def new_paragraph():
    paragraph_entry.config(state=NORMAL)
    paragraph_entry.delete('1.0', END)
    to_type_paragraph_label.config(state=NORMAL)
    to_type_paragraph_label.delete('1.0', END)
    to_type_paragraph_label.insert(END, generator.get_paragraph())
    to_type_paragraph_label.config(state=DISABLED)

    your_speed.config(text="Your Speed:")
    your_accuracy.config(text="Your Accuracy:")
    your_score.config(text="Your Score:")
    your_rank.config(text=f"Your Rank:")

    window.bind('<Return>', return_func)
    window.bind('<KeyPress>', key_func)


# -------------------------------- UI SETUP ----------------------------------- #

# initial labels
title_label = Label(text="Typing Speed Test", font=("Courier", 40, "italic"))
title_label.grid(column=0, columnspan=2, row=0)

high_score_label = Label(text=f'High Score: {"{:.1f}".format(high_score)}', font=("Courier", 18, "normal"))
high_score_label.grid(column=0, columnspan=2, row=1)

# rabbit picture
canvas = Canvas(width=200, height=200)
rabbit_image = Image.open("resources/rabbit.png")
rabbit_image = rabbit_image.resize((150, 150))
rabbit_image = ImageTk.PhotoImage(rabbit_image)
canvas.create_image(100, 100, image=rabbit_image)
canvas.grid(column=0, columnspan=2, row=2)

to_type_title_label = Label(text="Paragraph to Type:", font=("Courier", 18, "normal"))
to_type_title_label.grid(column=0, row=3, sticky="W", pady=(0, 10))

frame1 = Frame(window, width=600, height=100)
frame1.grid(column=0, columnspan=2, row=4)

to_type_paragraph_label = Text(frame1, bg="white", fg="midnightblue", wrap=WORD, font=("Courier", 16, "normal"))
to_type_paragraph_label.insert(END, paragraph_to_type)
to_type_paragraph_label.config(state=DISABLED)
to_type_paragraph_label.place(width=600, height=100)

type_here_label = Label(text="Type Here (hit <return> when finished):", font=("Courier", 18, "normal"))
type_here_label.grid(column=0, row=5, sticky="W", pady=(10, 10))

# player text entry
frame2 = Frame(window, width=600, height=100)
frame2.grid(column=0, columnspan=2, row=6)

paragraph_entry = Text(frame2, wrap=WORD, font=("Courier", 16, "normal"))
paragraph_entry.place(width=600, height=100)

# endgame labels
your_speed = Label(text="Your Speed:", font=("Courier", 18, "normal"))
your_speed.grid(column=0, row=7, sticky="W", pady=(10, 0))

your_accuracy = Label(text="Your Accuracy:", font=("Courier", 18, "normal"))
your_accuracy.grid(column=0, row=8, sticky="W")

your_score = Label(text="Your Score:", font=("Courier", 18, "bold"))
your_score.grid(column=0, row=9, sticky="W", pady=(20, 0))

your_rank = Label(text="Your Rank:", font=("Courier", 18, "bold"))
your_rank.grid(column=0, row=10, sticky="W")

# "new paragraph" button
new_round = Button(text="New Paragraph", command=new_paragraph, width=15, height=1, font=("Courier", 18, "normal"))
new_round.grid(column=1, row=7, pady=(10, 0))


# keep program open
window.mainloop()
