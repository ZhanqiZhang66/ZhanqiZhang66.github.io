---
layout: page
title: "Hi, I'm Victoria"
subtitle: Researcher in Artificial and Biological Intelligence. Bird Lover.
css: "/assets/css/index.css"
share-img: /assets/img/victoria.jpg
share-title: "Victoria Zhang | Popular posts"
share-description: "List of all the most popular posts by Victoria Zhang."
support_promo_box: true
cover-img:
  - "/assets/img/big-imgs/balboa.JPEG" : "Balboa Park, San Diego (2022)"
  - "/assets/img/big-imgs/bird.jpeg" : "Forest Park, Saint Louis, MO (2021)"
  - "/assets/img/big-imgs/cherry.JPG" : "WashU, Saint Louis, MO (2020)"
  - "/assets/img/big-imgs/child.JPG" : "Jinan, China (2000)"
  - "/assets/img/big-imgs/child_2.JPG" : "Jinan, China (2002)"
  - "/assets/img/big-imgs/dog_2.JPG" : "Creve Coeur Lake. Saint Louis, MO (2018)"
  - "/assets/img/big-imgs/grad_fountain.jpeg" : "WashU Brookings Quadrangle, Saint Louis, MO (2020)"
  - "/assets/img/big-imgs/seaside.JPG" : "Sunset Cliffs, La Jolla, CA (2021)"
  - "/assets/img/big-imgs/yosemite_2.JPEG" : "Yosemite Valley, Yosemite National Park, CA (2022)"
  - "/assets/img/big-imgs/river.jpg" : "Jinan, China (2018)"
  - "/assets/img/big-imgs/freshman.JPG" : "WashU, Saint Louis, MO (2016)"
  - "/assets/img/big-imgs/sea.jpeg" : "La Jolla tide pool, La Jolla, CA (2022)"
  - "/assets/img/big-imgs/chinohill.JPEG" : "Chino Hills State Park, Chino Hills, CA (2023)"
  - "/assets/img/big-imgs/ironmountain.JPG" : "Iron Mountain Trail, Poway, CA (2023)"
  - "/assets/img/big-imgs/ski.jpeg" : "Palisade, Tahoe, CA (2023)"
  - "/assets/img/big-imgs/jeju.JPG" : "Jeju, South Korea (2018)"
---

<div class="list-filters">
  <a href="/" class="list-filter">All posts</a>
  <a href="/popular" class="list-filter filter-selected">Most Popular</a>
  <a href="/tutorials" class="list-filter">Tutorials</a>
  <a href="/tags" class="list-filter">Index</a>
</div>

{% assign posts = paginator.posts | default: site.posts %}

<div class="posts-list">
  {% for post in posts %}
  <article class="post-preview">

    {%- capture thumbnail -%}
      {% if post.thumbnail-img %}
        {{ post.thumbnail-img }}
      {% elsif post.cover-img %}
        {% if post.cover-img.first %}
          {{ post.cover-img[0].first.first }}
        {% else %}
          {{ post.cover-img }}
        {% endif %}
      {% else %}
      {% endif %}
    {% endcapture %}
    {% assign thumbnail=thumbnail | strip %}

    {% if site.feed_show_excerpt == false %}
    {% if thumbnail != "" %}
    <div class="post-image post-image-normal">
      <a href="{{ post.url | absolute_url }}" aria-label="Thumbnail">
        <img src="{{ thumbnail | absolute_url }}" alt="Post thumbnail">
      </a>
    </div>
    {% endif %}
    {% endif %}

    <a href="{{ post.url | absolute_url }}">
      <h2 class="post-title">{{ post.title }}</h2>

      {% if post.subtitle %}
        <h3 class="post-subtitle">
        {{ post.subtitle }}
        </h3>
      {% endif %}
    </a>

    <p class="post-meta">
      {% assign date_format = site.date_format | default: "%B %-d, %Y" %}
      Posted on {{ post.date | date: date_format }}
    </p>

    {% if thumbnail != "" %}
    <div class="post-image post-image-small">
      <a href="{{ post.url | absolute_url }}" aria-label="Thumbnail">
        <img src="{{ thumbnail | absolute_url }}" alt="Post thumbnail">
      </a>
    </div>
    {% endif %}

    {% unless site.feed_show_excerpt == false %}
    {% if thumbnail != "" %}
    <div class="post-image post-image-short">
      <a href="{{ post.url | absolute_url }}" aria-label="Thumbnail">
        <img src="{{ thumbnail | absolute_url }}" alt="Post thumbnail">
      </a>
    </div>
    {% endif %}

    <div class="post-entry">
      {% assign excerpt_length = site.excerpt_length | default: 50 %}
      {{ post.excerpt | strip_html | xml_escape | truncatewords: excerpt_length }}
      {% assign excerpt_word_count = post.excerpt | number_of_words %}
      {% if post.content != post.excerpt or excerpt_word_count > excerpt_length %}
        <a href="{{ post.url | absolute_url }}" class="post-read-more">[Read&nbsp;More]</a>
      {% endif %}
    </div>
    {% endunless %}

    {% if site.feed_show_tags != false and post.tags.size > 0 %}
    <div class="blog-tags">
      Tags:
      {% for tag in post.tags %}
      <a href="{{ '/tags' | absolute_url }}#{{- tag -}}">{{- tag -}}</a>
      {% endfor %}
    </div>
    {% endif %}

   </article>
  {% endfor %}
</div>

{% if paginator.total_pages > 1 %}
<ul class="pagination main-pager">
  {% if paginator.previous_page %}
  <li class="page-item previous">
    <a class="page-link" href="{{ paginator.previous_page_path | absolute_url }}">&larr; Newer Posts</a>
  </li>
  {% endif %}
  {% if paginator.next_page %}
  <li class="page-item next">
    <a class="page-link" href="{{ paginator.next_page_path | absolute_url }}">Older Posts &rarr;</a>
  </li>
  {% endif %}
</ul>
{% endif %}