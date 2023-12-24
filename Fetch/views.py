from .fetcher import News
from .models import Archive
from .serializers import ArchiveSerializer
import datetime
from NewsAggregator.settings import REDIS_HOST, REDIS_PORT, REDIS_DB
from redis import Redis
from rest_framework import generics, permissions, status
from rest_framework.response import Response

# Create your views here.

class ArchiveList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArchiveSerializer
    
    def get_queryset(self):
        return Archive.objects.all()  # must not use both .all() and .get_queryset()

    def get_serializer_class(self):
        return self.serializer_class
    

class ArchiveListLT(ArchiveList):  # last ten news ordered by id that inherit from ArchiveList
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-id')[:10][::-1]


class ArchiveCreate(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

    def get(self, request, *args, **kwargs):
        
        redis_instance = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

        if redis_instance.get('data_inserted'):
            remaining_time = int(str(redis_instance.ttl('data_inserted')))
            if remaining_time >= 0:
                remaining_time = datetime.timedelta(seconds=remaining_time)
                remaining_time_str = str(remaining_time)
                message = f"Skipped insertion. Data already exists. Key will expire in {remaining_time_str}."
            else:
                message = "Skipped insertion. Data already exists. Key has expired."
            return Response(message, status=status.HTTP_409_CONFLICT)

        news = News.irna_news()  # Fetching data from the News class
        skipped = False

        for data in news:
            title = data['title']
            author = data['author']
            publish_date = data['publish date']

            if (Archive.objects.filter(title=title).exists() and
                Archive.objects.filter(author=author).exists() and
                Archive.objects.filter(publish_date=publish_date).exists()):
                skipped = True
                continue  # Skip insertion if news already exists

            Archive.objects.create(
                title=title,
                author=author,
                publish_date=publish_date
            )

        if skipped:
            response_code = status.HTTP_409_CONFLICT
            remaining_time = int(str(redis_instance.ttl('data_inserted')))
            if remaining_time >= 0:
                remaining_time = datetime.timedelta(seconds=remaining_time)
                remaining_time_str = str(remaining_time)
                message = f"Skipped insertion. Data already exists. Key will expire in {remaining_time_str}."
            else:
                message = "Skipped insertion. Data already exists. Key has expired."
            response_data = message
        else:
            redis_instance.setex('data_inserted', 45, 1)  # Set key to indicate data insertion with a TTL of 45 seconds
            response_code = status.HTTP_201_CREATED
            response_data = "Data inserted successfully."

        return Response(response_data, response_code)
    