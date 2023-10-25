from django.urls import path

from materials.views import ( 
    add_reading_material, 
    reading_material,
    get_passage_info,
    delete_reading_material,
    manage_passage
)

urlpatterns = [
    # Reading Materials
    path('reading_material', reading_material.to_reading_materials, name="reading_material"),
    path('add_reading_material', add_reading_material.add_reading_material, name="add_reading_material"),
    path('manage_passage/<int:passage_id>', manage_passage.manage_passage, name="manage_passage"),
    path('delete_passage/<int:passage_id>', delete_reading_material.delete_passage, name="delete_passage"),
    path('get_passage_info/<int:passage_id>', get_passage_info.get_passage_info, name="get_passage_info"),
]