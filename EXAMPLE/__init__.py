from __future__ import annotations

from http.cookiejar import MozillaCookieJar
from typing import Any, Optional, Union

import click
import requests

from devine.core.constants import AnyTrack
from devine.core.service import Service
from devine.core.titles import Movies, Series
from devine.core.tracks import Chapter, Tracks
from devine.core.credential import Credential


class SERVICE_TAG(Service):
    """
    Service code for <Company>'s <Service Name> <Service Type> service (<main short link>).

    \b
    Authorization: Cookies (or Credentials, or both, or None)
    Robustness:
      Widevine:
        L1: 1080p
        L3: 576p
      PlayReady:
        SL3: 2160p (whitelisted)
        SL2: 1080p
        SL150: 576p

    \b
    Tips: - In this format, you may specify Service-specific tips
          - The \b at the start is to force the help-string to be rendered as-is with line breaks
          - Only specify short and sweet tips here, anything more should be a dedicated paragraph
          - All references to 'SERVICE_TAG' (e.g., this classes name) should be the cased service
            tag e.g., 'DSNP' not 'DisneyPlus' or 'dsnp', 'iT' not 'iTunes' or 'IT'.
          - If you have a question about something, look at other services and see if they answer
            your question by example.
    """

    # List of Service Aliases. Do NOT include the Service Tag. All aliases must be lowercase.
    ALIASES = ("fullname", "altname", "commonname", "and so on...")

    # List of regions of which the service offers support for.
    GEOFENCE = ("us",)

    @staticmethod
    @click.command(name="SERVICE_TAG", short_help="https://website.com", help=__doc__)
    @click.argument("title", type=str)
    @click.pass_context
    def cli(ctx: click.Context, **kwargs: Any) -> SERVICE_TAG:
        """
        Python-click CLI command.

        The entire purpose of this is just to define the CLI arguments for the service
        and pass them to the Service class's constructor.
        """
        return SERVICE_TAG(ctx, **kwargs)

    def __init__(self, ctx: click.Context, title: str):
        # Store argument data to class instance variables at the top of the constructor
        self.title = title

        # (important) This calls the base-service constructor, make sure this is after the above!
        super().__init__(ctx)
        # After this super() call, you now have various useful objects to work with like,
        # - self.log to log information. Will be `info` level unless debug mode is used.
        # - self.session to make HTTP calls with cookies set, common headers from config set,
        #   proxy set, and more. Use this unless you specifically need a session-less state (no auth/proxy).
        # - self.cache to cache data into the Cache directory. It allows you to set/get/update data based
        #   on a key (filename). This is great to cache auth tokens and retrieve them later on, with an
        #   expiry timestamp that is automatically handled.
        # - and more! Take a look at the base Service class's constructor to see what class instance variables
        #   get created, and what you could use them for.

        """
        From this point on the service constructor can be used for whatever you wish. My recommendations
        are to keep the constructor in the following layout with a line-break spacing them out.

        - <Store arguments to a class instance variable>
        - <Call the super() constructor call, passing the current click context>
        - <Get and store any parent-arguments from ctx.parent.params>
        - <Get and store any data from the Click context (ctx.obj)>
        - <Define any service-specific class instance variables>
        - <Write any service-specific initialization code. E.g., grabbing data from a Config endpoint>
          The constructor should not contain any login related code, whatsoever. You may deal with
          acquiring Device authorization bearers, but anything needing cookies or a login should
          NOT be in here! Use `authorize()` for that instead. Alterations or verification of
          arguments and their values/types should be done here.

        Overall, the constructor should be quick to read. If it has become long, you should likely
        move some of the service-specific code to a function and call that instead.

        When defining class instance variables, I recommend defining it WITHOUT a default value.
        If the default value is never actually used, then what's the point? Even a default of
        `None` is very pointless. Type-hint it with the type you expect to set it to further down
        the stack instead. This provides the benefit of a single possibility of type in type-hints.

        Avoid just moving a large proportion of the constructor to a function, e.g., a `configure()`.
        This is pointless and unnecessary. By design that seems like there's two functions to deal
        with constructor. Instead do multiple smaller functions.
        """

    # What next? Implement the following methods.
    # See the same named methods in the base Service class for more information on them.
    # The base Service class has a lot of information that you should read.
    # I highly recommend keeping these implemented in the same order as shown.

    # Optional methods:
    # These have universal default operations already defined in BaseService.
    # You may remove these functions completely if you cant or don't want to implement.

    def get_session(self) -> requests.Session:
        # modify the creation of the requests session (stored as self.session)
        # make a super() call to take the original result and further modify it,
        # or don't to make a completely fresh one if required.
        ...

    def authenticate(self, cookies: Optional[MozillaCookieJar] = None, credential: Optional[Credential] = None) -> None:
        # obtain authentication data like auth bearers or tokens using cookies and/or credentials.
        # I recommend making a check to ensure the required cookies and/or credentials for your service is
        # supplied, otherwise raise an EnvironmentError.
        # Only use this to get authentication data or setting up authentication state enough for the
        # future functions to be authorized.
        super().authenticate(cookies, credential)  # important
        ...

    # Required methods:

    def get_titles(self) -> Union[Movies, Series]:
        # the return type hint should only be what this service returns e.g.,
        # if it's a music service do `-> Album`, or Movie/TV do `-> Union[Movies, Series]`.
        ...

    def get_tracks(self, title: Union[Movies, Series]) -> Tracks:
        # the type hint for `title` param must match the return type of get_titles().
        # the same goes for any further function with a `title` param.
        ...

    def get_chapters(self, title: Union[Movies, Series]) -> list[Chapter]:
        # technically optional, but you must define and at least `return []`.
        ...

    def get_widevine_service_certificate(self, *, challenge: bytes, title: Union[Movies, Series], track: AnyTrack) -> Union[bytes, str]:
        # Return the service-specific certificate if used. If it uses the common google server one,
        # then return `common_privacy_cert` from the pywidevine Cdm class. If you see 'license.google.com'
        # in ASCII then it's the common Google License server certificate.

        # If you don't know what it is, you can pass this request to get_widevine_license, and it will send
        # a service-cert license request. The "license" returned will instead be the service cert.
        # Once obtained, I recommend manually saving it with a print or open().write() and then caching it
        # as base64. Remember to check if it's the common one or not. Do note that the cert may change over
        # time.

        # The return type should be accurate. You can return either str or bytes, but the return type should
        # be specific to one of the two, whatever the service's API returns it as. Avoid base64 decoding yourself
        # and such, as all of that is done for you.
        ...

    def get_widevine_license(self, *, challenge: bytes, title: Union[Movies, Series], track: AnyTrack) -> Optional[Union[bytes, str]]:
        # Send the license challenge (base64-encode it if needed) and return the license. You should check for and
        # handle any failed API calls, requests, errors, or such here.

        # The return type should be accurate. You can return either str or bytes, but the return type should
        # be specific to one of the two, whatever the service's API returns it as. Avoid base64 decoding yourself
        # and such, as all of that is done for you.
        ...

    # Service specific functions
    # These are functions of which will only be used by this service.
    # You can also store these in neighboring .py file(s) and import them relatively instead.
    # Don't be shy at creating many small functions instead of over-complicating other functions.
    # I recommend keeping the above 'Service specific functions' comment to have a clear divider.

    def get_api_config_data(self, device_id: str, version: int):
        # example
        ...

    # Service specific classes
    # This is similar to the above, but for service classes.
    # You can also store this in a neighboring .py file and import it relatively instead.

    class ServiceApiWrapper:
        # example
        ...
