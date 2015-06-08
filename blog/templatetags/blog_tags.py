from django import template
from ..models import Comment
from ..utils import utils
from django.template import Context, Template

register = template.Library()


@register.simple_tag(takes_context=True)
def current_time(context, format_string):
    user = context['user']
    return user

#TODO: Fix recursive close feature
@register.simple_tag()
def show_comments(post):

	#Closure to find child comments recursively
	def insert_children(html, comment_template, post, parent, margin_left):
		children_comments = Comment.objects.filter(post=post, answer_to=parent.id).order_by('-date')
		if children_comments:
			for child in children_comments:
				margin_left[child.id] = margin_left[parent.id] + 50
				grand_children_number = Comment.objects.filter(post=post, answer_to=child.id).count()
				child_context = Context({'post_id': post.id, 'photo_url': child.author.photo.url if child.author.photo else '', 'author': child.author.user.username, 'date': child.date, 'text': child.text, 'comment_id': child.id, 'parent_comment_id': parent.id, 'children_number': grand_children_number, 'margin_left': margin_left[child.id], 'display': 'none'})
				html[0] += comment_template.render(child_context)

				insert_children(html, comment_template, post, child, margin_left)

	#HTML content to be appended for each comment		
	comment_html = """
		{% load i18n %}
		{% load staticfiles %}
		<div class="media parent-div-{{ parent_comment_id }}" style="margin-left: {{ margin_left }}px; display: {{ display }};">
		    <a class="pull-left" href="#">
		    	{% if photo_url %}
			    	<img class="media-object not-3d-img" src="{{ photo_url }}" alt="" width="100" height="100">
			    {% else %}
			    	<img class="media-object not-3d-img" src="{% static 'blog/images/anonymous.jpg' %}" alt="" width="100" height="100">
			    {% endif %}
		    </a>
		    <div class="media-body">
		        <h4 class="media-heading">
		        	<label>{{ author }}</label> 
		            <small> {% trans "at" %}  {{ date }} </small>
		        </h4>
		        {{ text }}
		        <hr>
		    </div>
		    <a id="link-respond-{{ comment_id }}"> Respond </a>
		    {% if children_number > 0 %}
		    	<a id="link-answers-{{ comment_id }}" style="margin-left: 50px"> (See answers) </a>
		    {% endif %}
		    <div id="div-answer-{{ comment_id }}" style="display: none;">
			    <hr>
			    <div class="col-lg-10 col-lg-offset-2 col-md-10 col-md-offset-1">
				    <div class="well">
					    <h4>Leave a Comment:</h4>
					    
					    <form action="/send_answer_to_comment/{{ post_id }}/{{ comment_id }}/" method="post">
						    {{ form }}
						    <div class="form-group">
					        	<textarea id="answer-text-{{ comment_id }}" name="answer-text-{{ comment_id }}" class="form-control" rows="3" rows="5" class="form-control" placeholder="Comment" required data-validation-required-message="Please enter your answer."></textarea>
					        	<label id="answer-to-{{ comment_id }}" style="display: none;"> {{ parent_comment_id }} </label>
					    	</div>
					    	<div id="answer-success-{{ comment_id }}"></div>
				    		<button id="answer-btn-{{ comment_id }}" name="answer-btn-{{ comment_id }}" type="submit" class="btn btn-default">Send</button>
						</form>
					</div>	
				</div>	
			</div>	
		</div>

		<script type="text/javascript">
			$("#link-respond-{{ comment_id }}").click(function() {
				var display = $("#div-answer-{{ comment_id }}").css("display") === "none" ? "block" : "none";
				$("#div-answer-{{ comment_id }}").css("display", display);
  			});
			$("#link-answers-{{ comment_id }}").click(function() {
				var display = $(".parent-div-{{ comment_id }}").first().css("display") === "none" ? "block" : "none";
				$(".parent-div-{{ comment_id }}").css("display", display);
  			});
		</script>
	"""

	comment_template = Template(comment_html)
	margin_left = {}
	html = [""]

	parent_comments = Comment.objects.filter(post=post, answer_to=None).order_by('-date')
	if not parent_comments:
		comment_template = Template("<h4 id='no-comments' class='media-heading'> No comments were left here yet. Be the first to comment!</h4>")
		return comment_template.render(Context())

	for parent in parent_comments:
		margin_left[parent.id] = 0
		children_number = Comment.objects.filter(post=post, answer_to=parent.id).count()
		context = Context({'post_id': post.id, 'photo_url': parent.author.photo.url if parent.author.photo else '', 'author': parent.author.user.username,'date': parent.date, 'text': parent.text, 'comment_id': parent.id, 'parent_comment_id': 0, 'children_number':children_number, 'margin_left': margin_left[parent.id], 'display': 'block' })
		html[0] += comment_template.render(context)
		
		insert_children(html, comment_template, post, parent, margin_left)

	return html[0] 




