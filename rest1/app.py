from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from flask import Flask, render_template, request

from forms import MainForm
import CharacterMaker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ravenclaw_rules'


@app.route('/', methods=['GET', 'POST'])
def main_form():
    form = MainForm()
    if form.is_submitted():
        result = request.form
        pokemon_1 = CharacterMaker.Pokemon(result['pokemon1_name'], result['pokemon1_level'])
        pokemon_2 = CharacterMaker.Pokemon(result['pokemon2_name'], result['pokemon2_level'])
        winner = pokemon_1.fight(pokemon_2)
        flavor, berry = CharacterMaker.define_nature()
        return render_template('submit.html', pokemon_1=pokemon_1, pokemon_2=pokemon_2, winner=winner, flavor=flavor, berry=berry)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
