from models import db, Favorit, Character, Planet


def existePlanetaFavorito(user_id, planet_id):
    if Favorit.query.filter_by(id_user=user_id).filter_by(id_planet=planet_id).filter_by(tipo="P").first():
        return True
    else:
        return False

    return False

def existeCharacterFavorito(user_id, character_id):
    if Favorit.query.filter_by(id_user=user_id).filter_by(id_character=character_id).filter_by(tipo="C").first():
        return True
    else:
        return False


def delPlanetFav(id_user, id_planet):
    return borra_favoritos("P", id_user, id_planet, 0)

def delcharacterFav(id_user, id_character):
    return borra_favoritos("C", id_user, 0, id_character)

def delAmbosFav(id_user, id_planet, id_character):
    return borra_favoritos("A", id_user, id_planet, id_character)



def borra_favoritos(tipo_fav, id_user, id_planet, id_character):
    aux = ""
    id_str = ""

    if (tipo_fav == "C"):
        n = Favorit.query.filter_by(id_user=id_user).filter_by(id_character=id_character).filter_by(tipo=tipo_fav).delete()
        aux = "Character"
        id_str = str(id_character)
    elif (tipo_fav == "P"):
        n = Favorit.query.filter_by(id_user=id_user).filter_by(id_planet=id_planet).filter_by(tipo=tipo_fav).delete()
        aux = "Planeta"
        id_str = str(id_planet)
    else:
        n = Favorit.query.filter_by(id_user=id_user).filter_by(id_planet=id_planet).filter_by(id_character=id_character).filter_by(tipo=tipo_fav).delete()
        aux = "Planeta/Character"
        id_str = str(id_planet)+"/"+str(id_character)

    if n == 1:
        db.session.commit()
        response_body = {"msg": "Borrado "+ aux +" Favorito: " + id_str + " del usuario: " + str(id_user)}
    elif n > 1:
        db.session.rollback()
        response_body = {"msg": "No se puede borrar "+ aux +" Favorito: " + id_str + " del usuario: " + str(id_user) + " tiene " +str(n)+ " registros"}
    else:
        db.session.rollback()
        response_body = {"msg": "No existe "+ aux +" Favorito: " + id_str + " del usuario: " + str(id_user)}

    return response_body

"""
    person = Person.query.get(3)
    person.delete()
    db.session.commit()



try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")

"""