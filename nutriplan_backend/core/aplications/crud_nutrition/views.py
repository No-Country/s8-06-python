import requests
from django.shortcuts import render, get_object_or_404, redirect
from ..crud_nutrition.models import Post_recipe
from .forms import PublicationRecipeForm
    
# BUSQUEDA DE RECETAS Y NUTRIENTES DE LA RECETA

def find_recipe(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        app_id = '2a1df3d6'
        api_key = '44a9edf235f4f291e95637636455047b'

        url = f'https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            recipes = data['hits']

            for recipe in recipes:
                recipe_data = recipe['recipe']
                calories = recipe_data['calories']
                yield_view = recipe_data['yield']
                calories_per_serving = calories / yield_view
                recipe_data['calories_per_serving'] = calories_per_serving

                total_nutrients = recipe_data['totalNutrients']

                nutrient_names = ['ENERC_KCAL', 'FAT', 'FASAT', 'CHOLE', 'NA',
                                  'CHOCDF', 'FIBTG', 'SUGAR', 'PROCNT', 'VITD', 'CA', 'FE', 'K']
                nutrient_info_list = [{'label': total_nutrients[name]['label'],
                                       'quantity': total_nutrients[name]['quantity'],
                                       'unit': total_nutrients[name]['unit']} for name in nutrient_names]

                # Lista de ingredientes a texto
                ingredients = [ingredient['text'] for ingredient in recipe_data['ingredients']]

                recipe_data['nutrient_info_list'] = nutrient_info_list
                recipe_data['ingredients'] = ingredients

            recipes.sort(key=lambda x: x['recipe']['label'])

            return render(request, 'find_recipe.html', {'recipes': recipes, 'nutrient_info_list': nutrient_info_list})
                
# CRUD PUBLICACIONES PROFESIONAL

def post_list(request):
    publications = Post_recipe.objects.all()
    return render(request, ' list_post.html', {'publications': publications})

def post_create(request):
    if request.method == 'POST':
        form = PublicationRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_post')
    else:
        form = PublicationRecipeForm()
    return render(request, 'create_post.html', {'form': form})

def post_detail(request, pk):
    publication = get_object_or_404(Post_recipe, pk=pk)
    return render(request, 'detail_post.html', {'publication': publication})

def post_edit(request, pk):
    publication = get_object_or_404(Post_recipe, pk=pk)
    if request.method == 'POST':
        form = PublicationRecipeForm(request.POST, instance=publication)
        if form.is_valid():
            form.save()
            return redirect('list_post')
    else:
        form = PublicationRecipeForm(instance=publication)
    return render(request, 'edit_post.html', {'form': form, 'publication': publication})

def post_delete(request, pk):
    publication = get_object_or_404(Post_recipe, pk=pk)
    if request.method == 'POST':
        publication.delete()
        return redirect('list_post')
    return render(request, 'delete_post.html', {'publication': publication})

def favorites_view(request):
    user = request.user
    favorites = user.favorite_post.all()
    return render(request, 'favorite_post.html', {'favorites': favorites})

