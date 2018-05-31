# rapid-personal-sites

This app lets you drag and drop blocks to easily create websites.  You can manage the content and the layouts using templates and models that I've already created, and create as many pages as you like under the collabcake domain.

## Code

This site is developed primarily in JQuery and Bootstrap for the front-end and Python/Django/Wagtail for the back-end.  It hosts simple websites meant to showcase someone's talent.  Ideally it would host them on yourname.com.  

Models and templates are used to build pages that are hosted on one or more sites.  This can host multiple sites which are run out of just one instance of Wagtail.

## Rapid Development

This allows for rapid development of personal websites but scales to suit individuals of any skill level.  The ideal individual has some background in programming but it works for beginner, intermediate, and advanced skillsets.

## Workflow

1. Models are created for certain functions (documents, columns, calendars, portals, etc) that are handled the same way across websites
2. Templates are created which are similar but may have a slightly different look across websites
3. Custom CSS is created for each website to specialize the look and feel.  But, again, this is similar across websites.
4. People with no development experience can access the back-end to drag and drop webpage elements and design their site their way.  They can easily edit/create content and layouts based on the templates and models that were developed earlier.
5. Multiple sites can be developed with much code reusability.

## Requirements

Django 2.0.3  
mysqlclient  1.3.12  
wagtail 2.0  
