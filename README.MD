# Proyecto Gimnasio Codemakers

## Descripción del Proyecto
El proyecto **Gimnasio Codemakers** es una aplicación web diseñada para gestionar y facilitar la administración de un gimnasio. La plataforma permite la gestión de usuarios con diferentes roles (Clientes, Asistentes, Entrenadores), así como la visualización y actualización de sus perfiles. Además, los usuarios pueden ver y filtrar las máquinas disponibles en el gimnasio y suscribirse a diferentes planes de membresía.

El proyecto está construido utilizando el framework Django, que ofrece una robusta estructura para el desarrollo de aplicaciones web. El diseño de la página es responsivo y está estilizado con Bootstrap y CSS personalizado, asegurando que se vea bien en dispositivos de diferentes tamaños.

## Tecnologías Utilizadas
- **Django 5.0**: El framework principal para el desarrollo de la aplicación web.
- **SQLite3**: Base de datos utilizada para almacenar la información de los usuarios y las máquinas.
- **Bootstrap**: Utilizado para hacer que el diseño sea atractivo y responsivo.
- **CSS**: Para estilizar componentes específicos de la página.
- **JavaScript**: Para manejar interacciones dinámicas, como la edición en línea de perfiles.
- **HTML**: Para estructurar las páginas web.
- **Sweetify**: Para mostrar alertas de manera atractiva y moderna.
- **Python DataUtil**: Para el manejo de fechas y formatos de estas.


## Modo de Uso

### Instalación del Entorno Virtual
1. 
    ```bash
    git clone https://github.com/Doxir010/https://github.com/Doxir010/cs50w-project5.git
    cd cs50w-project5
    ```
2. 
    ```bash
    python -m venv env
    ```
3. 
    
    ```bash
    .\env\Scripts\activate
    ```

### Instalación de Requerimientos
1. Instala las dependencias del proyecto:
    ```bash
    pip install -r requirements.txt
    ```

### Configuración de la Base de Datos
1. Realiza las migraciones para configurar la base de datos:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Ejecución del Servidor de Desarrollo
1. Inicia el servidor de desarrollo de Django:
    ```bash
    python manage.py runserver
    ```

2. Abre tu navegador y ve a `http://127.0.0.1:8000/` para ver la aplicación en funcionamiento.

## Distinción y Complejidad
Hablando respecto al apartado de distincion y complejidad considero que mi proyecto es en cierta forma unica ya que implementa varios de los conocimientos
adquiridos en los distintos projects anteriores realizados en este curso de modo que crea una aplicacion a la cual se le puede sacar provecho en la vida real.
Considero el apartado de pago de membresia y su validado de fechas como lo que mas se me dificulto asi como la implementacion de js para apartados como la asistencia.
ya que por el diseño que elegi no lo hizo una tarea facil.

## Como surgio esta idea
Esta idea vino a mi mente debido a que al ir a un gimnasio por primera vez note como este llevaba registro aun con un cuaderno donde todos se apuntaban y si bien
esto puede ser conveniente en ciertos aspectos, en mas de una ocasion veia a los encargados batallar por buscar algunos registros. Es por esto que comenze a pensar en
esta idea y luego el resto de apartados surgio en base a mi abstraccion sobre las necesidades que este tipo de negocios pueden llegar a tener. Porque a veces
no es necesario pensar en una idea revolucionaria que vaya a ser la proxima gran app del mercado cuando en realidad la escencia de ser desarrollador de aplicaciones es 
suplir las necesidades de los negocios mas cotidianos.

## Perfil de GitHub
Puedes encontrar más proyectos en mi [perfil de GitHub](https://github.com/Doxir010).

## Agradecimientos
Agradecimientos especiales a:
- **Lars**: Por su constante apoyo y colaboración en el proyecto.
- **Adrian Luna**: Por sus valiosos aportes y sugerencias durante el desarrollo.

¡Gracias por utilizar **Gimnasio Codemakers**! 