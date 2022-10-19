from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('common_sentence/', views.common_sentence, name='common_sentence'),
    path('create_section/', views.create_section, name='create_section'),
    path("section/<int:id>/", views.view_section, name='view_section'),
    path('section/<int:id>/edit/', views.edit_section, name='edit_section'),
    path('section/update/', views.update_section, name='update_section'),
    path('delete_section/<int:id>', views.delete_section, name='delete_section'),
    path('create_sentence/<int:id>/', views.create_sentence, name='create_sentence'),
    path('edit_sentence/<int:id>/', views.edit_sentence, name='edit_sentence'),
    path('update_sentence', views.update_sentence, name='update_sentence'),
    path('delete_sentence/<int:id>/', views.delete_sentence, name='delete_sentence'),
    path('clear_index_history/', views.clear_index_history, name='clear_index_history'),
]
