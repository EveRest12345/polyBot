
def registration():
    from firebase import firebase
    conc = input("На какой конкурс хотите зарегестрироваться?")
    token ='/hackaton-9de63/' + conc
    name = input("Введите ваше Ф.И.О:")
    age = input("Укажите ваш возраст:")
    groupe = input("Введите вашу группу:")
    mail = input("Укажите адресс вашей электронной почты:")
    phone = input("Введите ваш номер телефона:")
    firebase = firebase.FirebaseApplication("https://hackaton-9de63.firebaseio.com/")
    data = {

        'name':name,
        'age': age,
        'groupe': groupe,
        'email':mail,
        'number':phone

    }
    result = firebase.post(token , data)
    print(result)
registration()