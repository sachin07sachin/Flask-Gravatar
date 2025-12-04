# -*- coding: utf-8 -*-
#
# This file is part of Flask-Gravatar
# Copyright (C) 2014 Andrew Grigorev.
# Copyright (C) 2014 Nauman Ahmad.
# Copyright (C) 2014 Tom Powell.
# Copyright (C) 2015 CERN.
# Copyright (C) 2017 Jiri Kuncar.
# Copyright (C) 2018 Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Flask-Gravatar is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Small extension for Flask to make using Gravatar easy."""

import hashlib

from flask import current_app, has_request_context, request

from .version import __version__

try:
    # FIX: Safely attempt to import the deprecated object.
    # This will succeed on older Flask versions but raise ImportError on Flask 2.3+.
    from flask import _request_ctx_stack
except ImportError: # pragma: no cover
    # Define as None to gracefully handle Flask 2.3+ where this object was removed.
    _request_ctx_stack = None

try:
    # Try the modern app context stack
    from flask import _app_ctx_stack, has_app_context
except ImportError: # pragma: no cover
    # If app context stack fails (very old Flask)
    _app_ctx_stack = None
    has_app_context = None



# Which stack should we use? _app_ctx_stack is new in 0.9
connection_stack = _app_ctx_stack or _request_ctx_stack

def has_context():
    """Return True if either an app or a request context is active.

    Some Flask versions may not provide both helpers at import time, so
    check callability before calling them.
    """
    app_ctx_check = globals().get('has_app_context')
    req_ctx_check = globals().get('has_request_context')

    if callable(app_ctx_check):
        try:
            if app_ctx_check():
                return True
        except Exception:
            # defensive: if the helper raises for some reason, ignore it
            pass

    if callable(req_ctx_check):
        try:
            if req_ctx_check():
                return True
        except Exception:
            pass

    return False


class Property(object):
    """A property descriptor that sets and returns values."""

    def __init__(self, default, key=None):
        self.default = default
        self.key = key

    def __get__(self, obj, objtype):
        """Return value from application config, instance value or default."""
        # Prefer the value from current_app.config when an app context exists.
        try:
            if self.key and self.key in current_app.config:
                return current_app.config[self.key]
        except RuntimeError:
            # Accessing current_app outside app context raises RuntimeError.
            # We'll fall back to instance or default below.
            pass

        # If the Config check failed or there is no app context, then
        # check for an instance override (only if the instance exists).
        if obj is not None:
            if hasattr(obj, self.key):
                return getattr(obj, self.key)

        # Fallback to the default value defined on the descriptor.
        return self.default

    def __set__(self, obj, val):
        """Set instance value."""
        setattr(obj, self.key, val)


class Gravatar(object):
    """Simple object for gravatar link creation.

    .. code-block:: python

        gravatar = Gravatar(app,
                            size=100,
                            rating='g',
                            default='retro',
                            force_default=False,
                            force_lower=False,
                            use_ssl=False,
                            base_url=None
                           )
    """

    size = Property(100, key='GRAVATAR_SIZE')
    rating = Property('g', key='GRAVATAR_RATING')
    default = Property('retro', key='GRAVATAR_DEFAULT')
    force_default = Property(False, key='GRAVATAR_FORCE_DEFAULT')
    force_lower = Property(False, key='GRAVATAR_FORCE_LOWER')
    use_ssl = Property(None, key='GRAVATAR_USE_SSL')
    base_url = Property(None, key='GRAVATAR_BASE_URL')

    def __init__(self, app=None, **kwargs):
        """Initialize the Flask-Gravatar extension.

        :param app: Your Flask app instance
        :param size: Default size for avatar
        :param rating: Default rating
        :param default: Default type for unregistered emails
        :param force_default: Build only default avatars
        :param force_lower: Make email.lower() before build link
        :param use_ssl: Use https rather than http
        :param base_url: Use custom base url for build link
        """
        for key in tuple(kwargs.keys()):
            # Only set if the class actually defines this attribute
            # (so the Property descriptor is used instead of creating a plain attribute)
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs.pop(key))
        self.app = None

        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app):
        """Initialize the Flask-Gravatar extension for the specified application.

        :param app: The application.
        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.jinja_env.filters.setdefault('gravatar', self)
        app.extensions['gravatar'] = self

    def __call__(self, email, size=None, rating=None, default=None,
                 force_default=None, force_lower=False, use_ssl=None,
                 base_url=None):
        """Build gravatar link."""
        if size is None:
            size = self.size

        if rating is None:
            rating = self.rating

        if default is None:
            default = self.default

        if force_default is None:
            force_default = self.force_default

        if force_lower is None:
            force_lower = self.force_lower

        if force_lower:
            email = email.lower()

        if use_ssl is None:
            use_ssl = self.use_ssl

        if use_ssl is None and has_request_context():
            use_ssl = request.headers.get('X-Forwarded-Proto',
                                          request.scheme) == 'https'

        if base_url is None:
            base_url = self.base_url

        if base_url is not None:
            url = base_url + 'avatar/'
        else:
            if use_ssl:
                url = 'https://secure.gravatar.com/avatar/'
            else:
                url = 'http://www.gravatar.com/avatar/'

        hash = hashlib.md5(email.encode('utf-8')).hexdigest()

        link = '{url}{hash}'\
               '?s={size}&d={default}&r={rating}'.format(**locals())

        if force_default:
            link = link + '&f=y'

        return link

__all__ = ('Gravatar', '__version__')
