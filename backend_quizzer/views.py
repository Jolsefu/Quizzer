from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import json

from .serializers import QuizFileSerializer

from .models import QuizFile


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_file(request, id):
    """
    Let's the users delete quiz files
    """

    quiz_file = QuizFile.objects.get(pk=id)

    if not quiz_file.user == request.user:
        return Response({"error": "You are not the owner of the quiz file."}, status=status.HTTP_400_BAD_REQUEST)

    quiz_file.delete()

    return Response({"success": f"The file was deleted successfully."})

@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_file(request):
    """
    Lets the user update their saved quiz files on the database
    via the Quizzer's Create
    """

    quiz_file = QuizFile.objects.get(pk=request.data["id"])

    if not quiz_file.user == request.user:
        return Response({"error": "You are not the owner of the quiz file."}, status=status.HTTP_400_BAD_REQUEST)

    with open(quiz_file.file.path, "w") as f:
        json.dump(request.data["json"], f)

    return Response({"success": f"The file was updated successfully."})

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """
    Lets the user save files to their own database
    """

    try:
        json.loads(request.data["file"].read())
    except ValueError:
        return Response({"error": "Uploaded file is not a valid JSON."})

    serializer = QuizFileSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()

        return Response({"success": "Uploaded file successfully!"}, status=status.HTTP_200_OK)

    return Response({"error": serializer.errors}, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_file(request, id):
    """
    Responsible for sending quiz files as json format

    Used for quiz file downloads, and quizzes purposes on the frontend
    """

    quiz_file = QuizFile.objects.get(user=request.user, pk=id)

    if not quiz_file.user == request.user:
        return Response({"error": "You are not the owner of the quiz file."})

    try:
        json_file = json.loads(quiz_file.file.open().read())
    except json.decoder.JSONDecodeError:
        quiz_file.delete()
        
        return Response(
            {"error": "The file was deleted from the database because it was corrupted."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(json_file, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_files(request):
    """
    Sends a list of saved files of quizzes of the current user from the database
    """

    quiz_files = QuizFile.objects.filter(user=request.user)

    data = {"files": []}
    for quiz_file in quiz_files:
        try:
            name = json.loads(quiz_file.file.open().read())["info"]["name"]
        except json.decoder.JSONDecodeError:
            quiz_file.delete()

            return Response(
                {"error": "A file was deleted from the database because it was corrupted."}, 
                status=status.HTTP_200_OK
            )

        data["files"].append({
            "id": quiz_file.pk,
            "dt": quiz_file.dt,
            "name": name
        })

    return Response(data, status=status.HTTP_200_OK)
