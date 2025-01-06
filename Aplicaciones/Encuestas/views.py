from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Encuesta, Pregunta, Respuesta, RespuestaUsuario
from .forms import EncuestaForm
from django.shortcuts import get_object_or_404




def inicio(request):
    return render(request, 'inicio.html')

@login_required
def encuestas(request):
    return render(request, 'crear_encuesta.html')

@login_required
def crear_encuesta(request):
    if request.method == 'POST':
        encuesta_form = EncuestaForm(request.POST)

        if encuesta_form.is_valid():
            encuesta = encuesta_form.save()
            
            # Extraer preguntas y opciones dinámicamente del POST
            total_preguntas = int(request.POST.get('total_preguntas', 0))
            for i in range(total_preguntas):
                pregunta_texto = request.POST.get(f'pregunta_{i}')
                if pregunta_texto:
                    pregunta = Pregunta.objects.create(encuesta=encuesta, texto=pregunta_texto)

                    # Opciones para la pregunta
                    total_opciones = int(request.POST.get(f'total_opciones_pregunta_{i}', 0))
                    for j in range(total_opciones):
                        opcion_texto = request.POST.get(f'pregunta_{i}_opcion_{j}')
                        if opcion_texto:
                            Respuesta.objects.create(pregunta=pregunta, texto=opcion_texto)

            return redirect('lista_encuestas')
    else:
        encuesta_form = EncuestaForm()

    return render(request, 'crear_encuesta.html', {
        'encuesta_form': encuesta_form,
    })


@login_required
def resultados_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    preguntas = encuesta.preguntas.all()

    resultados = []
    for pregunta in preguntas:
        conteo_respuestas = []
        for respuesta in pregunta.respuestas.all():
            # Contar cuántos usuarios seleccionaron esta respuesta
            conteo = RespuestaUsuario.objects.filter(
                pregunta=pregunta, respuesta=respuesta
            ).count()
            conteo_respuestas.append((respuesta.texto, conteo))  # Lista de tuplas
        resultados.append({
            "texto": pregunta.texto,
            "resultados": conteo_respuestas,  # Lista ordenada
        })

    return render(request, 'resultados_encuesta.html', {
        'encuesta': encuesta,
        'resultados': resultados,
    })


def lista_encuestas(request):
    encuestas = Encuesta.objects.all()
    return render(request, 'lista_encuestas.html', {'encuestas': encuestas})

@login_required
def gracias(request):
    return render(request, 'gracias.html')

@login_required
def editar_encuesta_form(request, encuesta_id):
    # Obtener la encuesta seleccionada
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    preguntas = encuesta.preguntas.all()

    if request.method == 'POST':
        # Actualizar título y descripción de la encuesta
        encuesta.titulo = request.POST.get('titulo', encuesta.titulo)
        encuesta.descripcion = request.POST.get('descripcion', encuesta.descripcion)
        encuesta.save()

        # Actualizar preguntas existentes
        preguntas_existentes_ids = []
        for pregunta in preguntas:
            pregunta_texto = request.POST.get(f'pregunta_{pregunta.id}')
            if pregunta_texto:
                pregunta.texto = pregunta_texto
                pregunta.save()
                preguntas_existentes_ids.append(str(pregunta.id))

                # Actualizar respuestas existentes de esta pregunta
                respuestas_existentes_ids = []
                for respuesta in pregunta.respuestas.all():
                    respuesta_texto = request.POST.get(f'respuesta_{respuesta.id}')
                    if respuesta_texto:
                        respuesta.texto = respuesta_texto
                        respuesta.save()
                        respuestas_existentes_ids.append(str(respuesta.id))

                # Eliminar respuestas que no están en el formulario
                for respuesta in pregunta.respuestas.all():
                    if str(respuesta.id) not in respuestas_existentes_ids:
                        respuesta.delete()

                # Procesar nuevas respuestas para esta pregunta
                for key, value in request.POST.items():
                    if key.startswith(f'respuesta_new_{pregunta.id}_'):
                        Respuesta.objects.create(
                            pregunta=pregunta,
                            texto=value
                        )

        # Eliminar preguntas que no están en el formulario
        for pregunta in preguntas:
            if str(pregunta.id) not in preguntas_existentes_ids:
                pregunta.delete()

        # Procesar nuevas preguntas
        for key, value in request.POST.items():
            if key.startswith('pregunta_new_'):  # Detectar nuevas preguntas
                nueva_pregunta = Pregunta.objects.create(
                    encuesta=encuesta,
                    texto=value
                )

                # Procesar respuestas para la nueva pregunta
                for opcion_key, opcion_value in request.POST.items():
                    if opcion_key.startswith(f'respuesta_new_{key.split("_")[-1]}'):
                        Respuesta.objects.create(
                            pregunta=nueva_pregunta,
                            texto=opcion_value
                        )

        # Renderizar con éxito
        return render(request, 'editar_encuesta_form.html', {
            'encuesta': encuesta,
            'preguntas': encuesta.preguntas.all(),  # Refrescar las preguntas
            'success': True
        })

    # Si no es POST, renderizar el formulario inicial
    return render(request, 'editar_encuesta_form.html', {
        'encuesta': encuesta,
        'preguntas': preguntas
    })

@login_required
def editar_encuesta(request):
    # Obtiene todas las encuestas disponibles
    encuestas = Encuesta.objects.all()
    return render(request, 'editar_encuesta.html', {'encuestas': encuestas})

@login_required
def borrar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    encuesta.delete()
    return redirect('editar_encuesta_list')
@login_required
def compartir_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    preguntas = encuesta.preguntas.prefetch_related('respuestas').all()

    if request.method == 'POST':
        # Aquí puedes manejar la lógica para guardar las respuestas enviadas por el usuario.
        for pregunta in preguntas:
            respuesta_id = request.POST.get(f'pregunta_{pregunta.id}')
            if respuesta_id:
                # Guarda la respuesta seleccionada por el usuario.
                print(f"Pregunta {pregunta.id} - Respuesta {respuesta_id}")
                # Implementa tu lógica de almacenamiento aquí.

        # Opcional: redirige a una página de agradecimiento
        return render(request, 'gracias.html', {'encuesta': encuesta})

    return render(request, 'llenar_encuesta.html', {'encuesta': encuesta, 'preguntas': preguntas})


def llenar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)
    preguntas = encuesta.preguntas.all()

    if request.method == 'POST':
        # Imprime todos los datos enviados por el formulario
        print("Datos POST recibidos:", request.POST)

        # Aquí continúa el resto del código como está
        for pregunta in preguntas:
            respuesta_id = request.POST.get(f'pregunta_{pregunta.id}')
            print(f"Procesando Pregunta {pregunta.id} - Respuesta {respuesta_id}")  # Depuración extra
            if respuesta_id:
                try:
                    RespuestaUsuario.objects.create(
                        encuesta=encuesta,
                        pregunta=pregunta,
                        respuesta_id=respuesta_id,
                        usuario=request.user.username if request.user.is_authenticated else "Anónimo"
                    )
                    print(f"Guardado exitoso: Pregunta {pregunta.id}, Respuesta {respuesta_id}")
                except Exception as e:
                    print(f"Error al guardar la respuesta: {e}")
        return redirect('gracias')

    return render(request, 'llenar_encuesta.html', {
        'encuesta': encuesta,
        'preguntas': preguntas,
    })


def seleccionar_encuesta(request):
    # Obtener todas las encuestas
    encuestas = Encuesta.objects.all()
    return render(request, 'seleccionar_encuesta.html', {
        'encuestas': encuestas
    })






