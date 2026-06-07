import os
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game, GameScore

@login_required
def games_dashboard(request):
    # 1. Waxaan soo qaadaynaa dhammaan games-ka firfircoon (Active)
    all_games = Game.objects.filter(is_active=True)
    
    # 2. Waxaan soo qaadaynaa dhibciha uu qofkaan hadda soo galay (User) ka dhashay games-ka
    user_scores = GameScore.objects.filter(user=request.user)
    
    # 3. Xogta profile-ka qofka si aan ugu tusino ID-giisa iyo magiciisa bogga games-ka
    user_profile = getattr(request.user, 'userprofile', None)

    context = {
        'games': all_games,
        'user_scores': user_scores,
        'user_profile': user_profile,
    }
    return render(request, 'maxamed_game/dashboard.html', context)


@login_required
def play_game(request, game_slug):
    # 1. Markuu qofku gujiyo game gaar ah, nidaamkaan ayaa furaya
    game = get_object_or_404(Game, slug=game_slug, is_active=True)
    
    # 2. Waxaan hubineynaa in feyl gaar ah oo ciyaartaan u rasi ah uu jiro iyo in kale
    specific_template = f"maxamed_game/games/{game.slug}.html"
    
    context = {
        'game': game,
        'user_profile': getattr(request.user, 'userprofile', None),
        'specific_template': specific_template,
    }
    return render(request, 'maxamed_game/play.html', context)