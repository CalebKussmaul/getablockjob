from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import json
import datetime
from .models import *

COLOR = "color"
TYPE = "type"
board = {}
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


def place_block(request):
    if request.method == 'POST':
        print(request.POST)
        response = request.body
        response = json.loads(response)
        if request.user.is_authenticated():
            username = request.user.username
            print(username)
        else:
            return HttpResponse(204, "not authenticated")
        if username not in cooldown:
            print(response)
            x = cooldowntable[response[TYPE]]
            cooldown[username] = datetime.datetime.now() + datetime.timedelta(minutes=x)

        else:
            if cooldown[username] < datetime.datetime.now():
                return HttpResponse(cooldown[username] - datetime.datetime.now())

        if response['x'] is not None and response['y'] is not None and response[COLOR] is not None:
            block_type = response[TYPE]
            x = response['x']
            y = response['y']
            cord = (x, y)
            cd = response['cooldown']
            color = response[COLOR]
            print(board)
            if cord not in board:
                if block_type == 'basic':
                    board[cord] = ColorBlock(x=x, y=y, color=color)
                elif block_type == 'gol':
                    board[cord] = GolBlock(x=x, y=y)
                elif block_type == 'mbs':
                    board[cord] = MbsBlock(x=x, y=y)
                elif block_type == 'note':
                    board[cord] = NotEastBlock(x=x, y=y)
                elif block_type == 'notn':
                    board[cord] = NotNorthBlock(x=x, y=y)
                elif block_type == 'nots':
                    board[cord] = NotSouthBlock(x=x, y=y)
                elif block_type == 'notw':
                    board[cord] = NotWestBlock(x=x, y=y)
                elif block_type == 'wireon':
                    board[cord] = WireOnBlock(x=x, y=y)
                elif block_type == 'wireoff':
                    board[cord] = WireOffBlock(x=x, y=y)
                elif block_type == 'othw':
                    board[cord] = OthelloWhiteBlock(x=x, y=y)
                elif block_type == 'othb':
                    board[cord] = OthelloBlackBlock(x=x, y=y)
                print(board)
            elif board[cord].getColor() == color:
                board[cord].setHealth(board[cord].getHeath() + 1.0)
            elif board[cord].getHeath() <= 1.0:
                board[cord] = Block(type=block_type, color=color, x=x, y=y, cooldown=cd, health=1.0)
            else:
                board[cord].setHealth(board[cord].getHeath() - 1.0)
            return gamedata(request)

    return False


def delete_block(request):
    if request.method == 'POST':
        response = request.POST
        x = response.get('x')
        y = response.get('y')
        cord = (x, y)
        if cord is not None and cord in board:
            board.pop(cord, None)
            return HttpResponse(204)
    return False


def get_board(request):
    if request.method == 'GET':
        return render(request, json.dumps(board))
    return False


def game(request):

    return render(request, "game.html")


def gamedata(request):
    game_dict = []
    for k, v in board.items():
        game_dict.append(v)

    results = {"blocks": [ob.as_json() for ob in game_dict]}
    print(results)

    return HttpResponse(json.dumps(results), content_type="application/json")
