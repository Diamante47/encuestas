from django.db import models

class Encuesta(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Pregunta(models.Model):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto


class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas')
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto


class RespuestaUsuario(models.Model):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=255, blank=True, null=True)  # Puede ser "Anónimo"

    def __str__(self):
        return f"{self.usuario} - {self.pregunta.texto} - {self.respuesta.texto}"


