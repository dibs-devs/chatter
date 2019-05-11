Customizing Django Chatter Templates
====================================

* **Host Chatter Templates Inside Your App**

  You can add chatter templates inside your own app's HTML files. For example, if you have
  reusable headers and footers in a :code:`base.html` file, then you can include
  that file's location in your :code:`settings` file like so:

  .. code-block:: python

    CHATTER_BASE_TEMPLATE="<your app templates directory>/base.html"

  Depending on how your template directories are defined, Django will try to find the
  template located in the location you've defined, and use it as a container for Chatter.
