---
layout: page
title: "Sitemap"
permalink: /sitemap/
---

A list of all the posts and pages found on the site. For you robots out there is an [XML version](/sitemap.xml) available for digesting as well.

<h2>Posts</h2>
<ul>
  {% for post in site.posts %}
    <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

<h2>Pages</h2>
<ul>
  {% for page in site.pages %}
    {% if page.url != '/' and page.url != '/404.html' and page.url != '/sitemap/' %}
      <li><a href="{{ page.url | relative_url }}">{{ page.title | default: page.name }}</a></li>
    {% endif %}
  {% endfor %}
</ul>