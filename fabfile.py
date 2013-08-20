import os, re
from fabric.api import local


def cleanPackage():
    """
    Remove purges the package files that were created from H5BP.
    """
    local('rm -rf dh5bp/static')
    local('rm -rf dh5bp/templates')


def cleanup_h5bp():
    """
    Remove the fetched H5BP.
    """
    local('rm -rf html5-boilerplate')


def getLatestH5BP(cleanup=True):
    """
    Fetch the latest H5BP.
    """
    path_exists = os.path.exists('./html5-boilerplate')

    if cleanup and path_exists:
        cleanup_h5bp()
        path_exists = False

    if not path_exists:
        local('git clone https://github.com/h5bp/html5-boilerplate.git')


def migrateHtml():
    """
    Creates the necessary HTML template files and updates them as necessary to
    make them Django templates.
    """
    e404PathSource = os.path.join('html5-boilerplate', '404.html')
    indexPathSource = os.path.join('html5-boilerplate', 'index.html')

    templatePath = os.path.join('dh5bp', 'templates', 'dh5bp')
    local('mkdir -p %s' % templatePath)

    e404PathDest = os.path.join(templatePath, '404.html')
    e500PathDest = os.path.join(templatePath, '500.html')
    basePathDest = os.path.join(templatePath, 'base.html')

    local('cp %s %s' % (e404PathSource, e404PathDest))

    # create a 500 error page
    with open(e404PathSource, 'r') as f:
        text = ''.join(f.readlines())
        text = text.replace('Page Not Found', 'Internal Error')
        text = text.replace('Not found', 'Internal Error')
        text = re.sub('<p>[^<]+</p>', '', text)
        text = re.sub(re.compile(
            '<ul>.*?</ul>', flags=re.MULTILINE|re.DOTALL), '', text)
        text = text.replace(
            '</h1>', '</h1>\n'
                     '<p>We are sorry for the inconvenience, '
                     'but something went wrong.</p>'
                     '<p>We have logged the problem and will be '
                     'investigating soon.</p>'
                     '<p>Please go back and try again.</p>')

    with open(e500PathDest, 'w') as f:
        f.write(text)

    # prepare index.html for being a base template
    with open(indexPathSource, 'r') as f:
        text = ''.join(f.readlines())

        # add load staticfiles so we can use the static template tags
        text = text.replace(
            '<!DOCTYPE html>', '{% load staticfiles %}<!DOCTYPE html>')

        # add a attribute template variables to the HTML and BODY tag
        text = text.replace(
            '<html class', '<html {{ html_attr|safe }} class')
        text = text.replace(
            '<body>', '<body {{ body_attr|safe }}>')

        # update the head block (title, meta, additional scripts)
        text = text.replace(
            '<title></title>', '<title>{% block title %}{% endblock %}</title>')
        text = text.replace(
            'content=""', 'content="{% block description %}{% endblock %}"')
        text = text.replace(
            '</head>', '    {% block head %}{% endblock %}\n    </head>')


        # make CSS and JS paths use static
        text = re.sub('css/([^"]+)', '{% static "css/dh5bp/\\1" %}', text)
        text = re.sub('js/([^"]+)', '{% static "js/dh5bp/\\1" %}', text)

        # setup a GA variable, only include script block in final page,
        #   if the code is set
        text = text.replace('UA-XXXXX-X', '{{ DH5BP_GA_CODE }}')
        text = text.replace('<script>\n', '{% if DH5BP_GA_CODE %}<script>\n')
        text = text.replace(
            '\n        </script>', '\n        </script>{% endif %}')

        # create the content block
        text = text.replace('<p>', '{% block content %}<p>')
        text = text.replace('</p>', '</p>{% endblock %}')

        # wrap the legacy browser message, so it can be changed
        text = text.replace(
            '<p class="browsehappy">',
            '{% block outdated_message %}<p class="browsehappy">')

        # change the path for the main script
        text = text.replace(
            '<script src="{% static "js/dh5bp/main.js" %}"></script>',
            '{% block pre_main_script %}{% endblock %}\n'
            '        <script src="{% if main_js %}{% static main_js %}{% else %}{% static "js/main.js" %}{% endif %}"></script>\n'
            '        {% block post_main_script %}{% endblock %}')

    with open(basePathDest, 'w') as f:
        f.write(text)

    # Other Templates
    local('cp %s %s' % (
        os.path.join('html5-boilerplate', "*.xml"), templatePath))
    local('cp %s %s' % (
        os.path.join('html5-boilerplate', "*.txt"), templatePath))

def moveStatic():
    """
    Copy static files from H5BP to the appropriate place in the module.
    """
    # CSS
    cssPathSource = os.path.join('html5-boilerplate', 'css')
    cssPathDest = os.path.join('dh5bp', 'static', 'css', 'dh5bp')
    local('mkdir -p %s' % cssPathDest)
    local('cp %s %s' % (os.path.join(cssPathSource, "*.css"), cssPathDest))

    # JS
    jsPathSource = os.path.join('html5-boilerplate', 'js')
    jsPathDest = os.path.join('dh5bp', 'static', 'js', 'dh5bp')
    local('mkdir -p %s' % jsPathDest)
    local('cp %s %s' % (os.path.join(jsPathSource, "*.js"), jsPathDest))
    local('cp -R %s %s' % (os.path.join(jsPathSource, "vendor"), jsPathDest))

    # Images
    imgPathDest = os.path.join('dh5bp', 'static', 'img', 'dh5bp')
    local('mkdir -p %s' % imgPathDest)
    local('cp %s %s' % (
        os.path.join('html5-boilerplate', '*.png'), imgPathDest))
    local('cp %s %s' % (
        os.path.join('html5-boilerplate', '*.ico'), imgPathDest))


def update(purge=False, cleanup=True):
    """
    Run everything.
    Use "fab update:cleanup=" for setting cleanup to False
    """
    if purge:
        cleanPackage()
    getLatestH5BP(cleanup)
    moveStatic()
    migrateHtml()
    if cleanup:
        cleanup_h5bp()