import os

def init_user(userid):
    os.mkdir('users/{}'.format(userid))
    os.mkdir('users/{}/images'.format(userid))
    os.mkdir('users/{}/features'.format(userid))
    os.mkdir('users/{}/test_images'.format(userid))
    os.mkdir('users/{}/test_features'.format(userid))
    with open('users/{}/features.csv'.format(userid), 'w') as features:
        with open('./app/static/template.csv', 'r') as f:
            headers = f.readlines()
            features.write(headers[0])
        