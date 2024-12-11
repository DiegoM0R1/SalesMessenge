# Estudio Tesen

**Estudio Tesen** es una plataforma de gestión para usuarios, clientes, oportunidades de negocio, cotizaciones, cobranzas, y más. Este proyecto está desarrollado con Django y tiene como objetivo facilitar la administración de clientes y su ciclo de ventas, desde la creación de oportunidades hasta la gestión de facturas y cobranzas.

## Características

- **Gestión de usuarios**: Los usuarios pueden tener roles de administrador o trabajador de área.
- **Mensajes**: Los usuarios pueden enviar mensajes tanto directos como en grupos, con soporte para texto, imágenes, videos y archivos adjuntos.
- **Gestión de clientes**: Administración de la información del cliente, incluyendo categoría, estado, y fecha de creación.
- **Oportunidades de negocio**: Las oportunidades de negocio pueden ser creadas, actualizadas y asociadas a un cliente.
- **Cotizaciones**: Se pueden crear cotizaciones para cada oportunidad de negocio.
- **Facturación**: Generación de facturas con su respectivo estado (pendiente o pagada).
- **Cobranza**: Gestión de pagos relacionados con las facturas, con el estado parcial o total.
- **Consultas**: Los clientes pueden registrar consultas que se pueden resolver o dejar pendientes.

## Tecnologías

- **Backend**: Django (Python)
- **Base de Datos**: PostgreSQL (o cualquier base de datos compatible con Django)
- **Imágenes**: Soporte para carga de imágenes de perfil y archivos adjuntos
- **Gestión de archivos**: Uso de `FileField` y `ImageField` para el manejo de archivos y fotos

## Instalación

1. **Clona este repositorio**:

    ```bash
    git clone https://github.com/tuusuario/estudio-tesen.git
    cd estudio-tesen
    ```

2. **Crea un entorno virtual**:

    ```bash
    python -m venv venv
    ```

3. **Activa el entorno virtual**:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instala las dependencias**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Configura tu base de datos**:
   - Asegúrate de tener PostgreSQL instalado (o el motor de base de datos que prefieras).
   - Crea la base de datos y actualiza el archivo `settings.py` con las credenciales adecuadas.

6. **Realiza las migraciones**:

    ```bash
    python manage.py migrate
    ```

7. **Crea un superusuario** (si necesitas acceder al admin):

    ```bash
    python manage.py createsuperuser
    ```

8. **Corre el servidor de desarrollo**:

    ```bash
    python manage.py runserver
    ```

## Estructura del Proyecto

- `estudio_tesen/`: Directorio principal del proyecto.
    - `settings.py`: Configuración del proyecto, incluyendo base de datos y aplicaciones instaladas.
    - `urls.py`: Definición de las URLs del proyecto.
    - `wsgi.py`: Archivo WSGI para el despliegue en producción.
- `app/`: Directorio con las aplicaciones Django que manejan la lógica de negocio (usuarios, clientes, ventas, etc.).
    - `models.py`: Definición de modelos de base de datos.
    - `views.py`: Lógica de las vistas.
    - `urls.py`: Rutas específicas de la aplicación.
    - `admin.py`: Configuración de la interfaz administrativa de Django.

## Modelos

### **Usuario**
El modelo `Usuario` gestiona la información de los usuarios del sistema, incluyendo nombre, apellido, código, tipo de usuario (admin/trabajador), y la foto de perfil.

### **Mensaje**
El modelo `Mensaje` gestiona la comunicación entre usuarios. Los mensajes pueden ser de tipo texto, foto, video o archivo.

### **GrupoChat**
El modelo `GrupoChat` permite la creación de grupos de chat con múltiples usuarios. Los mensajes dentro del grupo se gestionan a través del modelo `MensajeGrupo`.

### **Cliente**
El modelo `Cliente` administra la información de los clientes, incluyendo su categoría (alto, medio, bajo, VIP, etc.) y estado (activo, prospecto, inactivo).

### **Oportunidad**
El modelo `Oportunidad` representa una oportunidad de negocio para un cliente, con un estado que puede cambiar entre prospecto, negociación, cerrado y seguimiento.

### **Cotización**
El modelo `Cotización` está vinculado a una oportunidad de negocio, y registra la descripción, valor y estado de la cotización.

### **Factura**
El modelo `Factura` gestiona las facturas de los clientes, con un estado que indica si la factura está pendiente o pagada.

### **Cobranza**
El modelo `Cobranza` registra los pagos realizados para una factura, y su estado (parcial o total).

### **Consulta**
El modelo `Consulta` permite registrar consultas realizadas por los clientes, con estado pendiente o resuelto.

## Contribuciones

Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

1. Haz un fork de este repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios.
4. Haz un commit con tus cambios (`git commit -m 'Añadir nueva funcionalidad'`).
5. Haz un push a tu rama (`git push origin feature/nueva-funcionalidad`).
6. Abre un Pull Request para que se revisen tus cambios.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

¡Gracias por usar **Estudio Tesen**!
