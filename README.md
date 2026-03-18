# 🚀 Asistente de Eventos con IA (Gemini)

Este proyecto es un asistente virtual inteligente que se conecta a una API de Django para gestionar eventos (crear, ver, actualizar y eliminar) usando lenguaje natural.

## 👥 Integrantes del Equipo
* **Alexis [moreno]** - Documentador
* **[Felipe Mendieta]** - UI/UX (Maquillador)
* **[sebastian murciua]** - Desarrolladr IA (ERRORES)
* **[David Anzola]** - Desarrollador (CORREO📰)


## 🛠️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Splashscar/PROYECTO_ADVAIH3.git]



   ## 📋 Solución de Problemas (FAQ)

Si encuentras algún error durante la ejecución, aquí tienes las soluciones más comunes:

* **Error 429 (RESOURCE_EXHAUSTED):** - **Causa:** Has superado el límite de peticiones gratuitas de la API de Gemini.
  - **Solución:** Espera 60 segundos antes de enviar otro mensaje o cambia el `modelo_id` a `gemini-1.5-flash` en el código.

* **Error de Conexión (Connection Error):** - **Causa:** El asistente no puede comunicarse con la API de Django.
  - **Solución:** Verifica que tu servidor backend esté corriendo en `http://127.0.0.1:8000`.

* **ID de Evento no encontrado:** - **Causa:** El ID proporcionado no existe en Firebase.
  - **Solución:** Primero ejecuta "Consultar mis tareas" para copiar el ID exacto (es una cadena de texto como `OZvDgeu...`).

* **Error de Autenticación:** - **Causa:** Email o contraseña incorrectos.
  - **Solución:** Revisa tus credenciales en la base de datos de Django.



  ---

## 🚀 Próximos Pasos (Mejoras Futuras)

Para las siguientes versiones del asistente, el equipo tiene planeado:

- [ ] **Notificaciones:** Implementar avisos automáticos al correo cuando se acerque la fecha de un evento.
- [ ] **Interfaz Gráfica:** Crear una ventana con botones (usando Tkinter o CustomTkinter) para no depender solo de la consola.
- [ ] **Soporte de Archivos:** Permitir que el usuario suba un PDF con su horario y que la IA extraiga los eventos automáticamente.
- [ ] **Sincronización:** Conectar el backend con Google Calendar real para ver los cambios en el celular.
- [ ] **Historial:** Guardar las conversaciones pasadas para que la IA recuerde eventos anteriores.