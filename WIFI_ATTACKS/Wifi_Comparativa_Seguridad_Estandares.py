from flask import Flask, render_template_string
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = Flask(__name__)

# Datos de seguridad de los estándares WiFi
wifi_data = {
    'WEP': {
        'año': 1999,
        'seguridad': 2,
        'cifrado': 'RC4 (40-104 bits)',
        'autenticacion': 'Clave compartida',
        'vulnerabilidades': ['Clave estática', 'IV débil', 'Fácil de descifrar'],
        'color': '#ff4444'
    },
    'WPA': {
        'año': 2003,
        'seguridad': 5,
        'cifrado': 'TKIP con RC4',
        'autenticacion': 'PSK o 802.1X',
        'vulnerabilidades': ['Ataques de diccionario', 'Vulnerabilidades en TKIP'],
        'color': '#ffaa00'
    },
    'WPA2': {
        'año': 2004,
        'seguridad': 8,
        'cifrado': 'AES-CCMP',
        'autenticacion': 'PSK o 802.1X',
        'vulnerabilidades': ['KRACK attack', 'Ataque de diccionario offline'],
        'color': '#44aa44'
    },
    'WPA3': {
        'año': 2018,
        'seguridad': 10,
        'cifrado': 'AES-GCMP-256',
        'autenticacion': 'SAE (Dragonfly)',
        'vulnerabilidades': ['Dragonblood (parcheado)', 'Muy resistente'],
        'color': '#4444ff'
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seguridad en Estándares WiFi</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: white;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .slide {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .slide h2 {
            color: #667eea;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        .comparison-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .wifi-card {
            padding: 20px;
            border-radius: 10px;
            color: white;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .wifi-card h3 {
            font-size: 1.8em;
            margin-bottom: 15px;
        }
        .wifi-card p {
            margin: 8px 0;
            line-height: 1.6;
        }
        .wifi-card strong {
            display: inline-block;
            width: 120px;
        }
        .vulnerabilities {
            margin-top: 10px;
        }
        .vulnerabilities li {
            margin-left: 20px;
            margin-top: 5px;
        }
        .chart-container {
            margin: 20px 0;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
        }
        .similarities {
            background: #e7f3ff;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #2196F3;
        }
        .differences {
            background: #fff3e0;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #ff9800;
        }
        ul {
            margin-left: 20px;
            margin-top: 10px;
        }
        li {
            margin: 8px 0;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Seguridad en Estándares WiFi</h1>
        
        <!-- Slide 1: Comparación Visual -->
        <div class="slide">
            <h2>📊 Comparación de Seguridad</h2>
            <div class="comparison-grid">
                <div class="wifi-card" style="background: #ff4444;">
                    <h3>WEP</h3>
                    <p><strong>Año:</strong> 1999</p>
                    <p><strong>Cifrado:</strong> RC4 (40-104 bits)</p>
                    <p><strong>Autenticación:</strong> Clave compartida</p>
                    <p><strong>Nivel:</strong> ⚠️ Obsoleto</p>
                    <div class="vulnerabilities">
                        <strong>Vulnerabilidades:</strong>
                        <ul>
                            <li>Clave estática</li>
                            <li>IV débil</li>
                            <li>Fácil de descifrar</li>
                        </ul>
                    </div>
                </div>
                
                <div class="wifi-card" style="background: #ffaa00;">
                    <h3>WPA</h3>
                    <p><strong>Año:</strong> 2003</p>
                    <p><strong>Cifrado:</strong> TKIP con RC4</p>
                    <p><strong>Autenticación:</strong> PSK o 802.1X</p>
                    <p><strong>Nivel:</strong> ⚠️ Depreciado</p>
                    <div class="vulnerabilities">
                        <strong>Vulnerabilidades:</strong>
                        <ul>
                            <li>Ataques de diccionario</li>
                            <li>Vulnerabilidades en TKIP</li>
                        </ul>
                    </div>
                </div>
                
                <div class="wifi-card" style="background: #44aa44;">
                    <h3>WPA2</h3>
                    <p><strong>Año:</strong> 2004</p>
                    <p><strong>Cifrado:</strong> AES-CCMP</p>
                    <p><strong>Autenticación:</strong> PSK o 802.1X</p>
                    <p><strong>Nivel:</strong> ✅ Aceptable</p>
                    <div class="vulnerabilities">
                        <strong>Vulnerabilidades:</strong>
                        <ul>
                            <li>KRACK attack</li>
                            <li>Ataque de diccionario offline</li>
                        </ul>
                    </div>
                </div>
                
                <div class="wifi-card" style="background: #4444ff;">
                    <h3>WPA3</h3>
                    <p><strong>Año:</strong> 2018</p>
                    <p><strong>Cifrado:</strong> AES-GCMP-256</p>
                    <p><strong>Autenticación:</strong> SAE (Dragonfly)</p>
                    <p><strong>Nivel:</strong> ⭐ Recomendado</p>
                    <div class="vulnerabilities">
                        <strong>Vulnerabilidades:</strong>
                        <ul>
                            <li>Dragonblood (parcheado)</li>
                            <li>Muy resistente</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Slide 2: Gráficos -->
        <div class="slide">
            <h2>📈 Análisis de Seguridad</h2>
            <div class="chart-container">
                {{ security_chart | safe }}
            </div>
            <div class="chart-container">
                {{ timeline_chart | safe }}
            </div>
        </div>
        
        <!-- Slide 3: Similitudes -->
        <div class="slide">
            <h2>🎯 Comparación Radar - Todos los Estándares</h2>
            <div class="chart-container">
                {{ radar_chart_all | safe }}
            </div>
            <div style="background: #f0f4ff; padding: 20px; border-radius: 10px; margin-top: 20px;">
                <h3 style="color: #667eea;">📊 Criterios de Evaluación:</h3>
                <ul>
                    <li><strong>Cifrado:</strong> Robustez del algoritmo de cifrado utilizado</li>
                    <li><strong>Autenticación:</strong> Seguridad del proceso de verificación de identidad</li>
                    <li><strong>Resistencia a Ataques:</strong> Capacidad para resistir intentos de intrusión</li>
                    <li><strong>Protección de Contraseña:</strong> Defensa contra ataques de fuerza bruta y diccionario</li>
                    <li><strong>Velocidad:</strong> Rendimiento y eficiencia en la transmisión de datos</li>
                    <li><strong>Compatibilidad:</strong> Soporte en dispositivos existentes</li>
                </ul>
            </div>
        </div>
        
        <!-- Slide 4: Gráficos Radar Individuales -->
        <div class="slide">
            <h2>🔍 Análisis Individual por Estándar</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 20px;">
                <div class="chart-container">
                    {{ radar_wep | safe }}
                </div>
                <div class="chart-container">
                    {{ radar_wpa | safe }}
                </div>
                <div class="chart-container">
                    {{ radar_wpa2 | safe }}
                </div>
                <div class="chart-container">
                    {{ radar_wpa3 | safe }}
                </div>
            </div>
        </div>
        
        <!-- Slide 5: Similitudes -->
        <div class="slide">
            <h2>🔗 Similitudes</h2>
            <div class="similarities">
                <ul>
                    <li><strong>Propósito común:</strong> Todos buscan proteger redes inalámbricas de accesos no autorizados</li>
                    <li><strong>Autenticación:</strong> WPA, WPA2 y WPA3 soportan autenticación empresarial (802.1X/EAP)</li>
                    <li><strong>Compatibilidad:</strong> Muchos dispositivos modernos soportan múltiples estándares</li>
                    <li><strong>Basados en IEEE 802.11:</strong> Todos son extensiones del estándar base WiFi</li>
                    <li><strong>Cifrado de datos:</strong> Todos implementan alguna forma de cifrado de transmisión</li>
                    <li><strong>Uso de contraseñas:</strong> Todos permiten autenticación mediante PSK (clave pre-compartida)</li>
                </ul>
            </div>
        </div>
        
        <!-- Slide 6: Diferencias -->
        <div class="slide">
            <h2>⚡ Diferencias Clave</h2>
            <div class="differences">
                <h3 style="color: #ff5722; margin-bottom: 10px;">Cifrado</h3>
                <ul>
                    <li><strong>WEP:</strong> RC4 con claves de 40-104 bits (débil y obsoleto)</li>
                    <li><strong>WPA:</strong> TKIP con RC4 mejorado (temporal)</li>
                    <li><strong>WPA2:</strong> AES-CCMP de 128 bits (estándar actual)</li>
                    <li><strong>WPA3:</strong> AES-GCMP-256 de 256 bits (más robusto)</li>
                </ul>
                
                <h3 style="color: #ff5722; margin: 20px 0 10px 0;">Autenticación</h3>
                <ul>
                    <li><strong>WEP:</strong> Clave estática compartida</li>
                    <li><strong>WPA/WPA2:</strong> PSK (4-way handshake) o 802.1X</li>
                    <li><strong>WPA3:</strong> SAE (Simultaneous Authentication of Equals) - protege contra ataques offline</li>
                </ul>
                
                <h3 style="color: #ff5722; margin: 20px 0 10px 0;">Seguridad</h3>
                <ul>
                    <li><strong>WEP:</strong> Vulnerado completamente, se descifra en minutos</li>
                    <li><strong>WPA:</strong> Vulnerable a ataques de diccionario y fuerza bruta</li>
                    <li><strong>WPA2:</strong> Vulnerable a KRACK, pero aún seguro con contraseñas fuertes</li>
                    <li><strong>WPA3:</strong> Protección Forward Secrecy y contra ataques de diccionario offline</li>
                </ul>
                
                <h3 style="color: #ff5722; margin: 20px 0 10px 0;">Características Adicionales</h3>
                <ul>
                    <li><strong>WPA3:</strong> Incluye Easy Connect (configuración simplificada) y Enhanced Open (cifrado en redes públicas)</li>
                    <li><strong>WPA3:</strong> Cifrado individualizado en redes abiertas</li>
                    <li><strong>WPA3:</strong> Protección contra ataques de desautenticación</li>
                </ul>
            </div>
        </div>
        
        <!-- Slide 7: Recomendaciones -->
        <div class="slide">
            <h2>💡 Recomendaciones</h2>
            <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #4caf50;">
                <h3 style="color: #2e7d32;">✅ Usar:</h3>
                <ul>
                    <li><strong>Primera opción:</strong> WPA3 (si tu router y dispositivos lo soportan)</li>
                    <li><strong>Segunda opción:</strong> WPA2 con contraseña fuerte (mínimo 12 caracteres alfanuméricos)</li>
                </ul>
            </div>
            
            <div style="background: #ffebee; padding: 20px; border-radius: 10px; border-left: 5px solid #f44336; margin-top: 20px;">
                <h3 style="color: #c62828;">❌ Evitar:</h3>
                <ul>
                    <li><strong>WEP:</strong> Nunca usar, completamente inseguro</li>
                    <li><strong>WPA:</strong> Solo como último recurso en dispositivos antiguos</li>
                    <li><strong>Redes abiertas:</strong> Sin cifrado (a menos que uses VPN)</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    # Crear gráfico de barras de seguridad
    standards = list(wifi_data.keys())
    security_levels = [wifi_data[std]['seguridad'] for std in standards]
    colors = [wifi_data[std]['color'] for std in standards]
    
    fig_security = go.Figure(data=[
        go.Bar(
            x=standards,
            y=security_levels,
            marker_color=colors,
            text=security_levels,
            textposition='auto',
        )
    ])
    
    fig_security.update_layout(
        title='Nivel de Seguridad (0-10)',
        xaxis_title='Estándar WiFi',
        yaxis_title='Nivel de Seguridad',
        yaxis=dict(range=[0, 10]),
        plot_bgcolor='white',
        height=400
    )
    
    # Crear línea de tiempo
    years = [wifi_data[std]['año'] for std in standards]
    
    fig_timeline = go.Figure()
    
    fig_timeline.add_trace(go.Scatter(
        x=years,
        y=security_levels,
        mode='lines+markers+text',
        marker=dict(size=15, color=colors),
        line=dict(width=3, color='#667eea'),
        text=standards,
        textposition='top center',
        textfont=dict(size=14, color='black')
    ))
    
    fig_timeline.update_layout(
        title='Evolución de la Seguridad WiFi',
        xaxis_title='Año de Lanzamiento',
        yaxis_title='Nivel de Seguridad',
        yaxis=dict(range=[0, 11]),
        plot_bgcolor='white',
        height=400
    )
    
    # Crear gráficos de radar para cada estándar
    categories = ['Cifrado', 'Autenticación', 'Resistencia a<br>Ataques', 
                  'Protección de<br>Contraseña', 'Velocidad', 'Compatibilidad']
    
    # Valores para cada estándar (0-10)
    radar_values = {
        'WEP': [1, 2, 1, 1, 8, 10],
        'WPA': [4, 5, 4, 3, 7, 9],
        'WPA2': [8, 7, 7, 5, 9, 10],
        'WPA3': [10, 10, 9, 10, 9, 7]
    }
    
    # Crear gráfico de radar comparativo (todos juntos)
    fig_radar_all = go.Figure()
    
    for std in standards:
        fig_radar_all.add_trace(go.Scatterpolar(
            r=radar_values[std],
            theta=categories,
            fill='toself',
            name=std,
            line=dict(color=wifi_data[std]['color'], width=2),
            fillcolor=wifi_data[std]['color'],
            opacity=0.3
        ))
    
    fig_radar_all.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        title='Comparación Radar - Todos los Estándares',
        height=500
    )
    
    # Crear gráficos de radar individuales
    radar_charts_individual = {}
    for std in standards:
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=radar_values[std],
            theta=categories,
            fill='toself',
            name=std,
            line=dict(color=wifi_data[std]['color'], width=3),
            fillcolor=wifi_data[std]['color'],
            opacity=0.5
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=False,
            title=f'{std} - Análisis de Seguridad',
            height=400
        )
        
        radar_charts_individual[std] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # Renderizar plantilla
    return render_template_string(
        HTML_TEMPLATE,
        security_chart=fig_security.to_html(full_html=False, include_plotlyjs=False),
        timeline_chart=fig_timeline.to_html(full_html=False, include_plotlyjs=False),
        radar_chart_all=fig_radar_all.to_html(full_html=False, include_plotlyjs=False),
        radar_wep=radar_charts_individual['WEP'],
        radar_wpa=radar_charts_individual['WPA'],
        radar_wpa2=radar_charts_individual['WPA2'],
        radar_wpa3=radar_charts_individual['WPA3']
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)