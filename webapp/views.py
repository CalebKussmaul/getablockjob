from django.http import QueryDict, HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import json
import datetime
from .models import Block

COLOR = 'color'
TYPE = 'type'
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
        response = request.POST
        username = response.get('username')
        if username not in cooldown:
            x = cooldowntable[  response.get(TYPE)]
            cooldown[username] = datetime.datetime.now() + datetime.timedelta(minutes = x)
        else:
            if cooldown[username] < datetime.datetime.now():
                return HttpResponse( cooldown[username]- datetime.datetime.now() )

        if response.get('x') is not None and response.get('y') is not None and response.get(COLOR) is not None:
            type = response.get(TYPE)
            x = response.get('x')
            y = response.get('y')
            cord = (x, y)
            color = response.get(COLOR)

            success = False
            if cord not in board:
                board[cord] = Block(type, color, x, y)
                success = color
            elif board[cord].getColor() == color:
                board[cord].setHealth(board[cord].getHeath() + 1.0)
                success = color
            elif board[cord].getHeath() <= 1.0:
                board[cord] = Block(type, color, x, y)
                success = color
            else:
                board[cord].setHealth(board[cord].getHeath() - 1.0)
                success = board[cord].getColor
            return HttpResponse(success)
    return False


def delete_block(request):
    if request.method == 'POST':
        response = request.POST
        x = response.get('x')
        y = response.get('y')
        cord = (x, y)
        if cord is not None and cord in board:
            color = board[cord]
            board.pop(cord, None)
            return rander(color)
    return False


def get_board(request):
    if request.method == 'GET':
        return render(request,json.dumps(board))
    return False


def game(request):

    return render(request, "game.html")


def gamedata(request):

    return render(request, "game.html")
