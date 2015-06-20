import os.path

# TODO: udpate to use Django's app-specific settings so
# they're not all shared in this library.

# Django doesn't explicitly provide this and assumes it can
# be derived on-demand from the request data, but this isn't
# always true with load-balanced setups and it needs to be
# a configuration setting. PRODUCTION WILL PROBABLY USE
# https:// BUT THIS WILL DEPEND ON THE SITE. We keep this as
# a separate field so we don't have to update all the
# hostname variables as well.
# NOTE: Django 1.7 adds a "scheme" property to the request
# object but since that's determined from the connection
# itself, it can be wrong.
SCULPT_SITE_PROTOCOL = 'http://'

# if this is set to True, then attempts to send email that
# fail will be quietly ignored; this should NEVER be set to
# True as a default, but it may be useful to do this during
# development until email credentials are properly set
SCULPT_EMAIL_FAIL_SILENTLY = False

# set this to a list of email addresses to capture all
# outbound email and direct it to the list instead (for
# debugging)
SCULPT_EMAIL_OVERRIDE_TOLIST = None

# by default email will appear to originate from a single
# (typically non-replyable) address; YOU MUST SET THIS
# as it's totally app-specific
#SCULPT_EMAIL_FROM = 'noreply@my_site.com'

# we need to know where email templates (in an 'email'
# folder) are stored, since we don't want to put 'email'
# in the base templates directory (which should be reserved
# for project/module names)
# NOTE: YOU MUST DEFINE THIS as it's completely app-specific
#SCULPT_EMAIL_TEMPLATE_BASE = 'my_app'

# Email messages often need to refer to the site; this will
# require the hostname and the protocol. The default for
# this should be ALLOWED_HOSTS[0] but that's not available
# when this module is imported, so you MUST set it in your
# main settings.py instead.
#SCULPT_EMAIL_SITE_HOSTNAME = ALLOWED_HOSTS[0]

# When processing forms we want to keep all the actual
# error messages in a centralized file to make them easier
# to find, but we also need to be able to override and
# extend the error messages with app-specific ones.
# This list should be redefined in settings.py to include
# the app's error messages file in addition to the core
# sculpt-ajax one.
SCULPT_AJAX_FORM_ERROR_MESSAGES = (
        'sculpt.ajax.form_errors',
    )

# if the sculpt.model_tools is available, this can be
# set to True to derive all AjaxView classes in a way
# that includes AjaxLoginRequiredMixin
SCULPT_AJAX_LOGIN_REQUIRED = False

# FastSave optimizes record saving to avoid extra queries,
# but assumes we never create records in the database with
# pre-defined IDs; if you are using FastSave and loading
# fixtures, you will need to disable this temporarily
#
# This should always default to True so that including
# FastSave in the inheritance path will result in the
# expected performance gains.
#
SCULPT_FASTSAVE = True
SCULPT_FASTSAVE_DUMP_INFO = False   # spew debugging information

# global defaults about login requirements
LOGIN_REQUIRED_DEFAULT = False
LOGIN_REDIRECT_LOCATION_DEFAULT = "/"
LOGIN_SESSION_KEY_DEFAULT = 'appuser_id'

# pagination defaults
#PAGINATION_URL_PAGE_KEY_DEFAULT = 'page'
#PAGINATION_PAGINATE_BY_DEFAULT = 24
#PAGINATION_SHOW_PAGE_NUMBER_AMOUNT_DEFAULT = 0

# s3files.StoredFile defaults
SCULPT_S3FILES_REMOTE_MODE = 'local'        # one of 'local', 's3'
SCULPT_S3FILES_BUCKET = None                # S3 bucket name
SCULPT_S3FILES_AUTO_EXPIRE_UPLOADS = 1.0    # default time, in days, before uploads auto-expire; use None to disable
SCULPT_S3FILES_CHECK_IMAGES = True          # whether to extract image metadata at upload time
SCULPT_S3FILES_DIR = None                   # if not None, contains a path fragment where uploads will go
SCULPT_S3FILES_REMOTE_URL = '/media/'       # URL base path for remote media

# revert to always using the temporary file upload handler
# as we always need to have the file on disk
#FILE_UPLOAD_HANDLERS = ( "django.core.files.uploadhandler.TemporaryFileUploadHandler", )

SCULPT_DEFAULT_TOAST_DURATION = 4

#
# debug-related settings
# NOTE: the defaults should ALWAYS BE OFF
#

# when dumping, which classes should be skipped?
# this is primarily a performance enhancement, as some
# of Django's internal data structures are very, very
# deeply nested
SCULPT_DEBUG_SKIP_CLASSES = (
    'django.db.models.sql.constants.JoinInfo',
    'django.db.models.sql.constants.SelectInfo',
)

# set this to True to report each request and its time;
# also enabled implicitly if DUMP_SQL or DUMP_SESSION
# are enabled
SCULPT_DUMP_REQUESTS = False

# set this to True to report all SQL queries with times
# after each request
SCULPT_DUMP_SQL = False

# set this to True to dump all session data at the end of
# each request
SCULPT_DUMP_SESSION = False

# set this to True to echo all AJAX requests/responses to
# the console
SCULPT_DUMP_AJAX = False

# if you want to use the standard error handlers, you will
# need to define the base directories for the message
# classes; 403, 404, and 500 especially rely on the "error"
# class
#SCULPT_MESSAGE_TEMPLATES = {
#        'error': 'appname/error',
#        'message': 'appname/message',
#    }
