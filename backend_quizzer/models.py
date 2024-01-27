from django.db import models


class QuizFile(models.Model):
    user = models.ForeignKey("backend_users.User", null=True, related_name="quizzes", on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True, blank=True)
    file = models.FileField(upload_to="quiz_uploads/", null=True)

    def delete(self, *args, **kwargs):
        self.file.close()
        self.file.delete()
        super(QuizFile, self).delete(*args, **kwargs)
