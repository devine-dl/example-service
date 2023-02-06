# devine-service-example

This is an example Devine service. Please do not email me for support, instead search for your question on the devine
repository. If your question was not found in a search, then ask your question in the Discussions tab.

## Folder Structure

```
/<Service Tag>/
  ├ /__init__.py
  ├ /config.yaml (optional)
  ├ /auth_class.py (any extra classes or code to use)
  └ /ssl_cert.pem (or any supplemental file)
```

The `__init__.py` file must contain a [Service Class](#service-class) of the same name as the folder name. It is
case-sensitive. An example service class with various documentation can be found in
[/EXAMPLE/\_\_init__.py](/EXAMPLE/__init__.py).

## Service Tags

Service tags generally follow these rules:

- Tag must be between 2-4 characters long, consisting of just `[A-Z0-9i]{2,4}`.
- `i`'s can only be lower-case for select services.
- If the Service's commercial name has a `+` or `Plus`, the last character should be a `P`.
  E.g., `ATVP` for `Apple TV+`, `DSCP` for `Discovery+`, `DSNP` for `Disney+`, and `PMTP` for `Paramount+`.

These rules are not exhaustive and should only be used as a guide. You don't strictly have to follow these rules, but
I recommend doing so for consistency.

## Tips

- You must import or access any file within the Service folders relatively. This includes imports.  
  Import like so: `from .auth_class import Auth` not `from devine.services.AMZN.auth_class import Auth`.
  Access files by taking advantage of `__file__` and `Path`, e.g., `Path(__file__, "../app_certificate.pem")`.
- You can store any arbitrary file(s) or folder(s) within the Service folders. However, you must remember to import
  or access them relative to the file you are accessing them from.
- If you don't like putting code in Service's `__init__.py` files, you may put the Service Class in a neighbouring
  `.py` file within the folder, then relatively import it from within `__init__.py`.

## Contributing

Feel free to make a pull request or a suggestion on a change relating to the Services or Documentation.
There is currently no strict ruleset to follow with code style or such, but try to follow what style it has
to the best of your ability.

* * *

© 2019-2023 rlaphoenix
