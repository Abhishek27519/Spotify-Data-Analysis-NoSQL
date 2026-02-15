import tkinter as tk
from tkinter import Canvas, Scrollbar, Frame, Label
import matplotlib.pyplot as plt
import pymongo
import requests
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def mongodb_connection_spotify():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Spotify"]
    collection = db["Songs"]
    return collection

def trend_relationship(collection):
    pipeline = [
        {"$group": {
            "_id": {"$floor": {"$divide": ["$Popularity", 10]}},
            "averageDanceability": {"$avg": "$Danceability"},
            "averageEnergy": {"$avg": "$Energy"}
        }},
        {"$sort": {"_id": 1}}
    ]
    return list(collection.aggregate(pipeline))

def display_trend_relationship(results):
    wd = tk.Toplevel()
    wd.title("Task 1 Results")

    p_rng, avg_db, avg_eng = prepare_data_trend_relationship(results)
    diag = plot_trend_relationship(p_rng, avg_db, avg_eng)
    cvn = FigureCanvasTkAgg(diag, master=wd)
    cvn.draw()
    cvn.get_tk_widget().pack()

def prepare_data_trend_relationship(results):
    popularity_ranges = [str(result['_id']) for result in results]
    average_danceabilities = [result['averageDanceability'] for result in results]
    average_energies = [result['averageEnergy'] for result in results]

    return popularity_ranges, average_danceabilities, average_energies


def plot_trend_relationship(popularity_ranges, avg_db, avg_eng):
    diag, xaxis1 = plt.subplots(figsize=(12, 8))

    xaxis1.set_xlabel('Popularity Range', fontsize=14)
    xaxis1.set_ylabel('Average Danceability', color='tab:blue', fontsize=14)
    danceability_bars = xaxis1.bar(popularity_ranges, avg_db, color='tab:blue', label='Danceability')
    xaxis1.tick_params(axis='y', labelcolor='tab:blue')

    xaxis2 = xaxis1.twinx()
    xaxis2.set_ylabel('Average Energy', color='tab:red', fontsize=14)
    energy_line, = xaxis2.plot(popularity_ranges, avg_eng, color='tab:red', marker='o', label='Energy')
    xaxis2.tick_params(axis='y', labelcolor='tab:red')

    plt.title('Trend Analysis: Danceability and Energy by Popularity Range', fontsize=16, pad=20)

    plt.subplots_adjust(top=0.85, bottom=0.15, right=0.75)

    lines, labels = xaxis1.get_legend_handles_labels()
    lines2, labels2 = xaxis2.get_legend_handles_labels()
    xaxis2.legend(lines + lines2, labels + labels2, loc='center left', bbox_to_anchor=(1.08, 0.8))

    plt.tight_layout(pad=4)

    return diag

def label_comparison_enhanced(collection):
    pipeline = [
        {"$group": {
            "_id": "$Label",
            "averagePopularity": {"$avg": "$Popularity"},
            "averageDanceability": {"$avg": "$Danceability"},
            "averageEnergy": {"$avg": "$Energy"},
            "averageLoudness": {"$avg": "$Loudness"},
            "averageSpeechiness": {"$avg": "$Speechiness"},
            "averageAcousticness": {"$avg": "$Acousticness"},
            "averageInstrumentalness": {"$avg": "$Instrumentalness"},
            "averageLiveness": {"$avg": "$Liveness"},
            "averageValence": {"$avg": "$Valence"},
            "averageTempo": {"$avg": "$Tempo"},
            "averageImageURL": {"$first": "$Album Image URL"},
            "averageTrackName": {"$first": "$Track Name"},
            "averageArtistNames": {"$addToSet": "$Artist Name(s)"},
            "averageAlbumName": {"$first": "$Album Name"},
            "averageCopyrights": {"$first": "$Copyrights"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"averagePopularity": -1}},
        {"$limit": 10},
        {"$addFields": {
            "EnergyAndRhythm": {
                "$add": [
                    {"$multiply": [0.6, "$averageEnergy"]},
                    {"$multiply": [0.4, "$averageDanceability"]}
                ]
            },
            "VocalInstrumentalCharacteristics": {
                "$add": [
                    {"$multiply": [0.4, "$averageSpeechiness"]},
                    {"$multiply": [0.8, "$averageLiveness"]},
                    {"$multiply": [0.2, "$averageAcousticness"]}
                ]
            }
        }}
    ]
    return list(collection.aggregate(pipeline))

def plot_label_comparison_enhanced(labels, eng_rhy_val, vcl_inst_val):

    diag, axis = plt.subplots(figsize=(12, 5))

    bar_graph_width = 0.35

    axis.bar([i - bar_graph_width/2 for i in range(1, len(labels) + 1)], eng_rhy_val, width=bar_graph_width, label='Energy and Rhythm', color='teal')
    axis.bar([i + bar_graph_width/2 for i in range(1, len(labels) + 1)], vcl_inst_val, width=bar_graph_width, label='Vocal and Instrumental Characteristics', color='magenta')

    axis.set_xticks(range(1, len(labels) + 1))
    axis.set_xticklabels(labels)

    axis.set_ylabel('Values')
    axis.set_xlabel('Labels')
    axis.set_title('Top 10 Labels - Track Characteristics')

    axis.set_ylim(0, 1)

    axis.legend(loc='upper right', bbox_to_anchor=(1, 1))

    plt.subplots_adjust(right=0.8)

    axis.autoscale_view()

    return diag

def display_label_comparison_enhanced(results):
    wd = tk.Toplevel()
    wd.title("Task 2 Results - Enhanced Label Comparision")

    labels, eng_rhy_val, vcl_inst_val = prepare_data_label_comparison_enhanced(results)
    diag = plot_label_comparison_enhanced(labels, eng_rhy_val, vcl_inst_val)

    canvas = FigureCanvasTkAgg(diag, master=wd)
    canvas.draw()
    canvas.get_tk_widget().pack()

    scroll_frame = Frame(wd)
    scroll_frame.pack(fill=tk.BOTH, expand=True)

    canvas_for_scroll = Canvas(scroll_frame)
    scrollbar = Scrollbar(scroll_frame, orient="vertical", command=canvas_for_scroll.yview)
    scrollable_frame = Frame(canvas_for_scroll)

    canvas_for_scroll.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvas_for_scroll.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas_for_scroll.configure(yscrollcommand=scrollbar.set)

    top_labels_title = Label(scrollable_frame, text="Top 10 Label's Track Characteristics are:", font=("Helvetica", 12, "bold"))
    top_labels_title.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    for i, album in enumerate(results):

        lbl_txt = f"{i + 1}.Label: {album['_id']}\n"

        lbl_txt += f"Track: {album['averageTrackName']}\n"
        lbl_txt += f"Artists: {', '.join(album['averageArtistNames'])}\n"
        lbl_txt += f"Album: {album['averageAlbumName']}\n"
        lbl_txt += f"Popularity: {album['averagePopularity']:.2f}\n"

        label = Label(scrollable_frame, text=lbl_txt, anchor='w')
        label.grid(row=i + 1, column=0, padx=5, pady=5, sticky='w')

        album_image_url = album.get('averageImageURL')

        if album_image_url:
            try:
                response = requests.get(album_image_url, stream=True)
                response.raw.decode_content = True
                img = Image.open(response.raw)
                img = img.resize((100, 100), Image.BICUBIC)
                photo = ImageTk.PhotoImage(img)
                image_label = Label(scrollable_frame, image=photo)
                image_label.image = photo
                image_label.grid(row=i + 1, column=1, padx=5, pady=5, sticky='w')
            except Exception as e:
                print(f"Failed to load image for {album['Label']} - {e}")

    scrollable_frame.bind("<Configure>",
                          lambda e: canvas_for_scroll.configure(scrollregion=canvas_for_scroll.bbox("all")))

def prepare_data_label_comparison_enhanced(results):
    labels = [str(i) for i in range(1, len(results) + 1)]
    energy_rhythm_values = [(0.6 * r['averageEnergy'] + 0.4 * r['averageDanceability']) for r in results]
    vocal_instrumental_values = [
        (0.4 * r['averageSpeechiness'] + 0.8 * r['averageLiveness'] + 0.2 * r['averageAcousticness']) for r in results]

    return labels, energy_rhythm_values, vocal_instrumental_values


def release_timing_impact(collection):
    pipeline = [
        {
            "$match": {
                "Album Release Date": {"$type": "string"}
            }
        },
        {
            "$addFields": {
                "formattedReleaseDate": {
                    "$dateFromString": {
                        "dateString": "$Album Release Date",
                        "format": "%m/%d/%Y",
                        "onError": "Invalid Date"
                    }
                }
            }
        },
        {
            "$match": {"formattedReleaseDate": {"$ne": "Invalid Date"}}
        },
        {
            "$project": {
                "dayOfWeek": {"$dayOfWeek": "$formattedReleaseDate"},
                "tempo": "$Tempo",
                "energy": "$Energy",
                "popularity": "$Popularity"
            }
        },
        {
            "$group": {
                "_id": "$dayOfWeek",
                "averageTempo": {"$avg": "$tempo"},
                "averageEnergy": {"$avg": "$energy"},
                "averagePopularity": {"$avg": "$popularity"}
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ]
    return list(collection.aggregate(pipeline))

def plot_release_timing_impact(day_names, days_of_week, average_tempos, average_energies, average_popularities):

    diag, xaxis1 = plt.subplots(figsize=(10, 6))

    color = 'tab:orange'
    xaxis1.set_xlabel('Day of the Week')
    xaxis1.set_ylabel('Average Tempo (BPM)', color=color)
    xaxis1.bar(days_of_week, average_tempos, color=color)
    xaxis1.tick_params(axis='y', labelcolor=color)

    xaxis2 = xaxis1.twinx()
    color = 'tab:purple'
    xaxis2.set_ylabel('Average Energy', color=color)
    xaxis2.plot(days_of_week, average_energies, color=color, marker='o')
    xaxis2.tick_params(axis='y', labelcolor=color)

    xaxis3 = xaxis1.twinx()
    xaxis3.spines.right.set_position(("axes", 1.15))
    color = 'tab:blue'
    xaxis3.set_ylabel('Average Popularity', color=color)
    xaxis3.plot(days_of_week, average_popularities, color=color, marker='x')
    xaxis3.tick_params(axis='y', labelcolor=color)

    diag.tight_layout()
    plt.title('Impact of Release Timing on Track Characteristics')

    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], color='tab:orange', lw=4, label='Tempo'),
                       Line2D([0], [0], color='tab:purple', marker='o', label='Energy'),
                       Line2D([0], [0], color='tab:blue', marker='x', label='Popularity')]
    xaxis1.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.3, 0.8))

    plt.tight_layout(pad=4)

    return diag

def display_release_timing_impact(results):
    try:
        wd = tk.Toplevel()
        wd.title("Task 3 Results - Release Timing Impact")

        day_names, days_of_week, average_tempos, average_energies, average_popularities = prepare_data_release_timing_impact(results)
        diag = plot_release_timing_impact(day_names, days_of_week, average_tempos, average_energies, average_popularities)

        canvas = FigureCanvasTkAgg(diag, master=wd)
        canvas.draw()

        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

    except Exception as e:
        print(f"An error occurred: {e}")

def prepare_data_release_timing_impact(results):
    day_names = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday', 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
    days_of_week = [day_names.get(result['_id'], 'Unknown') for result in results]
    average_tempos = [result['averageTempo'] for result in results]
    average_energies = [result['averageEnergy'] for result in results]
    average_popularities = [result['averagePopularity'] for result in results]

    return day_names, days_of_week, average_tempos, average_energies, average_popularities


def duration_popularity_correlation(collection):
    pipeline = [
        {
            "$addFields": {
                "formattedReleaseDate": {
                    "$toDate": {
                        "$cond": {
                            "if": {"$eq": [{"$type": "$Album Release Date"}, "string"]},
                            "then": "$Album Release Date",
                            "else": None
                        }
                    }
                }
            }
        },
        {
            "$match": {"formattedReleaseDate": {"$ne": None}}
        },
        {
            "$group": {
                "_id": {"$year": "$formattedReleaseDate"},
                "averagePopularity": {"$avg": "$Popularity"},
                "averageDuration": {"$avg": "$Track Duration (ms)"}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    return list(collection.aggregate(pipeline))

def plot_duration_popularity_correlation(years, average_popularities, average_durations):


    diag, xaxis1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    xaxis1.set_xlabel('Year', fontsize=14)
    xaxis1.set_ylabel('Average Popularity', color=color, fontsize=14)
    xaxis1.scatter(years, average_popularities, color=color, label='Popularity')
    xaxis1.tick_params(axis='y', labelcolor=color)

    ax2 = xaxis1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Average Track Duration (ms)', color=color, fontsize=14)
    ax2.scatter(years, average_durations, color=color, label='Track Duration')
    ax2.tick_params(axis='y', labelcolor=color)

    xaxis1.legend(loc='upper left', bbox_to_anchor=(1.2, 1), fontsize=10, facecolor='white', framealpha=0.7)
    ax2.legend(loc='upper left', bbox_to_anchor=(1.2, 0.9), fontsize=10, facecolor='white', framealpha=0.7)

    plt.title('Correlation Between Track Duration and Popularity Over Years', fontsize=16)

    diag.tight_layout()

    return diag

def display_popularity_correlation(results):
    try:
        wd = tk.Toplevel()
        wd.title("Task 4 Results - Track Duration and Popularity Correlation")

        years, average_popularities, average_durations = prepare_data_display_popularity_correlation(results)
        diag = plot_duration_popularity_correlation(years, average_popularities, average_durations)

        canvas = FigureCanvasTkAgg(diag, master=wd)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        wd.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")

def prepare_data_display_popularity_correlation(results):
    years = [result['_id'] for result in results if result['_id'] is not None]
    average_popularities = [result['averagePopularity'] for result in results if result['_id'] is not None]
    average_durations = [result['averageDuration'] for result in results if result['_id'] is not None]

    return years, average_popularities, average_durations

def display_result_tk(collection):
    r = tk.Tk()
    r.title("Spotify Data Analysis")

    task_num = tk.IntVar()
    tk.Radiobutton(r, text="Trend Analysis", variable=task_num, value=1).pack(anchor='w')
    tk.Radiobutton(r, text="Label Comparison", variable=task_num, value=2).pack(anchor='w')
    tk.Radiobutton(r, text="Release Timing Impact", variable=task_num, value=3).pack(anchor='w')
    tk.Radiobutton(r, text="Track Duration and Popularity Correlation", variable=task_num, value=4).pack(anchor='w')

    def run_selected_query():
        spotify_run_task = task_num.get()
        if spotify_run_task == 1:
            results = trend_relationship(collection)
            display_trend_relationship(results)
        elif spotify_run_task == 2:
            results = label_comparison_enhanced(collection)
            display_label_comparison_enhanced(results)
        elif spotify_run_task == 3:
            results = release_timing_impact(collection)
            display_release_timing_impact(results)
        elif spotify_run_task == 4:
            results = duration_popularity_correlation(collection)
            display_popularity_correlation(results)

    spotify_task_btn = tk.Button(r, text="Run Query", command=run_selected_query)
    spotify_task_btn.pack()

    r.mainloop()

def main():
    cl = mongodb_connection_spotify()
    display_result_tk(cl)


if __name__ == "__main__":
    main()
