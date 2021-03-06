import datetime
import math
from itertools import chain
from time import mktime

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *


def get_all_blocks():
    return list(
        chain(BacteriaBlock.objects.all(), MbsBlock.objects.all(), ColorBlock.objects.all(), WireBlock.objects.all(),
              NotEastBlock.objects.all(), NotWestBlock.objects.all(), NotSouthBlock.objects.all(),
              NotNorthBlock.objects.all(), OthelloWhiteBlock.objects.all(), OthelloBlackBlock.objects.all(),
              TNTBlock.objects.all(), GolBlock.objects.all()))


from threading import Timer


def tick():
    blocks = get_all_blocks()
    if blocks is not None:
        for block in blocks:
            block.on_tick()


class perpetualTimer():
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = tick
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


def printer():
    print('ipsem lorem')


t = perpetualTimer(1, tick)
t.start()

TYPE = "type"

cooldown = {}
cooldowntable = {'basic': 5}


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/game')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def make_block(cord, x, y, block_type, cd, color):
    if block_type == 'basic':
        print(color)
        ColorBlock.objects.create(x=x, y=y, color=color)
    elif block_type == 'gol':
        GolBlock.objects.create(x=x, y=y)
    elif block_type == 'mbs':
        MbsBlock.objects.create(x=x, y=y)
    elif block_type == 'note':
        NotEastBlock.objects.create(x=x, y=y)
    elif block_type == 'notn':
        NotNorthBlock.objects.create(x=x, y=y)
    elif block_type == 'nots':
        NotSouthBlock.objects.create(x=x, y=y)
    elif block_type == 'notw':
        NotWestBlock.objects.create(x=x, y=y)
    elif block_type == 'wireon':
        WireBlock.objects.create(x=x, y=y)
    elif block_type == 'wireoff':
        WireBlock.objects.create(x=x, y=y)
    elif block_type == 'othw':
        OthelloWhiteBlock.objects.create(x=x, y=y)
    elif block_type == 'othb':
        OthelloBlackBlock.objects.create(x=x, y=y)
    elif block_type == 'bacteria':
        BacteriaBlock.objects.create(x=x, y=y)
    elif block_type == 'tnt':
        TNTBlock.objects.create(x=x, y=y)


def place_block(request):
    if request.method == 'POST':
        print(request.POST)
        response = request.body
        response = json.loads(response)
        print(response, "axxxx")
        if request.user.is_authenticated():
            username = request.user.username
            print(username, "xxx")
            if username in cooldown:
                if cooldown[username] > mktime(datetime.datetime.now().timetuple()):
                    print("STOP I CANT DO IT")

        if response['x'] is not None and response['y'] is not None:
            print(response)
            block_type = response[TYPE]
            x = response['x']
            y = response['y']
            if 'color' in response:
                color = response['color']
            else:
                color = None
            cord = (x, y)
            cd = response['cooldown']
            if (block_type == "remove") and Block.objects.filter(x=x, y=y).exists():
                print("deleting")
                Block.objects.get(x=x, y=y).health = math.floor(Block.objects.get(x=x, y=y).health - 1)
                if Block.objects.get(x=x, y=y).health <= 0:
                    Block.objects.get(x=x, y=y).delete()

            if not Block.objects.filter(x=x, y=y).exists():
                make_block(cord=cord, x=x, y=y, block_type=block_type, cd=cd, color=color)
            elif Block.objects.get(x=x, y=y).typestr == block_type:
                if Block.objects.get(x=x, y=y).typestr == 'basic':
                    if ColorBlock.objects.get(x=x, y=y).color == color:
                        Block.objects.get(x=x, y=y).health += 1.0
                else:
                    Block.objects.get(x=x, y=y).health += 1.0
            elif Block.objects.get(x=x, y=y).health <= 1.0:
                Block.objects.get(x=x, y=y).delete()

                make_block(cord=cord, x=x, y=y, block_type=block_type, cd=cd, color=color)

            else:
                Block.objects.get(x=x, y=y).health -= 1

            print(mktime(datetime.datetime.now().timetuple()))
            cooldowntime = Block.objects.get(x=x, y=y).cooldown
            if (block_type == "remove"):
                cooldowntime = 300
            cooldown[username] = mktime(datetime.datetime.now().timetuple()) + cooldowntime
            print(cooldown[username])
            return gamedata(request)

    return False


def delete_block(request):
    if request.method == 'POST':
        response = request.body
        response = json.loads(response)
        if request.user.is_authenticated():
            username = request.user.username
        else:  # redirect
            return HttpResponse(204, "not authenticated")
        if username not in cooldown:
            x = cooldowntable[response[TYPE]]
            cooldown[username] = datetime.datetime.now() + datetime.timedelta(minutes=x)

        else:
            if cooldown[username] < datetime.datetime.now():
                return HttpResponse(cooldown[username] - datetime.datetime.now())

        if response['x'] is not None and response['y'] is not None:
            x = response['x']
            y = response['y']
            cord = (x, y)

            if cord is not None and Block.objects.filter(x=x, y=y).exists():
                Block.objects.filter(x=x, y=y).delete()
                return gamedata(request)
    return False


def game(request):
    return render(request, "game.html")


def gamedata(request):
    game_dict = []
    for block in ColorBlock.objects.all():
        game_dict.append(block.as_json())
    for block in GolBlock.objects.all():
        game_dict.append(block.as_json())
    for block in MbsBlock.objects.all():
        game_dict.append(block.as_json())
    for block in NotEastBlock.objects.all():
        game_dict.append(block.as_json())
    for block in NotNorthBlock.objects.all():
        game_dict.append(block.as_json())
    for block in NotSouthBlock.objects.all():
        game_dict.append(block.as_json())
    for block in NotWestBlock.objects.all():
        game_dict.append(block.as_json())
    for block in WireBlock.objects.all():
        game_dict.append(block.as_json())
    for block in OthelloWhiteBlock.objects.all():
        game_dict.append(block.as_json())
    for block in OthelloBlackBlock.objects.all():
        game_dict.append(block.as_json())
    for block in BacteriaBlock.objects.all():
        game_dict.append(block.as_json())
    for block in TNTBlock.objects.all():
        game_dict.append(block.as_json())

    results = {"blocks": [ob for ob in game_dict]}

    if request.user.is_authenticated():
        username = request.user.username
        if username in cooldown:
            results["cooldown"] = cooldown[username]
        results["username"] = username

    print(results)
    return HttpResponse(json.dumps(results), content_type="application/json")

    #
    # SomeModel_json = serializers.serialize("json", SomeModel.objects.all())
    # data = {"SomeModel_json": SomeModel_json}
    # return JsonResponse(data)
