import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .utils import get_video_details, extract_frames
from django.shortcuts import render
import os

class VideoProcessAPIView(APIView):
   def post(self, request):
       # Extract video name from the request
       video_name = request.data.get("video_name")
       if not video_name:
           return Response({"error": "Video name is required."}, status=status.HTTP_400_BAD_REQUEST)
       # Build the full path to the video
       video_path = os.path.join(settings.MEDIA_ROOT, "videos", video_name)
       if not os.path.exists(video_path):
           return Response({"error": f"Video '{video_name}' not found."}, status=status.HTTP_404_NOT_FOUND)
       try:
           # Get video details
           video_details = get_video_details(video_path)
           # Extract frames per minute
           output_dir = os.path.join(settings.MEDIA_ROOT, "frames")
           frames = extract_frames(video_path, output_dir)
           return Response({
               "duration_seconds": video_details["duration_seconds"],
               "duration_minutes": int(video_details["duration_seconds"] // 60),
               "frames": frames,
           })
       except Exception as e:
           return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
def test_api_view(request):
   response = None
   if request.method == "POST":
       video_name = request.POST.get("video_name")
       video_path = os.path.join(settings.MEDIA_ROOT, "videos", video_name)
       if not os.path.exists(video_path):
           response = {"error": f"Video '{video_name}' not found."}
       else:
           try:
               # Get video details
               video_details = get_video_details(video_path)
               # Extract frames
               output_dir = os.path.join(settings.MEDIA_ROOT, "frames")
               frames = extract_frames(video_path, output_dir)
               response = {
                   "duration_seconds": video_details["duration_seconds"],
                   "duration_minutes": int(video_details["duration_seconds"] // 60),
                   "frames": frames,
               }
           except Exception as e:
               response = {"error": str(e)}
   return render(request, "video_processor/test_api.html", {"response": response})