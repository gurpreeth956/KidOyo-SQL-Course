import os
from os.path import join, dirname, realpath
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import pymysql.cursors


# IMAGES UPLOADING RELATING STUFF
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/images/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Do hard refresh on web page if something does not loading
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# FOR MAKING SURE FILE HAS ALLOWED EXTENSION
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def home():
    items = None
    names = None

    # CONNECTING TO DATABASE
    client = pymysql.connect("localhost", "public", "password123", "KidOYO")
    try:
        # SELECTING ALL ITEMS TO DISPLAY
        cursor = client.cursor()
        query = "SELECT ItemID, ItemName, ImageName, ItemDesc, PersonID FROM Items"
        cursor.execute(query)

        # IF CATEGORY SELECTED, ONLY SELECTING ITEMS BASED ON PERSON
        if 'category' in request.args:
            query = "SELECT Items.ItemID, Items.ItemName, Items.ImageName, Items.ItemDesc, Items.PersonID " \
                    "FROM Items INNER JOIN Person ON Items.PersonID = %s AND Person.PersonID = %s"
            #query = "SELECT ID, ItemName, ImageName, ItemDesc, PersonID FROM Items WHERE PersonID = %s"
            cursor.execute(query, (request.args['category'], request.args['category']))
        items = cursor.fetchall()

        # SELECTING PEOPLE TO DISPLAY
        query = "SELECT PersonID FROM Person"
        cursor.execute(query)
        names = cursor.fetchall()
    except Exception:
        print("Can not retrieve specified Entity")
    finally:
        client.close()
    # FOR UPLOADING NEW DATA
    if request.method == 'POST':
        if 'additem' in request.form:
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                print('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):

                # FILE IS FINE SO WE CAN DO THE ITEM ADD TRANSACTION NOW
                name = request.form['name']
                desc = request.form['desc']
                persid = request.form['chooseper']
                client = pymysql.connect("localhost", "public", "password123", "KidOYO")
                try:
                    cursor = client.cursor()
                    query = "INSERT INTO Items(ItemID, ItemName, ImageName, ItemDesc, PersonID) values(%s, %s, %s, %s, %s)"
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cursor.execute(query, (len(getItemTable()) + 1, name, filename, desc, persid))
                    client.commit()
                except Exception:
                    print("Could not add entity to Item Table")
                    client.rollback()
                finally:
                    client.close()
                if 'category' in request.args:
                    return redirect('/?category=' + request.args['category'])
                return redirect('/')

        if 'addperson' in request.form:
            person = request.form['person']
            gender = request.form['gender']
            client = pymysql.connect("localhost", "public", "password123", "KidOYO")
            try:
                cursor = client.cursor()
                query = "INSERT INTO Person(PersonID, Gender) values (%s, %s)"
                cursor.execute(query, (person, gender))
                client.commit()
            except Exception:
                print("Can not add Person entity")
                client.rollback()
            finally:
                client.close()
            return redirect('/')

        if 'delete' in request.form:
            itemid = request.form['itemID']
            client = pymysql.connect("localhost", "public", "password123", "KidOYO")
            try:
                cursor = client.cursor()
                query = "DELETE FROM Items WHERE ItemID = %s"
                cursor.execute(query, itemid)
                client.commit()
            except Exception:
                print("Can not delete Item")
                client.rollback()
            finally:
                client.close()
            return redirect('/')

    return render_template('index.html', items=items, names=names)


def getItemTable():
    client = pymysql.connect("localhost", "public", "password123", "KidOYO")
    try:
        cursor = client.cursor()
        query = "SELECT ItemID, ItemName, ImageName, ItemDesc, PersonID FROM Items"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception:
        print("Could not retrieve Item Table data")
    finally:
        client.close()


if __name__ == '__main__':
    app.run(debug=True)

