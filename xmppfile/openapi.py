import logging

from sanic.response import text, html, json, redirect

from sanic.blueprints import Blueprint




logger = logging.getLogger(__name__)


bp = Blueprint('openapi')




@bp.get('/')
async def index(request):
    # _token = request.headers.get('token')
    # user = request['session'].get(_token)
    #
    # return render('index.html', request, user=user)

    return json('hello 基本运行成功')





@bp.route('/login/', methods=['GET', 'POST'])
async def login(request):
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        user_list = await User.filter(nickname=username, password=password)
        if user_list:
            _token = binascii.hexlify(os.urandom(16)).decode("utf8")
            response = json(_token)

            if not request._cookies.get('session'):
                request['session']['session'] = _token
            return response
        else:
            return json({'msg': 'user not exist'})
    else:
        return render('login.html', request)
