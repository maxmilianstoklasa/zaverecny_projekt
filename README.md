# django CMS Divio quickstart

A Dockerised django CMS project, ready to deploy on Divio or another Docker-based cloud platform, and run
locally in Docker on your own machine. A Divio account is not required.

This version uses Python 3.8 running and the most up-to-date versions of Django 3.1 and django CMS 3.8.


## Try it

```bash
git clone git@github.com:divio/django-cms-divio-quickstart.git
cd django-cms-divio-quickstart
docker-compose build
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
docker-compose up
open http://127.0.0.1:8000
```

For a more complete how-to guide to this project, see [Deploy a new django CMS project using the Divio quickstart
repository](https://docs.divio.com/en/latest/how-to/django-cms-deploy-quickstart/) in the [Divio Developer
Handbook](https://docs.divio.com).


## Customising the project

This project is ready-to-go without making any changes at all, but also gives you some options.

As-is, it will include a number of useful django CMS plugins and Bootstrap 4 for the frontend. You don't have to use
these; they're optional. If you don't want to use them, read through the `settings.py` and `requirements.txt` files to
see sections that can be removed - in each case, the section is noted with a comment containing the word 'optional'.

Options are also available for using Postgres/MySQL, uWSGI/Gunicorn/Guvicorn, etc.

Again, see [Deploy a new django CMS project using the Divio quickstart
repository](https://docs.divio.com/en/latest/how-to/django-cms-deploy-quickstart/) for more guidance on customisation.
# djangocms
=======
# Závěrečný projekt ve 4. ročníku na SŠPU Opava
## Webová aplikace v Djangu - Ubytování chalupa Stoklasa s rezervačním systémem
##### http://www.stoklaska.cz/ -> stará webová stránka, stránka je zastaralá
### **- Co stránka potřebuje renovovat?**
#####   - Silnější SEO 
#####   - Novější vzhled 
#####   - Nový formulářový systém 
#####   - Rezervace webové stránky na třetí straně
### **- Provedení:**
#####   - Zcela nová webová aplikace s prvky staré (textový a mediální obsah, ...)
#####   - Jazyk: Python, Javascript, HTML, CSS
#####   - Framework: Django, jQuery
##### Zdroje: 
##### Hilda Dokonalá:https://www.youtube.com/channel/UCK75iN1Qw_cF5zvl1P2yv8Q
##### PVY IT3 SharePoint (videa z hodin): https://opava.sharepoint.com/sites/IT3PVY-Lu/Sdilene%20dokumenty/Forms/AllItems.aspx?viewid=ac2afcf1%2Ddb53%2D4c9a%2D8111%2D9ad960747ef8&id=%2Fsites%2FIT3PVY%2DLu%2FSdilene%20dokumenty%2FWebov%C3%A9%20datab%C3%A1zov%C3%A9%20aplikace%2FRecordings
##### Django website tutorial:https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django
##### Official django website: https://docs.djangoproject.com/en/3.1/ref/models/fields/#choices
##### Django Hostel managing system tutorial: https://medium.com/nybles/building-a-hostel-managing-system-with-django-d2dc85d9dec2
##### Django Hotel reservation tutorial (videos): https://www.youtube.com/watch?v=-9dhCQ7FdD0&list=PL_6Ho1hjJirn8WbY4xfVUAlcn51E4cSbY
##### Django - building a web app: https://youtu.be/olRw5yPaRlw
##### PhoneNumber model: https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
##### Čítač hodin: +- 35 hodin
