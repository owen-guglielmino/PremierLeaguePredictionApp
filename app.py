import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('best_rf.pkl', 'rb'))
teams_df = pd.read_csv('teams.csv')
teams = teams_df['Squad'].tolist()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        home = request.form['team1']
        away = request.form['team2']

        prediction_result = predict()

        return render_template('index.html', teams=teams, prediction_result=prediction_result.to_html(index=False))

    else:
        return render_template('index.html', teams=teams, prediction_result=None)


def predict():
    home, away = [str(x) for x in request.form.values()]
    
    home_feats = teams_df[teams_df['Squad'] == home].reset_index()
    away_feats = teams_df[teams_df['Squad'] == away].reset_index()

    home_feats = home_feats.drop(['index', 'Squad'], axis=1)
    away_feats = away_feats.drop(['index', 'Squad'], axis=1)

    home_feats = home_feats.loc[0, :].values.flatten().tolist()
    away_feats = away_feats.loc[0, :].values.flatten().tolist()
    
    for i in range(len(home_feats)):
        home_feats.append(away_feats[i])
    
    order = [2, 5, 1, 4, 0, 3]
    final_features = [home_feats[i] for i in order]
    final_features = np.array(final_features)
    final_features = final_features.reshape(1, -1)

    probs = model.predict_proba(final_features)

    result = pd.DataFrame(probs)
    result['Home Team'] = home
    result['Away Team'] = away

    result = result.rename({0: 'Away Win %', 1: 'Home Win %', 2: 'Draw %'}, axis=1)
    result = result.iloc[:, [3, 4, 1, 0, 2]].round(decimals=3)
    return result


if __name__=="__main__":
    app.run(debug=True)