from django.shortcuts import render


# Create your views here.

# def home(request):
#     return render(request, 'packitPolygons/home.html')


def hexagon(request):
    current_turn = 1
    context = {
        'current_turn': current_turn,
    }
    return render(request, 'packitPolygons/hexagonal_board.html', context)


def index(request):
    current_turn = 1
    context = {
        'current_turn': current_turn,
    }
    return render(request, 'packitPolygons/index.html', context)

# def
