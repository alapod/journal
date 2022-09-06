from django.views import generic
from .models import Post
from .forms.forms import PostForm
from django.views.generic.edit import FormView
from django.template.defaultfilters import slugify
from transformers import pipeline


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


class NewPostView(FormView):
    template_name = 'new_post.html'
    form_class = PostForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        sentiment = get_sentiment(self.request.POST['content'])
        new_post = Post(title=self.request.POST['title'], content=self.request.POST['content'],
                        author=self.request.user, slug=slugify(self.request.POST['title']),
                        status=1, sentiment=sentiment)
        new_post.save()
        form.send_email()
        return super().form_valid(form)


def get_sentiment(text):
    sentiment_pipeline = pipeline("sentiment-analysis")
    label = sentiment_pipeline(text)[0]['label']
    return int(label == 'POSITIVE')
