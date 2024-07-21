import plotly.graph_objects as go
import json

# Opening JSON file
f = open('./datavis/sample2.json')
word_to_show = "slate"
# returns JSON object as 
# a dictionary
data = json.load(f)

# Iterating through the json
# list
x = []
y = []
hover_text = []
for pattern in data[word_to_show]["patterns"]:
    res = ""
    for letter in pattern:
        if letter == "2":
            res += "🟩"
        if letter == "1":
            res += "🟨"
        if letter == "0":
            res += "⬛"
            
    x.append(res)
    y.append(data[word_to_show]["patterns"][pattern]["value"])
    hover_text.append(f"Probability: {round((int(data[word_to_show]["patterns"][pattern]["value"])/2315)*100,2)}%" )

# Closing file
f.close()

fig = go.Figure(data=[go.Bar(x=x, y=y, hovertext=hover_text)])
# Customize aspect
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
fig.update_layout(title_text=f'Result patterns for {word_to_show}',xaxis_tickangle=-45)
fig.show()