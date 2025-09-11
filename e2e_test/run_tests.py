"""
Script para ejecutar tests con diferentes configuraciones
"""
import subprocess
import sys
import os
import argparse
from datetime import datetime

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔄 {description}")
    print(f"Ejecutando: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - ÉXITO")
        if result.stdout:
            print(f"Output: {result.stdout}")
    else:
        print(f"❌ {description} - ERROR")
        if result.stderr:
            print(f"Error: {result.stderr}")
        if result.stdout:
            print(f"Output: {result.stdout}")
    
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description='Ejecutar tests de QA para ecommerce')
    parser.add_argument('--smoke', action='store_true', help='Ejecutar solo smoke tests')
    parser.add_argument('--regression', action='store_true', help='Ejecutar regression tests')
    parser.add_argument('--ui', action='store_true', help='Ejecutar solo UI tests')
    parser.add_argument('--api', action='store_true', help='Ejecutar solo API tests')
    parser.add_argument('--auth', action='store_true', help='Ejecutar solo tests de autenticación')
    parser.add_argument('--security', action='store_true', help='Ejecutar tests de seguridad')
    parser.add_argument('--performance', action='store_true', help='Ejecutar tests de rendimiento')
    parser.add_argument('--parallel', action='store_true', help='Ejecutar tests en paralelo')
    parser.add_argument('--headless', action='store_true', help='Ejecutar en modo headless')
    parser.add_argument('--browser', choices=['chrome', 'firefox'], default='chrome', help='Browser a usar')
    parser.add_argument('--env', choices=['dev', 'staging', 'prod'], default='dev', help='Ambiente de testing')
    parser.add_argument('--report', choices=['html', 'json', 'junit'], default='html', help='Formato de reporte')
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verbose')
    
    args = parser.parse_args()
    
    # Configurar directorio de reportes
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = f"e2e_test/reports/{timestamp}"
    os.makedirs(report_dir, exist_ok=True)
    
    # Construir comando base
    base_command = "pytest"
    
    # Agregar opciones según argumentos
    if args.smoke:
        base_command += " -m smoke"
    elif args.regression:
        base_command += " -m regression"
    elif args.ui:
        base_command += " -m ui"
    elif args.api:
        base_command += " -m api"
    elif args.auth:
        base_command += " -m auth"
    elif args.security:
        base_command += " -m security"
    elif args.performance:
        base_command += " -m performance"
    
    # Opciones adicionales
    if args.parallel:
        base_command += " -n auto"
    
    if args.verbose:
        base_command += " -v"
    
    # Configurar reporte
    if args.report == 'html':
        base_command += f" --html={report_dir}/report.html --self-contained-html"
    elif args.report == 'junit':
        base_command += f" --junit-xml={report_dir}/junit.xml"
    elif args.report == 'json':
        base_command += f" --json-report --json-report-file={report_dir}/report.json"
    
    # Configurar cobertura
    base_command += f" --cov=e2e_test --cov-report=html:{report_dir}/coverage"
    
    # Variables de entorno
    env_vars = {
        'BROWSER': args.browser,
        'HEADLESS': str(args.headless).lower(),
        'ENV': args.env,
        'REPORT_DIR': report_dir
    }
    
    # Configurar variables de entorno
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("🚀 Iniciando ejecución de tests de QA")
    print(f"📊 Configuración:")
    print(f"   - Browser: {args.browser}")
    print(f"   - Headless: {args.headless}")
    print(f"   - Ambiente: {args.env}")
    print(f"   - Reporte: {args.report}")
    print(f"   - Directorio de reportes: {report_dir}")
    
    # Ejecutar tests
    success = run_command(base_command, "Ejecutando tests de QA")
    
    if success:
        print("\n🎉 Todos los tests completados exitosamente!")
        print(f"📄 Reportes generados en: {report_dir}")
        
        # Mostrar ubicación de reportes
        if args.report == 'html':
            print(f"🌐 Reporte HTML: {report_dir}/report.html")
        elif args.report == 'junit':
            print(f"📋 Reporte JUnit: {report_dir}/junit.xml")
        elif args.report == 'json':
            print(f"📊 Reporte JSON: {report_dir}/report.json")
        
        print(f"📈 Reporte de cobertura: {report_dir}/coverage/index.html")
    else:
        print("\n❌ Algunos tests fallaron")
        print(f"📄 Revisa los reportes en: {report_dir}")
        sys.exit(1)

if __name__ == "__main__":
    main()
