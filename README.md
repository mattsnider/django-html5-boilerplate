I really like using HTML5 boilerplate as the basis for all my websites, including my Django projects. In the past, I have included it as part of other projects, but find myself repeating the same steps for each new project. The Django HTML5 Boilerplate (DH5BP) project addresses this issue by incorporating the HTML5 Boilerplate (H5BP) project into an easy to consume Django-friendly Python package.

Find out for about HTML5 Boilerplate at https://github.com/h5bp/html5-boilerplate

This project differentiates itself from other H5BP to Django ports, by including Fabric scripts that automatically convert new versions of H5BP into a Django-friendly Python module. Ideally, this will make keeping up-to-date with the latest version of H5BP trivial.

Installation
============

Code is found at::

> https://github.com/mattsnider/django-html5-boilerplate

The easiest way to install is using pip::

> pip install django-html5-boilerplate

Requirements
============

To consume the package, you need only have a version of Django >= 1.3. This is the only dependency in the setup file.

To update the repository with the latest H5BP using the Fabric script, you will also need to install Fabric. I use Fabric >= 1.7, but the script is still very simple, so it will probably work on Fabric >= 1.0.

This library has been tested on Python >= 2.6.

Usage
=====

All static files and templates are namespaced under the directory DH5BP. You will need to include DH5BP in your `settings.py`:

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Uncomment the next line to enable the admin:
        'django.contrib.admin',
        # Uncomment the next line to enable admin documentation:
        'django.contrib.admindocs',
        ...
        'dh5bp',
        ...
    )

H5BP Template
-------------
Any template you want to inherit the H5BP page architecture include the following:

    {% extends 'dh5bp/base.html' %}
    {% load url from future %}
    {% load staticfiles %}
    {% block title %}YOUR TITLE HERE{% endblock %}
    {% block content %}YOUR PAGE MARKUP HERE{% endblock %}

If added a second template that puts all the JavaScript includes in the `head` tag. I don't recommend using this, unless you are using a mobile library like jQuery Mobile, which expects to be loaded before the body.

    {% extends 'dh5bp/base_script_in_head.html' %}
    {% load url from future %}
    {% load staticfiles %}
    {% block title %}YOUR TITLE HERE{% endblock %}
    {% block content %}YOUR PAGE MARKUP HERE{% endblock %}

Additionally, you can define more styles, meta, and other head-related markup in the title block:

    {% block head %}
        <link rel="stylesheet" href="{% static "css/YOUR_CSS.css" %}">
        <meta name="keywords" content="YOUR KEYWORD">
        ...
    {% endblock %}

The project expects you to create a /static/js/main.js file (see JavaScript notes below) for your primary script. To include JavaScript before or after main.js:

    {% block pre_main_script %}
        <script>
            var MySite = {
                // maybe put global variables passed from server here
            };
        </script>
        <!-- maybe another script file, like require.js -->
    {% endblock %}

    {% block post_main_script %}
        <script src="{% static "js/OTHER_JAVASCRIPT_FILE.js" %}"></script>
    {% endblock %}

If the enduser is viewing your site on a version of IE <= 7, then they will be shown a message indicating that they are using an outdated browser. To overwrite that message:

    {% block outdated_message %}
        <p class="browsehappy">YOUR MESSAGE</p>
    {% endblock %}

In v1.0.3+, there are two new template variables `html_attr` and `body_attr`, which can be used to add attributes to those html elements (such as `id` to the `body` tag and `manifest` to `html` tag). These variables should be provided as strings to the template.

If you use Google Analytics (GA), then H5BP includes the script for it right into the page. You will need to provide the template variable `DH5BP_GA_CODE` with your GA code to activate the script. You will probably want to use a context_processor for this:

> https://docs.djangoproject.com/en/dev/ref/templates/api/#writing-your-own-context-processors

JavaScript
----------
You will be provided the latest `jQuery`, `modernizr`, and a `console` polyfill from H5BP. In addition, the base template will look for a static file `js/main.js`. Put any JavaScript that is required for all pages of your site in `js/main.js`. I have created two blocks (as described above), where you can put JavaScript that needs to be execute before and after the main script.

If you want to use a different file name, instead of `js/main.js`, then provided the template variable `main_js` with the relative path to your JavaScript file from `STATIC_ROOT`. This variable should be provided as strings to the template.

Urls & Views
------------
The H5BP 404 page was ported over and wired up, as well as a similar looking 500 page. To use these in your project add the following to your `urls.py`:

    handler404 = 'dh5bp.views.page_not_found'
    handler500 = 'dh5bp.views.server_error'

I have wired up the default `favicon.ico`, `apple-touch-icon.png`, `humans.txt`, `robots.txt`, and `crossdomain.xml` from H5BP as well. To include those into your project, simply append the DH5BP urls to your urls:

    from dh5bp.urls import urlpatterns as dh5bp_urls

    urlpatterns = patterns('',
        # YOUR URLS
    )
    urlpatterns += dh5bp_urls

If you choose to change the behavior of these URLs, you can either not include these urls or declare your own version before adding the DH5BP urls (whichever definition occurs first will be the one used by Django).

What Isn't Included
===================

H5BP includes an `.htaccess` file for use with apache. Much of what this file is doing is outside of the scope of Django and should be handled by whatever static fileserver you are using, so I did not include it in this project.

Roadmap
=======

I don't think there is much missing right now, but I would like the to make the Fabric scripts more robust and to fail loudly if some step doesn't execute correctly, so that we know that something big has changed in H5BP.

Issues
======

https://github.com/mattsnider/django-html5-boilerplate/issues

Licensing
=========

Apache 2.0; see LICENSE file