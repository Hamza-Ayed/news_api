from django.shortcuts import render
from rest_framework.views import APIView
from django.utils import timezone
import dateparser

# Create your views here.
from rest_framework import generics
from .models import News
from .serializers import NewsSerializer
import requests
from bs4 import BeautifulSoup
import json
from rest_framework import status
from rest_framework.response import Response


# from urllib.parse import urljoin


def goalDesc(relative_url):
    url = relative_url
    response1 = requests.get(url)
    soup1 = BeautifulSoup(response1.content, "html.parser")
    try:
        desc = soup1.find("div", class_="article_content__XFYIz").text.strip()
        print(desc)
        return desc
    except AttributeError:
        print(f"No description found for {url}")


class NewsList(generics.ListCreateAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all().order_by("-pub_date")
        search_query = self.request.query_params.get("search", None)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        count = queryset.count()
        data = {"count": count, "results": serializer.data}
        return Response(data)


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = "pk"


class Scrap(generics.ListCreateAPIView):
    pass


def descSport360(sport360Url):
    response2 = requests.get(sport360Url)
    soup2 = BeautifulSoup(response2.content, "html.parser")
    try:
        desc = soup2.find_all("p")
        # Extract text from each paragraph and join them
        desc_text = " ".join([p.text.strip() for p in desc])
        print(desc_text)
        return desc_text
    except AttributeError:
        print(f"No description found for {sport360Url}")


def descBeinSport(relative_url):
    response2 = requests.get(relative_url)
    soup2 = BeautifulSoup(response2.content, "html.parser")
    try:
        desc = soup2.find_all("p")
        # Extract text from each paragraph and join them
        desc_text = " ".join([p.text.strip() for p in desc])
        print(desc_text)

        return desc_text
    except AttributeError:
        print(f"No description found for {relative_url}")


class beinSports(APIView):
    serializer_class = NewsSerializer

    def get(self, request):
        url = "https://www.beinsports.com/ar/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("section", class_="cluster_1 block-cluster")
        data = []
        for article in articles:
            title = article.find("h2", class_="cluster-Latest__title1").text.strip()
            link = "https://www.beinsports.com" + article.find("a")["href"]
            description = descBeinSport(link)
            pub_date = timezone.now()
            image = article.find("data-src")

            news_obj, created = News.objects.get_or_create(
                link=link,
                defaults={
                    "title": title,
                    "description": description,
                    "pub_date": pub_date,
                    "image": image
                }
            )

        if not created:
            news_obj.title = title
            news_obj.description = description
            news_obj.pub_date = pub_date
            news_obj.image = image
            news_obj.save()

        # Save all objects in the database
        News.objects.bulk_create(data)

        serializer = NewsSerializer(data, many=True)
        return Response(serializer.data)


class Sport360(APIView):
    def get(self, request):
        url = "https://arabic.sport360.com/all-stories"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("div", class_="v-item")
        data = []
        for article in articles:
            title = article.find("h3").text.strip()
            link = article.find("a")["href"]
            description = descSport360(link)
            pub_date_str = article.find("em").text.strip()
            pub_date = dateparser.parse(pub_date_str)
            if pub_date:
                pub_date = pub_date.astimezone(timezone.utc).replace(tzinfo=None)
            else:
                pub_date = timezone.now()
            image = article.find("img")["src"]
            try:
                news_obj = News.objects.get(link=link)
                # Update fields if News object already exists
                news_obj.title = title
                news_obj.description = description
                news_obj.pub_date = pub_date
                news_obj.image = image
                news_obj.save()
            except News.DoesNotExist:
                # Create a new News object if it does not exist
                news_obj = News.objects.create(
                    title=title,
                    link=link,
                    description=description,
                    pub_date=pub_date,
                    image=image,
                )
            data.append(news_obj)

        serializer = NewsSerializer(data, many=True)
        return Response(serializer.data)


class GoalNewsAdd(APIView):
    def get(self, request):
        url = "https://www.goal.com/ar/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1/1"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("li", class_="item")
        data = []
        for article in articles:
            h3_element = article.find("h3")
            if h3_element:
                title = h3_element.text.strip()
            else:
                title = 'None'

            # title = article.find("h3", class_="title h5").text.strip()
            link = "https://www.goal.com" + article.find("a")["href"]
            description = goalDesc(link)
            pub_date = article.find("time")["datetime"]
            image = article.find("img")["src"]

            news_obj, created = News.objects.get_or_create(
                image=image,
                defaults={
                    "title": title,
                    "description": description,
                    "pub_date": pub_date,
                    "link": link,
                },
            )
            # Update fields if News object already existed
            if not created:
                news_obj.title = title
                news_obj.description = description
                news_obj.pub_date = pub_date
                news_obj.link = link
                news_obj.save()

        serializer = NewsSerializer(data, many=True)
        return Response(serializer.data)


class NewsDeleteAll(APIView):
    def delete(self, request):
        News.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WordPress(APIView):
    def get(self, request):
        urls = [
            "https://hihi2.com/wp-json/wp/v2/posts?per_page=100",
            "https://www.belgoal.com/wp-json/wp/v2/posts?per_page=100",
            # "https://example.com/wp-json/wp/v2/posts?per_page=100",
            # Add more URLs as needed
        ]

        for url in urls:
            response = requests.get(url)
            data = json.loads(response.text)
            for post in data:
                # Extract relevant fields from JSON response
                title = post["title"]["rendered"]
                description = post["content"]["rendered"]
                pub_date = post["modified"]
                image = post["link"]

                # Check if News object with same image already exists
                news_obj, created = News.objects.get_or_create(
                    image=image,
                    defaults={
                        "title": title,
                        "description": description,
                        "pub_date": pub_date,
                    },
                )
                # Update fields if News object already existed
                if not created:
                    news_obj.title = title
                    news_obj.description = description
                    news_obj.pub_date = pub_date
                    news_obj.save()

        return Response({"success": "News objects created successfully"})


class youm7sport(APIView):
    serializer_class = NewsSerializer

    def get(self, request):
        url = "https://www.youm7.com/Section/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D8%A9/298/1"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("div", class_="col-xs-12 bigOneSec")
        data = []
        for article in articles:
            title = article.find('h3').text.strip()
            link = 'https://www.youm7.com/' + article.find("a")["href"]
            description = article.find('p').text.strip()
            pub_date = article.find('span', class_='newsDate2').text.strip()
            image = article.find('img')['src']

            news_obj, created = News.objects.get_or_create(
                link=link,
                defaults={
                    "title": title,
                    "description": description,
                    "pub_date": pub_date,
                    "image": image
                }
            )

        if not created:
            news_obj.title = title
            news_obj.description = description
            news_obj.pub_date = pub_date
            news_obj.image = image
            news_obj.save()

        # Save all objects in the database
        News.objects.bulk_create(data)

        serializer = NewsSerializer(data, many=True)
        return Response(serializer.data)


class dawriSaudi(APIView):
    serializer_class = NewsSerializer

    def get(self, request):
        url = "https://www.dawriplus.com/news.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("div", class_="video-smallbox")
        data = []
        for article in articles:

            link = article.find("a")["href"]
            response = requests.get(link)
            soup = BeautifulSoup(response.content, "html.parser")

            articles = soup.find("div", class_="news-detail-main")
            title=articles.find('h3').text.strip()
            # image=articles.find('div',class_='banner').text.strip()
            style = soup.select_one('.banner')['style']
            image = [link.strip("')") for link in style.split("url('")[1:]]
            pub_date=article.find('span').text.strip()
            try:
                desc = soup.find_all("p")
                # Extract text from each paragraph and join them
                description = ' '.join([p.text.strip() for p in desc])
                print('desc_short : '+description)
                #  return desc_text
            except AttributeError:
                print(f"No description found for {url}")


            news_obj, created = News.objects.get_or_create(
                link=link,
                defaults={
                    "title": title,
                    "description": description,
                    "pub_date": pub_date,
                    "image": image
                }
            )

        if not created:
            news_obj.title = title
            news_obj.description = description
            news_obj.pub_date = pub_date
            news_obj.image = image
            news_obj.save()

        # Save all objects in the database
        News.objects.bulk_create(data)

        serializer = NewsSerializer(data, many=True)
        return Response(serializer.data)