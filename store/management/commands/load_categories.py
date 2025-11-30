from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    help = 'Carga las categorías y subcategorías predefinidas de Armería Sniper'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todas las categorías existentes antes de cargar las nuevas',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('🗑️  Eliminando categorías existentes...')
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('Todas las categorías han sido eliminadas.'))

        # Definir estructura de categorías
        categories_data = {
            'SERVICIOS': [
                'Taller de reparación',
                'Certificaciones de armas de fuego',
                'Tasaciones para sucesiones',
                'Estudio criminalístico forense'
            ],
            
            'ARMAS': [
                'Armas Cortas',
                'Armas Largas',
                'Pistolones',
                'Armas Combinadas',
                'Armas de Proyección (Venta libre)',
                'Aire Comprimido / PCP / CO2 (Venta Libre)',
                'Armas de Colección (Venta libre)',
                'Armas Raras / Difíciles de conseguir',
                'Armas Nacionales Históricas',
                'Armas No Letales (Venta libre)'
            ],
            
            'ACCESORIOS': [
                'Cachas para Pistolas',
                'Cachas para Revólveres',
                'Cachas para Restauraciones',
                'Cargadores Nuevos',
                'Cargadores Usados',
                'Aparatos de Puntería',
                'Fundas y Portas',
                'Estuches',
                'Linternas y Láser',
                'Mantenimiento de Armas',
                'Accesorios para Tiradores'
            ],
            
            'COLECCIONISMO': [
                'Militaría y Coleccionismo',
                'Libros y Manuales'
            ],
            
            'CONSUMIBLES': [
                'Recarga y Limpieza'
            ]
        }

        self.stdout.write('🚀 Iniciando carga de categorías...')
        
        created_categories = 0
        created_subcategories = 0
        
        for category_name, subcategory_list in categories_data.items():
            
            # Crear categoría principal
            parent_category, created = Category.objects.get_or_create(
                name=category_name,
                parent=None,
                defaults={
                    'description': f'Categoría principal: {category_name}',
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'✅ Categoría creada: {category_name}')
                created_categories += 1
            else:
                self.stdout.write(f'📁 Categoría existente: {category_name}')
            
            # Crear subcategorías
            for subcategory_name in subcategory_list:
                subcategory, created = Category.objects.get_or_create(
                    name=subcategory_name,
                    parent=parent_category,
                    defaults={
                        'description': f'Subcategoría de {category_name}',
                        'is_active': True
                    }
                )
                
                if created:
                    self.stdout.write(f'  ✅ Subcategoría creada: {subcategory_name}')
                    created_subcategories += 1
                else:
                    self.stdout.write(f'  📄 Subcategoría existente: {subcategory_name}')
        
        # Mostrar resumen
        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 PROCESO COMPLETADO:\n'
            f'   📁 Categorías principales creadas: {created_categories}\n'
            f'   📄 Subcategorías creadas: {created_subcategories}\n'
            f'   📊 Total de categorías principales: {Category.objects.filter(parent=None).count()}\n'
            f'   📊 Total de subcategorías: {Category.objects.filter(parent__isnull=False).count()}'
        ))
        
        # Mostrar árbol de categorías
        if options['verbosity'] >= 2:
            self.show_category_tree()

    def show_category_tree(self):
        """Muestra el árbol de categorías creado"""
        self.stdout.write('\n🌳 ÁRBOL DE CATEGORÍAS:')
        self.stdout.write('=' * 40)
        
        parent_categories = Category.objects.filter(parent=None, is_active=True).order_by('name')
        
        for parent in parent_categories:
            self.stdout.write(f'📁 {parent.name}')
            
            subcategories = parent.subcategories.filter(is_active=True).order_by('name')
            for i, sub in enumerate(subcategories):
                connector = "└──" if i == len(subcategories) - 1 else "├──"
                self.stdout.write(f'    {connector} {sub.name}')
            self.stdout.write('')
