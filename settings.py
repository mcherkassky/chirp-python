MONGO_HOST = "paulo.mongohq.com"
MONGO_DATABASE_NAME = "Chirp"
MONGO_PORT = 10024

MONGO_USERNAME = "michael"
MONGO_PASSWORD = "cherkassky"

CONSUMER_KEY='vWbzHNYbSZB9vy1xcS5UNw'
CONSUMER_SECRET='FhtYfCx0Qvb0Q0F0KAGQFO0sQvJh1dH7Kq0MXuLRY'
CALLBACK_URL='http://chirp-app.herokuapp.com/verify'


API_KEY = 'AIzaSyA2IB5deG96CTPlH43p6ekdbco_TMi3gBc'
OAUTH2_CLIENT_ID = '783435406869.apps.googleusercontent.com'
OAUTH2_CLIENT_SECRET = 'C1osqQ9_U3HOfdTzvD6Tdirv'

#GOOGLE OAUTH API
ACCESS_TOKEN = 'ya29.1.AADtN_XPYZ0pe4-Q3lvahMpZAjBp1oEgoSBlUM18RhmJGWuZP6snAx_gibyQTmY'
REFRESH_TOKEN = '1/p7UoOGCo6Lte95zzfHhBM5Ujsw_A7uZOjKQyHHUyaUs'

HOST = 'http://127.0.0.1:5000'

# access_key='1552105075-fDyEqGl2qTOgFzdfJZAOAkZwlXdq7AXRxs2OZm4'
# access_secret='hbEZp3o075kvf7DS2v3RGhE9CGAzjzIVnqLI16w5kDGvK'

try:
    from settings_local import *
except:
    pass