---
layout: page
title: "Blog"
subtitle: "learning notes & essays"
css: "/assets/css/blog.css"
share-img: /assets/img/og-preview.png
share-title: "Victoria Zhang | Posts"
share-description: "List of all the blogs by Victoria Zhang."
support_promo_box: true
cover-img:
  - "/assets/img/photograph/forest.jpg" : "Yosemite, CA (2021)"
---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Y06S3E3WTE"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-Y06S3E3WTE');
</script>

<div class="list-filters">
  <a href="/blog" class="list-filter filter-selected">All</a>
  <a href="/tutorials" class="list-filter">Learning Blog</a>
  <a href="/essays" class="list-filter">Essays</a>
  <a href="/tags" class="list-filter">Index</a>
</div>

<style>
.section-heading {
  margin-top: 2.4rem;
  margin-bottom: 1rem;
  padding-bottom: 0.4rem;
  border-bottom: 2px solid #d0d7de;
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.5rem;
}
.section-heading .section-meta {
  font-size: 0.85rem;
  color: #7f8c8d;
  font-weight: 400;
  margin-left: 0.5rem;
}
.post-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 18px;
  margin-bottom: 1.5rem;
}
.post-card {
  display: flex;
  flex-direction: column;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.post-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 18px rgba(0,0,0,0.1);
}
.post-card-thumb {
  width: 100%;
  height: 150px;
  background: linear-gradient(135deg, #fafafa 0%, #eaeef2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.post-card-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.post-card-thumb .placeholder-icon {
  font-size: 3em;
  color: #b0b8c1;
}
.post-card-body {
  padding: 14px 16px 16px;
  display: flex;
  flex-direction: column;
  flex: 1;
}
.post-card-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.3;
  margin-bottom: 6px;
}
.post-card-title a {
  color: inherit;
  text-decoration: none;
}
.post-card-title a:hover {
  color: #2c5282;
}
.post-card-subtitle {
  font-size: 0.88rem;
  color: #5a6c7d;
  margin-bottom: 10px;
  line-height: 1.4;
}
.post-card-meta {
  margin-top: auto;
  font-size: 0.78rem;
  color: #7f8c8d;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}
.post-card-meta .post-date {
  font-weight: 500;
}
.post-card-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  background: #eef2f5;
  color: #4a5568;
  font-size: 0.72rem;
  text-decoration: none;
}
.post-card-tag:hover {
  background: #d8dfe5;
}
</style>

{% assign date_format = site.date_format | default: "%B %-d, %Y" %}

{% capture render_card %}{% endcapture %}

{% comment %} Learning Blog / Tutorials section {% endcomment %}
<h2 class="section-heading">Learning Blog <span class="section-meta">tutorials & technical notes</span></h2>
<div class="post-card-grid">
  {% assign professional_posts = site.tags.tutorials | sort: 'date' | reverse %}
  {% for post in professional_posts %}
  <article class="post-card">
    {%- capture thumbnail -%}
      {% if post.thumbnail-img %}{{ post.thumbnail-img }}
      {% elsif post.cover-img %}{% if post.cover-img.first %}{{ post.cover-img[0].first.first }}{% else %}{{ post.cover-img }}{% endif %}
      {% endif %}
    {%- endcapture -%}
    {% assign thumbnail = thumbnail | strip %}
    <div class="post-card-thumb">
      {% if thumbnail != "" %}
        <a href="{{ post.url | absolute_url }}" aria-label="Thumbnail"><img src="{{ thumbnail | absolute_url }}" alt="thumbnail"></a>
      {% else %}
        <span class="placeholder-icon"><i class="fas fa-book-open"></i></span>
      {% endif %}
    </div>
    <div class="post-card-body">
      <div class="post-card-title"><a href="{{ post.url | absolute_url }}">{{ post.title }}</a></div>
      {% if post.subtitle %}<div class="post-card-subtitle">{{ post.subtitle }}</div>{% endif %}
      <div class="post-card-meta">
        <span class="post-date">{{ post.date | date: date_format }}</span>
        {% for tag in post.tags %}<a class="post-card-tag" href="{{ '/tags' | absolute_url }}#{{- tag -}}">{{ tag }}</a>{% endfor %}
      </div>
    </div>
  </article>
  {% endfor %}
</div>

{% comment %} Essays section {% endcomment %}
<h2 class="section-heading">Inner Mind <span class="section-meta">words have power</span></h2>
<div class="post-card-grid">
  {% assign essay_posts = site.tags.essays | sort: 'date' | reverse %}
  {% for post in essay_posts %}
  <article class="post-card">
    {%- capture thumbnail -%}
      {% if post.thumbnail-img %}{{ post.thumbnail-img }}
      {% elsif post.cover-img %}{% if post.cover-img.first %}{{ post.cover-img[0].first.first }}{% else %}{{ post.cover-img }}{% endif %}
      {% endif %}
    {%- endcapture -%}
    {% assign thumbnail = thumbnail | strip %}
    <div class="post-card-thumb">
      {% if thumbnail != "" %}
        <a href="{{ post.url | absolute_url }}" aria-label="Thumbnail"><img src="{{ thumbnail | absolute_url }}" alt="thumbnail"></a>
      {% else %}
        <span class="placeholder-icon"><i class="fas fa-feather"></i></span>
      {% endif %}
    </div>
    <div class="post-card-body">
      <div class="post-card-title"><a href="{{ post.url | absolute_url }}">{{ post.title }}</a></div>
      {% if post.subtitle %}<div class="post-card-subtitle">{{ post.subtitle }}</div>{% endif %}
      <div class="post-card-meta">
        <span class="post-date">{{ post.date | date: date_format }}</span>
        {% for tag in post.tags %}<a class="post-card-tag" href="{{ '/tags' | absolute_url }}#{{- tag -}}">{{ tag }}</a>{% endfor %}
      </div>
    </div>
  </article>
  {% endfor %}
</div>
