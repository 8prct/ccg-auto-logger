import tkinter as tk
from tkinter import ttk, messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def fetch_attendees_from_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)
    sheet = client.open('Mado Task Spreadsheet').sheet1  
    attendees = sheet.col_values(2)[5:]  
    return [name for name in attendees if name]  
attendees = fetch_attendees_from_google_sheets()

activities = [
    "1v1s","2v2s", "Free For All (FFA)", "Gladiators", "Boss Rush",
   "Juggernaut", "Hide and Seek","Team Deathmatch"
]


root = tk.Tk()
root.title("CCG Training Report Generator")


current_page = 1
selected_attendees = []


def generate_report():
    selected_activities = [activity1_combobox.get(), activity2_combobox.get(), activity3_combobox.get()]

    if not selected_attendees or not all(selected_activities):
        messagebox.showerror("Error", "Please select attendees and all three activities.")
        return

    report = f"Attendees: \n{', '.join(selected_attendees)}\n=============================\n"

    for i, activity in enumerate(selected_activities, 1):
        report += f"{i}. Activity: {activity}\n"

        if activity == "Free For All (FFA)":
            first_round_winner = ffa_first_round_entry.get()
            second_round_winner = ffa_second_round_entry.get()

            if not first_round_winner or not second_round_winner:
                messagebox.showerror("Error", "Please fill in both FFA round winners.")
                return

            report += f"First round: {first_round_winner}\nSecond round: {second_round_winner}\n"

        elif activity == "1v1s":
            for i, match in enumerate(onevone_matches):
                score = match.get()
                player1 = onevone_frame.winfo_children()[i].winfo_children()[0].get() 
                player2 = onevone_frame.winfo_children()[i].winfo_children()[2].get() 
                if not player1 or not player2 or not score:
                    messagebox.showerror("Error", "Please complete all 1v1 match details.")
                    return
                try:
                    int(score.split('-')[0])
                    int(score.split('-')[1])
                except ValueError:
                    messagebox.showerror("Error", "Invalid score format. Please use 'number-number' (e.g., 2-1)")
                    return

                report += f"{player1} vs {player2} | {score}\n"
        
        elif activity == "2v2s":
            for i, match in enumerate(twovtwo_matches):
                score = match.get()
                player1_2 = twovtwo_frame.winfo_children()[i].winfo_children()[0].get() 
                player2_2 = twovtwo_frame.winfo_children()[i].winfo_children()[2].get() 
                if not player1_2 or not player2_2 or not score:
                    messagebox.showerror("Error", "Please complete all 1v1 match details.")
                    return
                try:
                    int(score.split('-')[0])
                    int(score.split('-')[1])
                except ValueError:
                    messagebox.showerror("Error", "Invalid score format. Please use 'number-number' (e.g., 2-1)")
                    return

                report += f"{player1_2} vs {player2_2} | {score}\n"

        elif activity == "Boss Rush":
            eto_time = eto_entry.get()
            amon_time = amon_entry.get()
            nishiki_time = nishiki_entry.get()
            fight_boss_time = fight_boss_entry.get()

            if not all([eto_time, amon_time, nishiki_time, fight_boss_time]):
                messagebox.showerror("Error", "Please fill in all Boss Rush times.")
                return

            report += f"Eto: {eto_time} secs\nAmon: {amon_time} secs\nNishiki: {nishiki_time} secs\nFight boss: {fight_boss_time} sec\n"

        report += "=============================\n"

    report_window = tk.Toplevel(root)
    report_window.title("Training Report")
    report_text = tk.Text(report_window, wrap=tk.WORD)
    report_text.insert(tk.END, report)
    report_text.pack(expand=True, fill=tk.BOTH)

def add_onevone_match():
    new_match = tk.StringVar()
    match_frame = ttk.Frame(onevone_frame)
    player1_combobox = ttk.Combobox(match_frame, values=selected_attendees, width=20)
    player1_combobox.set("Select Player 1")
    player1_combobox.pack(side=tk.LEFT)
    tk.Label(match_frame, text="vs").pack(side=tk.LEFT)
    player2_combobox = ttk.Combobox(match_frame, values=selected_attendees, width=20)
    player2_combobox.set("Select Player 2")
    player2_combobox.pack(side=tk.LEFT)
    score_entry = ttk.Entry(match_frame, width=10, textvariable=new_match) 
    score_entry.pack(side=tk.LEFT)
    remove_button = ttk.Button(match_frame, text="-", command=lambda: match_frame.destroy())
    remove_button.pack(side=tk.LEFT)
    match_frame.pack()
    onevone_matches.append(new_match) 

def add_twovtwo_match():
    new_match = tk.StringVar()
    match_frame = ttk.Frame(twovtwo_frame)
    player1_combobox = ttk.Combobox(match_frame, values=selected_attendees, width=20)
    player1_combobox.set("Select Player 1")
    player1_combobox.pack(side=tk.LEFT)
    tk.Label(match_frame, text="vs").pack(side=tk.LEFT)
    player2_combobox = ttk.Combobox(match_frame, values=selected_attendees, width=20)
    player2_combobox.set("Select Player 2")
    player2_combobox.pack(side=tk.LEFT)
    score_entry = ttk.Entry(match_frame, width=10, textvariable=new_match) 
    score_entry.pack(side=tk.LEFT)
    remove_button = ttk.Button(match_frame, text="-", command=lambda: match_frame.destroy())
    remove_button.pack(side=tk.LEFT)
    match_frame.pack()
    twovtwo_matches.append(new_match) 


def next_page():
    global current_page
    if current_page == 1:
        if not selected_attendees:
            messagebox.showerror("Error", "Please select at least one attendee.")
            return
        current_page = 2
        show_page_2()
    elif current_page == 2:
        current_page = 3
        show_page_3()

def show_page_1():
    hide_all_widgets()
    attendees_label.pack()
    attendee_combobox.pack()
    selected_attendees_listbox.pack(expand=True, fill=tk.BOTH)
    next_button_page1.pack()

    attendee_combobox['values'] = attendees  

def on_attendee_select(event):
    selected = attendee_combobox.get()
    if selected and selected not in selected_attendees:
        selected_attendees.append(selected)
        selected_attendees_listbox.insert(tk.END, selected)
        attendee_combobox.set('') 
def show_page_2():
    hide_all_widgets()
    activities_label.pack()
    activity1_combobox.set("Select Activity 1")
    activity1_combobox.pack()
    activity2_combobox.set("Select Activity 2")
    activity2_combobox.pack()
    activity3_combobox.set("Select Activity 3")
    activity3_combobox.pack()
    next_button_page2.pack()

def show_page_3():
    hide_all_widgets()

    selected_activities = [activity1_combobox.get(), activity2_combobox.get(), activity3_combobox.get()]

    for i, activity in enumerate(selected_activities, 1):
        activity_label = ttk.Label(root, text=f"{i}. Activity: {activity}")
        activity_label.pack()

        if activity == "Free For All (FFA)":
            ffa_frame = ttk.Frame(root)
            ffa_frame.pack()
            ttk.Label(ffa_frame, text="First round winner:").pack(side=tk.LEFT)
            global ffa_first_round_entry
            ffa_first_round_entry = ttk.Entry(ffa_frame)
            ffa_first_round_entry.pack(side=tk.LEFT)
            ttk.Label(ffa_frame, text="Second round winner:").pack(side=tk.LEFT)
            global ffa_second_round_entry
            ffa_second_round_entry = ttk.Entry(ffa_frame)
            ffa_second_round_entry.pack(side=tk.LEFT)

        elif activity == "1v1s":
            global onevone_frame, onevone_matches
            onevone_frame = ttk.Frame(root)
            onevone_frame.pack()
            onevone_matches = []
            add_button = ttk.Button(root, text="+", command=add_onevone_match)
            add_button.pack()

        elif activity == "2v2s":
            global twovtwo_frame, twovtwo_matches
            twovtwo_frame = ttk.Frame(root)
            twovtwo_frame.pack()
            twovtwo_matches = []
            add_button = ttk.Button(root, text="+", command=add_twovtwo_match)
            add_button.pack()


        elif activity == "Boss Rush":
            boss_rush_frame = ttk.Frame(root)
            boss_rush_frame.pack()
            ttk.Label(boss_rush_frame, text="Eto:").pack()
            global eto_entry
            eto_entry = ttk.Entry(boss_rush_frame)
            eto_entry.pack()
            ttk.Label(boss_rush_frame, text="Amon:").pack()
            global amon_entry
            amon_entry = ttk.Entry(boss_rush_frame)
            amon_entry.pack()
            ttk.Label(boss_rush_frame, text="Nishiki:").pack()
            global nishiki_entry
            nishiki_entry = ttk.Entry(boss_rush_frame)
            nishiki_entry.pack()
            ttk.Label(boss_rush_frame, text="Fight boss:").pack()
            global fight_boss_entry
            fight_boss_entry = ttk.Entry(boss_rush_frame)
            fight_boss_entry.pack()

    generate_button = ttk.Button(root, text="Generate Report", command=generate_report)
    generate_button.pack()

def hide_all_widgets():
    for widget in root.winfo_children():
        widget.pack_forget()


attendees_label = ttk.Label(root, text="Select Attendees:")
attendee_combobox = ttk.Combobox(root)
attendee_combobox.bind("<<ComboboxSelected>>", on_attendee_select)
selected_attendees_listbox = tk.Listbox(root)
next_button_page1 = ttk.Button(root, text="Next", command=next_page)

activities_label = ttk.Label(root, text="Select Activities:")
activity1_combobox = ttk.Combobox(root, values=activities)
activity2_combobox = ttk.Combobox(root, values=activities)
activity3_combobox = ttk.Combobox(root, values=activities)
next_button_page2 = ttk.Button(root, text="Next", command=next_page)

show_page_1()

root.mainloop()