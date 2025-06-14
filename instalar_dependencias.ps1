# Script de instalación para la app de Streamlit
# Ejecutar en PowerShell como administrador

Write-Host "📦 Instalando dependencias para la app de análisis de campaña electoral..." -ForegroundColor Green

# Instalar dependencias de Python
pip install -r requirements.txt

Write-Host "✅ Instalación completada!" -ForegroundColor Green
Write-Host "🚀 Para ejecutar la app, usa el comando:" -ForegroundColor Yellow
Write-Host "streamlit run app_streamlit_campana_mejorada.py" -ForegroundColor Cyan

# Pausa para ver el resultado
Read-Host "Presiona Enter para continuar..."
