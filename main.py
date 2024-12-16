import os

from flask import Flask, render_template, request
from db_model import Reaction
from flask_sqlalchemy import SQLAlchemy, pagination
app = Flask(__name__)

db_name = 'chem_reactions'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}.db'
db = SQLAlchemy(model_class=Reaction)
db.init_app(app)


@app.route('/', methods=['GET'])
def landing_page():
    per_page = 10
    page = 1
    go_to = request.args.get('go_to')
    if go_to is not None:
        if go_to.isnumeric():
            page = int(go_to)
    return render_template('index.html', data=Reaction.query.paginate(page=page, per_page=per_page),
                           tot_pages=Reaction.query.paginate(per_page=per_page).pages, page=page)


# @app.route('/<page>', methods=['GET'])
# def landing_page(page):
#     return render_template('index.html', data=Reaction.query.paginate(page=page, per_page=15))


@app.route('/addrxn', methods=['GET', 'POST'])
def add_rxn():
    if request.method == 'GET':
        return render_template('form.html'), 200
    else:
        response = 'NO changes made to database.'
        reactant_type = request.form.get('reactant_type')
        product_type = request.form.get('product_type')
        reactant = request.form.get('reactant')
        product = request.form.get('product')
        spc_name = request.form.get('spc_name')
        data = Reaction(reactant_type=reactant_type,
                        product_type=product_type,
                        catalyst=request.form.get('catalyst'),
                        reactant=reactant,
                        product=product,
                        spc_name=spc_name,
                        significance=request.form.get('significance'),
                        description=request.form.get('description')
                        )

        for i in [reactant, product, reactant_type, product_type, spc_name]:
            if i == '':
                response = 'You did not enter a required field.'
                return render_template('form.html', response=response)

        db.session.add(data)
        try:
            db.session.commit()
        except db.exc.IntegrityError:
            response = 'Integrity error in table. You did something wrong.'
        else:
            response = 'The reaction was added to database. You may add another if need be.'
        return render_template('form.html', response=response)


if __name__ == '__main__':
    app.app_context().push()  # pushes app context for db
    if not os.path.exists(f'./instance/{db_name}.db'):
        print(
            f'  [*] Creating a database: {db_name}')
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=False)
