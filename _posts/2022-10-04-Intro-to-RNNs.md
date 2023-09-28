---
layout: post
title: Intro to Recurrent Neural Networks (RNNs)
subtitle: Part I
gh-repo: zhanqizhang66/zhanqizhang66.github.io/
gh-badge: [star, fork, follow]
cover-img: /assets/img/photograph/281AB3B5-547A-4CE3-BDAF-E0C43AEC29DE.jpg
thumbnail-img:
share-img: /assets/img/photograph/281AB3B5-547A-4CE3-BDAF-E0C43AEC29DE.jpg
tags: [learning notes]
---


<h2>Intro to Recurrent Neural Networks (RNNs)</h2>

* Before RNNs: Perceptron and ConvNets
* RNNs, and Why?
* Some Math
  * Forward pass
  * Backpropagation refresher
  * The RNN backward pass
* Some pros and cons
* On the difficulty of training RNNs
* Applications



<iframe width="100%" height="800" src="/files/Intro to RNNs.pdf">
<!-- This is a demo post to show you how to write blog posts with markdown.  I strongly encourage you to [take 5 minutes to learn how to write in markdown](https://markdowntutorial.com/) - it'll teach you how to transform regular text into bold/italics/headings/tables/etc.

**Here is some bold text**

## Here is a secondary heading

Here's a useless table:

| Number | Next number | Previous number |
| :------ |:--- | :--- |
| Five | Six | Four |
| Ten | Eleven | Nine |
| Seven | Eight | Six |
| Two | Three | One |


How about a yummy crepe?

![Crepe](https://s3-media3.fl.yelpcdn.com/bphoto/cQ1Yoa75m2yUFFbY2xwuqw/348s.jpg)

It can also be centered!

![Crepe](https://s3-media3.fl.yelpcdn.com/bphoto/cQ1Yoa75m2yUFFbY2xwuqw/348s.jpg){: .mx-auto.d-block :}

Here's a code chunk:

~~~
var foo = function(x) {
  return(x + 5);
}
foo(3)
~~~

And here is the same code with syntax highlighting:

```javascript
var foo = function(x) {
  return(x + 5);
}
foo(3)
```

And here is the same code yet again but with line numbers:

{% highlight javascript linenos %}
var foo = function(x) {
  return(x + 5);
}
foo(3)
{% endhighlight %}

## Boxes
You can add notification, warning and error boxes like this:

### Notification

{: .box-note}
**Note:** This is a notification box.

### Warning

{: .box-warning}
**Warning:** This is a warning box.

### Error

{: .box-error}
**Error:** This is an error box. -->