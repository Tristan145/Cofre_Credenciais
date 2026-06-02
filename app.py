from flask import Flask, render_template, request, flash
import models
from security import encrypt_string, decrypt_string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def dashboard():
    credentials = models.Credential.query.all()
    return render_template('dashboard.html', credentials=credentials)

@app.route('/create-or-edit-credential', methods=['GET', 'POST'])
def create_or_edit_credential():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        username = request.form['username']
        password = request.form['password']

        new_credential = models.Credential(name=name, url=url, username=username, password=password)
        models.db.session.add(new_credential)
        models.db.session.commit()

        flash('Credential saved!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_or_edit_credential.html')
    if credential.user_id != user_id:
        return jsonify({'message': 'Access denied'}), 403

    db.session.delete(credential)
    db.session.commit()

    return jsonify({'message': 'Credential deleted successfully'})

@app.route('/revelar_senha/<int:id>', methods=['POST'])
def reveal_credential(id):
    user_id = request.args.get('user_id')
    data = request.get_json()
    password = data['password']

    credential = Credential.query.get_or_404(id)
    if credential.user_id != user_id:
        return jsonify({'message': 'Access denied'}), 403

    decrypted_password = decrypt_string(credential.encrypted_password)

    if password != decrypt_string(decrypted_password):
        return jsonify({'message': 'Invalid password'}), 401

    return jsonify({'decrypted_password': decrypted_password})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)