import html
from flask import Flask, render_template, session, request, flash, redirect

import enchant
import time

import data_processing
import word_processing

word_processing.process_words()
dictionary = enchant.DictWithPWL('en_GB', word_processing.ALL_WORDS)

app = Flask(__name__)
app.secret_key = "fhdgsd;ohfnvervneroigerrenverbner32hrjegb/kjbvr/o"


def check_spelling(words: list) -> list:
    spelling = []
    for word in words:
        spelling.append((word, dictionary.check(word)))
    return spelling


@app.route('/')
def hello_world() -> None:
    return redirect('/welcome')


@app.route('/welcome')
def welcome() -> None:
    return render_template('welcome.html')


@app.route('/startgame')
def startgame() -> 'html':
    session['source_word'] = word_processing.get_source_word()
    session['start_time'] = time.perf_counter()
    return render_template('startgame.html', sourceWord=session['source_word'])


@app.route('/processwords', methods=["POST"])
def process_words() -> 'html':
    session['final_time'] = time.perf_counter()
    winner = True
    seven_words = request.form['sevenWords'].lower().split(' ')
    seven_words = [word for word in seven_words if len(word) >= 1]
    new_word = len(seven_words)
    if new_word != 7:
        winner = False
        flash("Wrong number of words: {}, not 7.".format(new_word))
    wrong_letters = []
    for word in seven_words:
        wrong = [letter for (letter, ok) in
                 word_processing.check_letters(session['source_word'], word)
                 if not ok]
        wrong_letters.extend(wrong)
    if wrong_letters:
        winner = False
        flash("Invalid letters: " + ' '.join(set(wrong_letters)))
    incorrect_words = [word for (word, ok) in
                       check_spelling(seven_words)
                       if not ok]
    if incorrect_words:
        winner = False
        flash("Miss spelt these words: " + ' '.join(sorted(incorrect_words)))
    small_words = [word for (word, ok) in
                   word_processing.check_size(seven_words)
                   if not ok]
    if small_words:
        winner = False
        flash("Too small words: " + ' '.join(sorted(small_words)))
    if word_processing.check_duplicates(seven_words):
        winner = False
        flash("Duplicate words: " + ' '.join(sorted(seven_words)))
    if word_processing.check_source_word(seven_words, session['source_word']):
        winner = False
        flash("Cannot use given word: " + session['source_word'])
    if winner:
        time_passed = round(session['final_time'] - session['start_time'], 2)
        session['total_time'] = str(time_passed)
        flash("You took " + session['total_time'] + ' seconds.')
        session['finish'] = False
        return render_template('winner.html', title='Winner!')
    else:
        return render_template('loser.html', title='Loser!')


@app.route('/processhighscore', methods=["POST"])
def process_high_score() -> 'html':
    if not session['finish']:
        session['finish'] = True
        name = request.form['username']
        time_taken = float(session['total_time'])
        source = session['source_word']
        data_processing.add_scores(name, time_taken, source)
        leader_board = data_processing.retrieve_sorted_leaderboard()
        return render_template('leaderboard.html',
                               title='Top high scores!',
                               leaderboard=leader_board,
                               #position=leader_board.index((time_taken, name, source))+1,
                               outOf=len(leader_board))
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
