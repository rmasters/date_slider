# date_slider

A Django template tag that helps generate pagination for dates.

## Usage

### Add as an app

This isn't in pypi yet, so clone this repository in the root of your project:

    cd myproject
    git clone https://github.com/rmasters/date_slider.git
    
    or better:
    
    git submodule add https://github.com/rmasters/date_slider.git date_slider

### Add to `INSTALLED_APPS`

Ensure it is at the bottom, so you can override the templates.

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        ...
        
        'myapp',
        
        'date_slider',
    )

### Control display

In the template you want the control in:

    {% load date_slider %}
    {% date_slider date %}

### Date item display
    
Override and inherit the template `date_slider/slider.html`. You may need an
alternative template loader to do this (I'm using
[django-apptemplates][apptemplates]). With a directory structure like this, your
version of slider.html will be used instead of the default.

    project/
        date_slider/
            templates/
                date_slider/
                    slider.html     -- The default slider.html
        app/
            templates/
                date_slider/
                    slider.html     -- Your slider.html

`app/templates/date_slider/slider.html`

If there is a way to do this without an extra loader please submit a PR/issue.

Then, create your overriding and inheriting template like so. Note the
"date_slider:" part of the path is specific to django-apptemplates. You can
override the blocks defined in [slider.html](templates/date_slider/slider.html).

    {% extends "date_slider:date_slider/slider.html" %}

    {% block list_open %}<ul class="date-slider">{% endblock %}

    {% block current_item %}
    <li class="current_item"><a href="#">{{ date.date|date:"l jS" }}</a></li>
    {% endblock %}
    
    {% block item %}
    <li><a href="#">{{ date.date|date:"l jS" }}</a></li>
    {% endblock %}

[Date](templatetags/date_slider.py#L45) is a class that contains a
`datetime.date` instance and a couple of helpers.
    
## Todo

*   Allow option setting in the tag (optional arg),
*   Displayed entries for years and months,
*   Complete other options.

Released under the [MIT License](LICENSE).


[apptemplates]: https://pypi.python.org/pypi/django-apptemplates