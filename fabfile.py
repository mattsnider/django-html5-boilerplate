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
    baseJsOnTopPathDest = os.path.join(templatePath, 'base_script_in_head.html')

    local('cp %s %s' % (e404PathSource, e404PathDest))

    var_body_attr = 'body_attr'
    var_ga_code = 'DH5BP_GA_CODE'
    var_html_attr = 'html_attr'
    var_main_js = 'main_js'

    block_content = 'content'
    block_description = 'description'
    block_head = 'head'
    block_outdated_message = 'outdated_message'
    block_post_main_script = 'post_main_script'
    block_pre_main_script = 'pre_main_script'
    block_title = 'title'

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

        # remove non-conditional HTML comments
        text = re.sub('<!--(?!\[|>|<).+-->', '', text)

        # add a attribute template variables to the HTML and BODY tag
        text = text.replace(
            '<html class', '<html {{ %s|safe }} class' % var_html_attr)
        text = text.replace(
            '<body>', '<body {{ %s|safe }}>' % var_body_attr)

        # update the head block (title, meta, additional scripts)
        text = text.replace(
            '<title></title>',
            '<title>{%% block %s %%}{%% endblock %%}</title>' % block_title)
        text = text.replace(
            'content=""',
            'content="{%% block %s %%}{%% endblock %%}"' % block_description)
        text = text.replace(
            '</head>',
            '    {%% block %s %%}{%% endblock %%}\n'
            '    </head>' % block_head)


        # make CSS and JS paths use static
        text = re.sub('css/([^"]+)', '{% static "css/dh5bp/\\1" %}', text)
        text = re.sub('js/([^"]+)', '{% static "js/dh5bp/\\1" %}', text)

        # setup a GA variable, only include script block in final page,
        #   if the code is set
        text = text.replace('UA-XXXXX-X', '{{ %s }}' % var_ga_code)
        text = text.replace(
            '<script>\n', '{%% if %s %%}<script>\n' % var_ga_code)
        text = text.replace(
            '\n        </script>', '\n        </script>{% endif %}')

        # create the content block
        text = text.replace('<p>', '{%% block %s %%}<p>' % block_content)
        text = text.replace('</p>', '</p>{% endblock %}')

        # wrap the legacy browser message, so it can be changed
        text = text.replace(
            '<p class="browsehappy">',
            '{%% block %s %%}<p class="browsehappy">' % block_outdated_message)

        # cleanup extra lines
        text = text.replace('\n        \n', '        \n')
        text = text.replace('\n\n', '\n')

        # grab and remove the bottom script section
        rx_script_matcher = re.compile(
            '(<script src="//.*main.js".*?</script>)',
            flags=re.MULTILINE|re.DOTALL)
        script_section = re.search(rx_script_matcher, text).group(0)
        script_in_head = re.sub(rx_script_matcher, '', text)
        replacement_text = """
        {%% block %s %%}{%% endblock %%}
        <script src="{%% if %s %%}{%% static %s %%}{%% else %%}{%% static "js/main.js" %%}{%% endif %%}"></script>
        {%% block %s %%}{%% endblock %%}""" % (
            block_pre_main_script, var_main_js, var_main_js,
            block_post_main_script)
        text = re.sub(rx_script_matcher, '', text)
        script_section = '%s%s' % (
            script_section, replacement_text)
        script_section = script_section.replace(
            '<script src="{% static "js/dh5bp/main.js" %}"></script>', '')
        text = text.replace(
            '{% if DH5BP_GA_CODE %}',
            '%s\n        {%% if DH5BP_GA_CODE %%}' % script_section)

        # create a copy with scripts in the head section
        script_in_head = script_in_head.replace('</head>', """    %s
    </head>""" % script_section)

    # write the new text to base.html
    with open(basePathDest, 'w') as f:
        f.write(text)

    # write the new text to base_script_in_head.html
    with open(baseJsOnTopPathDest, 'w') as f:
        f.write(script_in_head)

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