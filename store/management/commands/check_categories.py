from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Product
from store.views import normalize_text
import unicodedata

class Command(BaseCommand):
    help = 'Verifica y arregla problemas de categorías y slugs automáticamente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Arreglar automáticamente los problemas encontrados',
        )
        parser.add_argument(
            '--check-duplicates',
            action='store_true',
            help='Verificar nombres duplicados o similares',
        )
        parser.add_argument(
            '--generate-test-urls',
            action='store_true',
            help='Generar URLs de prueba para todas las subcategorías',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 VERIFICANDO CATEGORÍAS Y SLUGS'))
        self.stdout.write('=' * 60)
        
        # Verificar todas las categorías
        categories = Category.objects.all()
        problems_found = []
        
        for category in categories:
            issues = self.check_category(category)
            if issues:
                problems_found.extend(issues)
        
        # Verificar duplicados si se solicita
        if options['check_duplicates']:
            duplicates = self.check_duplicates()
            problems_found.extend(duplicates)
        
        # Generar URLs de prueba si se solicita
        if options['generate_test_urls']:
            self.generate_test_urls()
        
        # Mostrar resumen
        self.stdout.write(f'\n📊 Categorías verificadas: {categories.count()}')
        self.stdout.write(f'🔍 Problemas encontrados: {len(problems_found)}')
        
        if problems_found:
            self.stdout.write('\n⚠️  PROBLEMAS ENCONTRADOS:')
            for problem in problems_found:
                self.stdout.write(f'- {problem}')
            
            if options['fix']:
                self.stdout.write('\n🔧 ARREGLANDO PROBLEMAS...')
                self.fix_problems(problems_found)
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ ¡No se encontraron problemas!'))

    def check_category(self, category):
        """Verifica problemas en una categoría específica"""
        issues = []
        
        # Verificar caracteres especiales problemáticos
        normalized = normalize_text(category.name)
        slug = slugify(category.name)
        
        # Verificar si el slug es muy diferente del nombre
        if len(slug) < len(category.name.replace(' ', '')) * 0.7:
            issues.append(f"Categoría '{category.name}': Slug muy corto '{slug}'")
        
        # Verificar caracteres especiales que podrían causar problemas
        if category.name != category.name.strip():
            issues.append(f"Categoría '{category.name}': Tiene espacios al inicio/final")
        
        # Verificar productos huérfanos
        if category.is_subcategory:
            products_count = Product.objects.filter(category=category).count()
            if products_count == 0:
                issues.append(f"Subcategoría '{category.name}': No tiene productos")
        
        return issues

    def check_duplicates(self):
        """Verifica nombres duplicados o muy similares"""
        issues = []
        categories = Category.objects.all()
        
        for i, cat1 in enumerate(categories):
            for cat2 in categories[i+1:]:
                # Verificar duplicados exactos (ignorando mayúsculas)
                if normalize_text(cat1.name) == normalize_text(cat2.name):
                    if cat1.parent == cat2.parent:  # Solo si están en el mismo nivel
                        issues.append(f"Duplicado: '{cat1.name}' y '{cat2.name}' (mismo nivel)")
                
                # Verificar nombres muy similares
                name1_normalized = normalize_text(cat1.name)
                name2_normalized = normalize_text(cat2.name)
                
                if (name1_normalized in name2_normalized or name2_normalized in name1_normalized) and len(name1_normalized) > 3:
                    issues.append(f"Similares: '{cat1.name}' y '{cat2.name}'")
        
        return issues

    def fix_problems(self, problems):
        """Intenta arreglar automáticamente algunos problemas"""
        fixed_count = 0
        
        for problem in problems:
            if "espacios al inicio/final" in problem:
                # Extraer nombre de categoría del mensaje de error
                category_name = problem.split("'")[1]
                try:
                    category = Category.objects.get(name=category_name)
                    old_name = category.name
                    category.name = category.name.strip()
                    category.save()
                    self.stdout.write(f"✅ Arreglado: '{old_name}' → '{category.name}'")
                    fixed_count += 1
                except Category.DoesNotExist:
                    self.stdout.write(f"❌ No se pudo encontrar la categoría para arreglar")
        
        self.stdout.write(f'\n🎉 Problemas arreglados: {fixed_count}')

    def generate_test_urls(self):
        """Genera URLs de prueba para todas las subcategorías"""
        self.stdout.write('\n🔗 URLs DE PRUEBA GENERADAS:')
        
        subcategories = Category.objects.filter(parent__isnull=False, is_active=True)
        
        for subcat in subcategories:
            parent_slug = slugify(subcat.parent.name)
            subcat_slug = slugify(subcat.name)
            url = f"/category/{parent_slug}/{subcat_slug}/"
            self.stdout.write(f"   {url} → {subcat.parent.name} > {subcat.name}")
