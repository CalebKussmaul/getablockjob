from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import json
import datetime
from .models import *



from threading import Timer,Thread,Event


def tick():
    for block in Block.objects.all():
        block.on_tick()

class perpetualTimer():


   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = tick
      self.thread = Timer(self.t,self.handle_function)


   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def printer():
    print ('ipsem lorem')

t = perpetualTimer(1,tick)
#t.start()


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
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def make_block(cord, x, y, block_type, cd, color):
    if block_type == 'basic':
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
            return redirect('home')
        else:
            return redirect('home')

        if username in cooldown:
            if cooldown[username] > datetime.datetime.now():
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
            if not Block.objects.filter(x=x, y=y).exists():
                make_block(cord=cord, x=x, y=y, block_type=block_type, cd=cd, color=color)
            elif Block.objects.get(x=x, y=y).color == color and Block.objects.get(x=x, y=y).typestr == block_type:
                Block.objects.get(x=x, y=y).health = Block.objects.get(x=x, y=y) + 1.0
            elif Block.objects.get(x=x, y=y).health <= 1.0:
                Block.objects.get(x=x, y=y).delete()
                make_block(cord = cord,x=x,y=y,block_type = block_type,cd=cd,color= color)
            else:
                Block.objects.get(x=x, y=y).health-=1
            cooldown[username] = datetime.datetime.now() + datetime.timedelta(seconds=Block.objects.get(x=x, y=y).cooldown)
            return gamedata(request)

    return False


def delete_block(request):
    if request.method == 'POST':
        response = request.body
        response = json.loads(response)
        if request.user.is_authenticated():
            username = request.user.username
        else:#redirect
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
                Block.objects.filter(x=x,y=y).delete()
                return gamedata(request)

    return False




def game(request):
    return render(request, "game.html")


def gamedata(request):
    game_dict = []
    print(Block.objects.count())
    for block in Block.objects.all():
        game_dict.append(block.as_json())

    results = {"blocks": [ob for ob in game_dict]}

    return HttpResponse(json.dumps(results), content_type="application/json")

    #
    # SomeModel_json = serializers.serialize("json", SomeModel.objects.all())
    # data = {"SomeModel_json": SomeModel_json}
    # return JsonResponse(data)