from .fetcher import News
from .models import Archive
from .serializers import ArchiveSerializer
from datetime import timedelta
from NewsAggregator.settings import REDIS_HOST, REDIS_PORT, REDIS_DB
from redis import Redis
from rest_framework import generics, permissions, status
from rest_framework.response import Response

# Create your views here.


class ArchiveList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArchiveSerializer

    def get_queryset(self):
        # must not use both .all() and .get_queryset()
        return Archive.objects.all()

    def get_serializer_class(self):
        return self.serializer_class


# last ten news ordered by id that inherit from ArchiveList
class ArchiveListLT(ArchiveList):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-id")[:10][::-1]


class ArchiveCreate(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

    def get(self, request, *args, **kwargs):
        redis_instance = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

        if redis_instance.get("data_inserted"):
            remaining_time = int(str(redis_instance.ttl("data_inserted")))
            if remaining_time >= 0:
                remaining_time = datetime.timedelta(seconds=remaining_time)
                remaining_time_str = str(remaining_time)
                message = f"Skipped insertion. Data already exists. Key will expire in {remaining_time_str}."
            else:
                message = "Skipped insertion. Data already exists. Key has expired."
            return Response(message, status=status.HTTP_409_CONFLICT)

        # fetching data from the News class
        news = News.irna_news()
        skipped = False

        for data in news:
            title = data["title"]
            author = data["author"]
            publish_date = data["publish date"]

            if Archive.objects.filter(title=title).exists():
                skipped = True
                # Skip insertion if news already exists
                continue

            Archive.objects.create(
                title=title, author=author, publish_date=publish_date
            )

        if skipped:
            response_code = status.HTTP_409_CONFLICT
            remaining_time = int(str(redis_instance.ttl("data_inserted")))
            if remaining_time >= 0:
                remaining_time = timedelta(seconds=remaining_time)
                remaining_time_str = str(remaining_time)
                message = f"Skipped insertion. Data already exists. Key will expire in {remaining_time_str}."
            else:
                message = "Skipped insertion. Data already exists. Key has expired."
            response_data = message
        else:
            # Set key to indicate data insertion with a TTL of 45 seconds
            redis_instance.setex("data_inserted", 45, 1)
            response_code = status.HTTP_201_CREATED
            response_data = "Data inserted successfully."

        return Response(response_data, response_code)
